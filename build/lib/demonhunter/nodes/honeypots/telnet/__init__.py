from demonhunter.nodes.honeypots import BaseHandler, BaseHoneypot

import asyncio
import time

from io import BytesIO

from telnetlib import (
    LINEMODE, NAWS, NEW_ENVIRON, BINARY, SGA, ECHO, STATUS,
    TTYPE, TSPEED, LFLOW, XDISPLOC, IAC, DONT, DO, WONT,
    WILL, SE, NOP, TM, DM, BRK, IP, AO, AYT, EC, EL, EOR,
    GA, SB, LOGOUT, CHARSET, SNDLOC, theNULL,
    # not supported or used,
    ENCRYPT, AUTHENTICATION, TN3270E, XAUTH, RSP,
    COM_PORT_OPTION, SUPPRESS_LOCAL_ECHO, TLS, KERMIT,
    SEND_URL, FORWARD_X, PRAGMA_LOGON, SSPI_LOGON,
    PRAGMA_HEARTBEAT, EXOPL, X3PAD, VT3270REGIME, TTYLOC,
    SUPDUPOUTPUT, SUPDUP, DET, BM, XASCII, RCP, NAMS,
    RCTE, NAOL, NAOP, NAOCRD, NAOHTS, NAOHTD, NAOFFD,
    NAOVTS, NAOVTD, NAOLFD)


iacBytes = {
    DO:   'DO',
    DONT: 'DONT',
    WILL: 'WILL',
    WONT: 'WONT',
    IP:   'IP'
}


class TelnetHandler(asyncio.Protocol, BaseHandler):
    """
    Copied twisted.protocols.telnet.Telnet mechanism.
    Thankyou twisted <3.
    """

    state = 0
    next_state = None

    username = None
    login_tries = 0
    authenticated = False

    gotIAC = 0
    iacByte = None
    lastLine = None
    buffer = b''
    echo = 0
    delimiters = [b'\r\n', b'\r\000']
    mode = "User"

    def __init__(self, honeypot):
        self.honeypot = honeypot

    def connection_made(self, transport):
        self.honeypot.active_attacks += 1
        self.transport = transport
        print("Connection from {0}".format(self.transport.get_extra_info('peername')[0]))
        self.write(self.welcome_message() + self.login_prompt())

    def write(self, data):
        """Send the given data over my transport."""
        self.transport.write(data)

    def welcome_message(self):
        return b"Welcome To Telnet Server\r\n\n"

    def login_prompt(self):
        return b"username: "

    def iacSBchunk(self, chunk):
        pass

    def iac_DO(self, feature):
        pass

    def iac_DONT(self, feature):
        pass

    def iac_WILL(self, feature):
        pass

    def iac_WONT(self, feature):
        pass

    def iac_IP(self, feature):
        pass

    def processLine(self, line):
        mode = getattr(self, "telnet_" + self.mode)(line)
        if mode is not None:
            self.mode = mode

    def telnet_User(self, user):
        self.username = user
        self.write(IAC + WILL + ECHO + b"password: ")
        return "Password"

    def telnet_Password(self, paswd):
        self.write(IAC + WONT + ECHO + b"\r\n")
        self.write(b"\r\nFail login\r\n")

        self.save_authentication(paswd)

        self.login_tries += 1
        if self.login_tries == 3:
            return "Done"
        else:
            if self.login_tries != 1:
                self.write(b'\r\n')
            self.write(self.login_prompt())
            return "User"

    def process_chunk(self, chunk):
        self.buffer = self.buffer + chunk

        for delim in self.delimiters:
            idx = self.buffer.find(delim)
            if idx != -1:
                break

        while idx != -1:
            buf, self.buffer = self.buffer[:idx], self.buffer[idx+2:]
            self.processLine(buf)
            if self.mode == 'Done':
                self.transport.close()

            for delim in self.delimiters:
                idx = self.buffer.find(delim)
                if idx != -1:
                    break

    def data_received(self, data):
        chunk = BytesIO()

        def iterbytes(originalBytes):
            for i in range(len(originalBytes)):
                yield originalBytes[i:i+1]

        for char in iterbytes(data):
            if self.gotIAC:
                if self.iacByte:
                    if self.iacByte == SB:
                        if char == SE:
                            self.iacSBchunk(chunk.getvalue())
                            chunk = BytesIO()
                            del self.iacByte
                            del self.gotIAC
                        else:
                            chunk.write(char)
                    else:
                        try:
                            getattr(self, 'iac_%s' % iacBytes[self.iacByte])(char)
                        except KeyError:
                            pass
                        del self.iacByte
                        del self.gotIAC
                else:
                    self.iacByte = char
            elif char == IAC:

                c = chunk.getvalue()
                if c:
                    why = self.process_chunk(c)
                    if why:
                        return why
                    chunk = BytesIO()
                self.gotIAC = 1
            else:
                chunk.write(char)

        c = chunk.getvalue()
        if c:
            why = self.process_chunk(c)
            if why:
                return why

    def set_username(self, data):
        self.username = data
        self.transport.write(IAC + WILL + ECHO)
        self.transport.write(b"password: ")

    def save_authentication(self, password):
        attack_time = time.time()
        print('Attack from {0}, with username {1}, and password {2}.'.format(self.transport.get_extra_info('peername')[0],
                                                                             str(self.username),
                                                                             str(password)))
        data = {
            'protocol':'telnet',
            'from':self.transport.get_extra_info('peername')[0],
            'username':self.username.decode('utf-8'),
            'password':password.decode('utf-8'),
            'time':attack_time
        }
        self.save_data(data)

    def connection_lost(self, exc):
        print("Connection lost from {0}".format(self.transport.get_extra_info('peername')[0]))
        self.honeypot.active_attacks -= 1


class DebianTelnet(TelnetHandler):
    def welcome_message(self):
        return b"Debian GNU/Linux 7\r\n\n"

    def login_prompt(self):
        return b"Login: "


class MicrosoftTelnet(TelnetHandler):

    def welcome_message(self):
        return b"Welcome to Microsoft Telnet Service\r\n\n"

    def login_prompt(self):
        return b"login: "


class TelnetHoneypot(BaseHoneypot):

    def __init__(self, handler=TelnetHandler, port=23, **kwargs):
        super(TelnetHoneypot, self).__init__(**kwargs)
        self.handler = handler
        self.port = port
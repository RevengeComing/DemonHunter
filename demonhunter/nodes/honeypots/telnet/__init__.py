from demonhunter.nodes.honeypots import BaseHandler

import asyncio
import time

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

def get_line(data):
    return data.decode().rstrip()


class TelnetHandler(asyncio.Protocol, BaseHandler):

    state = 0
    next_state = None

    username = None
    login_tries = 0
    authenticated = False

    def __init__(self, honeypot):
        self.honeypot = honeypot

    def connection_made(self, transport):
        self.honeypot.active_attacks += 1
        self.transport = transport
        print("Connection from {0}".format(self.transport.get_extra_info('peername')[0]))
        self.transport.write(self.welcome_message() + self.login_prompt())
        self.state = 'ask_username'

    def welcome_message(self):
        return b"Welcome To Telnet Server\r\n"

    def login_prompt(self):
        return b"username: "

    def set_username(self, data):
        self.username = data
        self.transport.write(IAC + WILL + ECHO)
        self.transport.write(b"password: ")

    def save_authentication(self, password):
        attack_time = time.time()
        print('Attack from {0}, with username {1}, and password {2}.'.format(self.transport.get_extra_info('peername')[0],
                                                                             self.username,
                                                                             password))
        data = {'protocol':'telnet', 'from':self.transport.get_extra_info('peername')[0],
                'username':self.username, 'password':password, 'time':attack_time}
        self.save_data(data)

    def data_received(self, data):

        if data == b"\xff\xf4\xff\xfd\x06":
            self.transport.write(b"Connection Closing")
            self.transport.close()
        elif not self.authenticated:
            self.do_authentication(data)

    def do_authentication(self, data):
        if self.state == "wait_for_confirm":
            self.state = self.next_state
        elif self.state == 'ask_username':
            if not self.username:
                self.set_username(get_line(data))
            self.state = "wait_for_confirm"
            self.next_state = "ask_password"
        elif self.state == 'ask_password':
            self.save_authentication(get_line(data))
            check_auth = False
            if check_auth:
                pass # give Shell, maybe medium interaction later.
            else:
                self.login_tries += 1
                self.transport.write(b"\r\nFail login\r\n")
                self.username = None
                self.transport.write(IAC + WONT + ECHO + b"\r\n")
                self.state = "wait_for_confirm"
                self.next_state = 'ask_username'
                self.transport.write(self.login_prompt())
                if self.login_tries == 3:
                    self.transport.close()

    def connection_lost(self, exc):
        print("Connection lost from {0}".format(self.transport.get_extra_info('peername')[0]))
        self.honeypot.active_attacks -= 1


class TelnetHoneypot:

    syslog = False
    sqlite = False
    agents = []

    active_attacks = 0

    interfaces = ['0.0.0.0']
    port = 23

    handler = TelnetHandler
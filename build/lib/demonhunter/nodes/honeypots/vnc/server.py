from demonhunter.nodes.honeypots import BaseHandler, BaseHoneypot

import asyncio
import binascii
import time
import ctypes

def make_challenge():
    """ Copied From VNC-Pot. Thankyou VNC-pot <3 """
    from random import randint
    a = randint(10000000, 99999999)
    b = randint(10000000, 99999999)
    c = randint(10000000, 99999999)
    d = randint(10000000, 99999999)
    abcd = str(a) + str(b) + str(c) + str(d)
    return binascii.unhexlify(abcd)


class VNCHandler(asyncio.Protocol, BaseHandler):
    """ Copied From VNC-Pot. Thankyou VNC-pot <3 """

    vnc_protocol_version = binascii.unhexlify("524642203030332e3030380a") # "RFB 003.008"
    challenge = None

    def __init__(self, honeypot):
        self.honeypot = honeypot

    def connection_made(self, transport):
        self.honeypot.active_attacks += 1
        self.transport = transport
        print("Connection from {0}".format(self.transport.get_extra_info('peername')[0]))
        # send "RFB 003.008"
        self.transport.write(self.vnc_protocol_version)
        self.state = 'wait_pversion'
        
    def data_received(self, data):
        if self.state == 'wait_pversion':
            if data == self.vnc_protocol_version:
                self.transport.write(binascii.unhexlify('0102'))
                print("Sending security types to %s" % self.transport.get_extra_info('peername')[0])
                self.state = 2
            else:
                self.unrecognized_data(data)
        elif self.state == 2:
            if data == binascii.unhexlify('02'):
                self.accept_vnc_authentication()
            else:
                self.unrecognized_data(data)
        elif self.state == 3:
            self.handle_password(data)

    def accept_vnc_authentication(self):
        self.transport.write(make_challenge())
        print("SuccessFul Security handshake from: %s" % self.transport.get_extra_info('peername')[0])
        self.state = 3

    def handle_password(self, data):
        attack_time = time.time()
        self.transport.write(binascii.unhexlify('00000001'))
        self.transport.write(binascii.unhexlify('00000045'))
        # Either the username was not recognised, or the password was incorrect
        a = '4569746865722074686520757365726e616d6520776173206e6f74207265636f676e697365642c206f72207468652070617373776f72642077617320696e636f7272656374'
        self.transport.write(binascii.unhexlify(a))
        self.transport.close()
        data = {
            'protocol':'vnc',
            'type':'authentication',
            'from':self.transport.get_extra_info('peername')[0],
            'time':attack_time
        }
        self.save_data(data)

    def unrecognized_data(self, data):
        attack_time = time.time()
        print("Unrecognized data from: %s" % self.transport.get_extra_info('peername')[0])
        self.transport.close()
        data = {
            'protocol':'vnc',
            'type':'unrecognized_data',
            'from':self.transport.get_extra_info('peername')[0],
            'data':str(data),
            'time':attack_time
        }
        self.save_data(data)

    def connection_lost(self, reason):
        print("Connection Lost From  %s" % self.transport.get_extra_info('peername')[0])
        self.honeypot.active_attacks -= 1
        self.state = 0

class VNCHoneypot(BaseHoneypot):

    def __init__(self, handler=VNCHandler, port=5900, **kwargs):
        super(VNCHoneypot, self).__init__(**kwargs)
        self.handler = handler
        self.port = port
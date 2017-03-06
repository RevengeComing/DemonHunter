import asyncio
import os

from httptools import HttpRequestParser

from demonhunter.nodes.honeypots import BaseHandler, BaseHoneypot

base = b"""
<!DOCTYPE html>
<html>
<head>
    <title>My Webserver</title>
</head>
<body>
    <div style='text-align:center;'>
        <h1>Hello and Congratz</h1>
        <p>You run your new webserver ...</p>
    </div>
</body>
</html>
"""

base_error = """
<!DOCTYPE html>
<html>
    <head>
        <title>{error_code} {status_text}</title>
    </head>
    <body bgcolor="white">
        <center>
            <h1>{error_code} {status_text}</h1>
        </center>
    </body>
</html>
"""

class HTTPHandler(asyncio.Protocol, BaseHandler):

    def __init__(self, honeypot):
        self.honeypot = honeypot
        self.set_timeout(3)
        self.req_headers = {}
        self.resp_headers = {}
        self.body = ""
    
    def set_timeout(self, timeout_sec):
        pass

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        hrp = HttpRequestParser(self)
        hrp.feed_data(data)
        self.request_version = hrp.get_http_version()
        self.send_response()

    def on_url(self, url):
        self.url = url
        # print(url)

    def on_body(self, body):
        self.body = body

    def on_header(self, name, value):
        self.req_headers[name] = value

    def set_status_code(self, code, text):
        self.resp_status_code = code
        self.resp_status_text = text

    def set_proto_version(self, version):
        self.resp_version = b'HTTP/%f' % version

    def run_default(self):
        self.set_proto_version(1.1)
        self.set_status_code(b'200', b'OK')
        self.resp_headers['Content-Type'] = 'text/html; encoding=utf8'
        self.resp_headers['Content-Length'] = str(len(base))
        self.resp_headers['Connection'] = 'close'
        self.resp_body = base

    def display_error(self, code, text):
        self.set_status_code(code, text)
        path = '%s%serror.html' % (self.honeypot.www_folder, self.url)
        if os.path.exists(path):
            print('asdas')
            self.resp_body = open(path, 'r').read()
        else:
            self.resp_body = base_error.format(error_code=code.decode('utf-8'),
                                               status_text=text.decode('utf-8')).encode()


    def send_response(self):
        self.set_proto_version(1.1)
        if not self.honeypot.www_folder:
            # Run Default Page
            self.run_default()
        else:
            if not os.path.isdir(self.honeypot.www_folder):
                self.run_default()
            else:
                if self.url.endswith(b'/'):
                    path = '%s%sindex.html' % (self.honeypot.www_folder, self.url.decode('utf-8'))
                    if os.path.exists(path):
                        self.resp_body = open(path, 'r').read().encode()
                        self.set_status_code(b'200', b'OK')
                    else:
                        self.display_error(b'404', b'Not Found')
                else:
                    path = '%s%s' % (self.honeypot.www_folder, self.url.decode('utf-8'))
                    if os.path.exists(path):
                        self.resp_body = open(path, 'r').read().encode()
                        self.set_status_code(b'200', b'OK')
                    else:
                        self.display_error(b'404', b'Not Found')

        print(self.resp_body)


        response_headers_raw = b''.join(b'%s: %s\n' % (k.encode(), v.encode()) for k, v in \
                                                self.resp_headers.items())
        
        self.transport.write(b'%s %s %s' % (self.resp_version, self.resp_status_code,
                                                        self.resp_status_text))
        self.transport.write(response_headers_raw)
        self.transport.write(b'\n')

        self.transport.write(self.resp_body)
        self.transport.close()

        saving_data = {
            'request_http_version': self.request_version,
            'response_http_version': self.resp_version,

            'request_headers': "\n".join(["%s: %s" % (key, value) for key, value\
                 in self.req_headers.items() ]),
            'response_headers': "\n".join(["%s: %s" % (key, value) for key, value\
                 in self.resp_headers.items() ]),

            'body': self.body,
            'url': self.url,

            'status_code': self.resp_status_code,
            "status_text": self.resp_status_text
        }
        self.save_data(saving_data)


class Apache(HTTPHandler):
    pass


class Nginx(HTTPHandler):
    pass


class HTTPHoneypot(BaseHoneypot):
    def __init__(self, handler=HTTPHandler, port=80, www_folder=None, **kwargs):
        super(HTTPHoneypot, self).__init__(**kwargs)
        self.handler = handler
        self.port = port
        self.www_folder = www_folder
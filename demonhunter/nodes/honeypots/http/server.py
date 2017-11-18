import datetime
import time
import logging
import os
import inspect
import asyncio

from httptools import HttpRequestParser
from httptools.parser.errors import (HttpParserInvalidMethodError,
    HttpParserError, HttpParserInvalidURLError)

from demonhunter.nodes.honeypots import BaseHandler, BaseHoneypot

HTTP_FOLDER_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
NGINX_FOLDER_PATH = os.path.join(HTTP_FOLDER_PATH, 'nginx/')
APACHE_FOLDER_PATH = os.path.join(HTTP_FOLDER_PATH, 'apache/')
DEFAULT_FOLDER_PATH = os.path.join(HTTP_FOLDER_PATH, 'default/')

# known_errors = {
#     'Bad Request': 'bad_request.html',   
# }

class HTTPHandler(asyncio.Protocol, BaseHandler):

    headers_count = 100
    max_header_size = 16384
    timeout = 10
    static_folder = DEFAULT_FOLDER_PATH

    def __init__(self, honeypot):
        self.honeypot = honeypot
        self.set_timeout(self.timeout)
        self.req_headers = {}
        self.resp_headers = {}
        self.setup_handler()
        self.body = ""
        self.error = False

    def add_resp_header(self, key, value):
        self.resp_headers[key] = value

    def setup_handler(self):
        with open(os.path.join(self.static_folder, 'index.html'), 'rb') as f:
            self.base = f.read()
        with open(os.path.join(self.static_folder, 'error.html'), 'r') as f:
            self.base_error = f.read()
    
    def set_timeout(self, timeout_sec):
        pass

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        hrp = HttpRequestParser(self)
        try:
            hrp.feed_data(data)
            self.request_version = hrp.get_http_version()
            self.send_response()
        except HttpParserInvalidMethodError:
            self.data = data
            self.error = True
            self.bad_request()
        except HttpParserError:
            self.data = data
            self.error = True
            self.bad_request()

    def on_url(self, url):
        self.url = url
        logging.debug('Request on %s at %s' % (url, str(datetime.datetime.now())))

    def on_body(self, body):
        self.body = body

    def on_header(self, name, value):
        # Its honeypot ? why did i set limitation ? i comment this piece of code
        # if len(value) > self.max_header_size:
        #     self.bad_request()
        #     return
        self.req_headers[name] = value

    def set_handler_server_name(self):
        self.add_resp_header('Server', self.server_details)

    @property
    def server_details(self):
        return 'DemonHunter (ubuntu)'

    def generate_date_header(self):
        self.add_resp_header('Date', str(datetime.datetime.now())) 

    def set_status_code(self, code, text):
        self.resp_status_code = code.encode()
        self.resp_status_text = text.encode()

    def set_content_length(self):
        if not self.resp_body:
            raise Exception("resp_body is None, you might call this function soon ...")
        self.resp_headers['Content-Length'] = str(len(self.resp_body))

    def set_proto_version(self, version):
        self.resp_version = b'HTTP/%s' % version

    def run_default(self):
        self.set_status_code('200', 'OK')
        self.resp_body = self.base

    def bad_request(self):
        self.display_error('400', "Bad Request", None)
        self.add_resp_header('Connection', 'close')
        self.finish_response()
        self.transport.close()

    def not_found(self):
        self.display_error('404', "Not Found", None)        

    def display_error(self, code, text, desc):
        self.set_status_code(code, text)
        if self.honeypot.www_folder and os.path.exists(
                        os.path.join(self.honeypot.www_folder, 'error.html')):
            path = os.path.join(self.honeypot.www_folder, 'error.html')
            self.resp_body = open(path, 'r').read().format(error_code=code,
                                                           status_text=text,
                                                           desc=desc,
                                                           server_details=self.server_details)
        else:
            self.resp_body = self.base_error.format(error_code=code,
                                                    status_text=text,
                                                    desc=desc,
                                                    server_details=self.server_details).encode()

    def send_response(self):
        if not self.honeypot.www_folder:
            if self.url == b"/" or self.url == b"/index.html":
                self.run_default()
            else:
                self.not_found()
        else:
            if self.url.endswith(b'/'):
                path = os.path.join(self.honeypot.www_folder,
                                    self.url.decode('utf-8'),
                                    'index.html')
                if os.path.exists(path):
                    self.resp_body = open(path, 'r').read().encode()
                    self.set_status_code('200', 'OK')
                else:
                    self.not_found()
            else:
                path = os.path.join(self.honeypot.www_folder, self.url.decode('utf-8'))
                if os.path.exists(path):
                    self.resp_body = open(path, 'r').read().encode()
                    self.set_status_code('200', 'OK')
                else:
                    self.not_found()
        self.finish_response()

    def finish_response(self):
        self.set_handler_server_name()
        self.set_proto_version(b'1.1')
        self.set_content_length()

        self.add_resp_header('Content-Type', 'text/html; charset=utf-8')
        self.generate_date_header()

        response_headers_raw = b''.join(b'%s: %s\n' % (k.encode(), v.encode()) for k, v in \
                                                self.resp_headers.items())
        
        self.transport.write(b'%s %s %s\n' % (self.resp_version, self.resp_status_code,
                                                        self.resp_status_text))
        self.transport.write(response_headers_raw)
        self.transport.write(b'\n')

        self.transport.write(self.resp_body)
        self.transport.close()
        self.prepare_data()

    def prepare_data(self):
        if not self.error:
            saving_data = {
                'protocol':'http',

                'request_http_version': str(self.request_version),
                # 'response_http_version': self.resp_version.decode('utf-8'),

                'request_headers': "\n".join(["%s: %s" % (key.decode('utf-8'), value.decode('utf-8'))
                     for key, value in self.req_headers.items() ]),
                # 'response_headers': "\n".join(["%s: %s" % (key, value)
                #      for key, value in self.resp_headers.items() ]),

                'body': self.body,
                'url': self.url.decode('utf-8'),

                'status_code': self.resp_status_code.decode('utf-8'),
                "status_text": self.resp_status_text.decode('utf-8'),

                'from':self.transport.get_extra_info('peername')[0],
                'time':time.time()
            }
            self.save_data(saving_data)
        else:
            saving_data = {
                'protocol':'http',

                'data_received': self.data.decode('utf-8'),

                'from':self.transport.get_extra_info('peername')[0],
                'time':time.time()
            }
            self.save_data(saving_data)
        self.clear()


    def clear(self):
        self.req_headers = {}
        self.resp_headers = {}
        self.resp_body = None
        self.body = ''
        self.data = None
        self.error = False


class Apache(HTTPHandler):
    """ Handler for Apache 2.4.18 """
    static_folder = APACHE_FOLDER_PATH

    def not_found(self):
        desc = "The requested URL %s was not found on this server." % (self.url.decode('utf-8'))
        self.display_error('404', "Not Found", desc)   

    def set_handler_server_name(self):
        self.resp_headers['Server'] = 'Apache 2.4.18 (Ubuntu)'

    @property
    def server_details(self):
        return "Apache/2.4.18 (Ubuntu) Server at {host} Port {port}"\
               .format(host=self.transport.get_extra_info('sockname')[0],
                       port=self.transport.get_extra_info('sockname')[1])


class Nginx(HTTPHandler):
    """ Handler for Nginx 1.10.0 """
    static_folder = NGINX_FOLDER_PATH

    def set_handler_server_name(self):
        self.resp_headers['Server'] = self.server_details

    @property
    def server_details(self):
        return "nginx/1.10.0 (Ubuntu)"

    def generate_date_header(self):
        "Tue, 16 May 2017 19:51:59 GMT"
        self.add_resp_header('Date', datetime.datetime.now().strftime('%a, %d %m %Y %H:%M:%S GMT')) 


class MicrosoftIIS(HTTPHandler):
    """ Handler for MicrosoftIIS """



class HTTPHoneypot(BaseHoneypot):
    def __init__(self, handler=HTTPHandler, port=80, www_folder=None, **kwargs):
        super(HTTPHoneypot, self).__init__(**kwargs)
        if handler == HTTPHandler:
            logging.warning("Default handler of DemonHunter http\
             honeypot is only for testing and its risky.")
        if not www_folder and handler == HTTPHandler:
            logging.warning("www_folder of DH's http honeypot shouldnt be None or its risky.")

        self.handler = handler
        self.port = port
        self.www_folder = www_folder
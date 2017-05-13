import asyncio

from aiohttp import web
from aiohttp.log import access_logger

@asyncio.coroutine
def index(request):
    text = "This is will be somewhere u can see DemonHunter's Reports."
    return web.Response(text=text)

def add_routes(app):
	app.router.add_get('/', index)

def run_app(app, *, host, port=None,
            shutdown_timeout=60.0, ssl_context=None,
            print=print, backlog=128, access_log_format=None,
            access_log=access_logger):
    """ Copied From aiohttp's main run_app """

    if port is None:
        if not ssl_context:
            port = 8080
        else:
            port = 8443

    loop = app.loop

    make_handler_kwargs = dict()
    if access_log_format is not None:
        make_handler_kwargs['access_log_format'] = access_log_format
    handler = app.make_handler(access_log=access_log,
                               **make_handler_kwargs)
    server = loop.create_server(handler, host, port, ssl=ssl_context,
                                backlog=backlog)
    srv, startup_res = loop.run_until_complete(asyncio.gather(server,
                                                              app.startup(),
                                                              loop=loop))

    scheme = 'https' if ssl_context else 'http'
    url = '{}://{}:{}'.format(scheme, host, port)
    print("DemonHunter Manager Web App Running on {}".format(url))

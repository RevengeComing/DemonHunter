from demonhunter.nodes.honeypots import BaseHandler, BaseHoneypot

class HTTPHandler(asyncio.Protocol, BaseHandler):
	pass


class Apache(HTTPHandler):
	pass


class Nginx(HTTPHandler):
	pass


class HTTPHoneypot(BaseHoneypot):
	pass
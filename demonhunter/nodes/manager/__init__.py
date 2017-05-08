from aiohttp import web

from demonhunter.nodes.manager.app import add_routes, run_app
from demonhunter.nodes.manager.agent.server import AgentManager
from demonhunter.core.loggers.logfile import FileLogger


class Manager:

    agents = list()
    def __init__(self, loop, server_address, agent_manager=True,
                 web_app=None, agent_password=None, logfile=None,
                 port=16742):
        self.server_address = server_address
        self.loop = loop
        self.port = port

        if agent_manager:
            if self.server_address is None:
                self.server_address = "127.0.0.1"
            coro = self.loop.create_server(lambda: AgentManager(self), self.server_address, self.port)
            server = self.loop.run_until_complete(coro)
            print('AgentManager Serving on {0}'.format(server.sockets[0].getsockname()))
            self.agent_password = agent_password

        if not web_app:
            app = web.Application(loop=self.loop)
            add_routes(app)
            run_app(app)

        if logfile:
            self.file_logger = FileLogger(logfile)


    def add_agent_address(self, address):
        self.agents.append(address)
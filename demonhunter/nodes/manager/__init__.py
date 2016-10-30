from aiohttp import web

from demonhunter.nodes.manager.app import add_routes, run_app
from demonhunter.nodes.manager.agent.server import AgentManager


class Manager:

    agents = list()

    def __init__(self, loop, agent_manager=True, web_app=None, agent_password=None):
        self.loop = loop

        if agent_manager:
            coro = self.loop.create_server(lambda: AgentManager(self), '127.0.0.1', 16742)
            server = self.loop.run_until_complete(coro)
            print('AgentManager Serving on {0}'.format(server.sockets[0].getsockname()))
            self.agent_password = agent_password

        if not web_app:
            app = web.Application(loop=self.loop)
            add_routes(app)
            run_app(app)

    def add_agent_address(self, address):
        self.agents.append(address)
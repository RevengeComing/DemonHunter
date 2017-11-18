from demonhunter.nodes.manager.agent.server import AgentManager
from demonhunter.core.loggers.logfile import FileLogger


class Manager:

    agents = list()
    def __init__(self, loop, server_address, webapp_address, agent_manager=True,
                 web_app=None, agent_password=None, logfile=None,
                 port=16742):
        self.server_address = server_address
        self.webapp_address = webapp_address
        self.loop = loop
        self.port = port

        if agent_manager:
            if self.server_address is None:
                self.server_address = "127.0.0.1"
            coro = self.loop.create_server(lambda: AgentManager(self), self.server_address, self.port)
            server = self.loop.run_until_complete(coro)
            print('AgentManager Serving on {0}'.format(server.sockets[0].getsockname()))
            self.agent_password = agent_password

        # if not web_app:
        #     app = web.Application(loop=self.loop)
        #     add_routes(app)
        #     if self.webapp_address is None:
        #         # this will only run internally, which I think is safe, but could run it on 0.0.0.0 by default
        #         self.webapp_address = "127.0.0.1"
        #     run_app(app, host=self.webapp_address)

        if logfile:
            self.file_logger = FileLogger(logfile)


    def add_agent_address(self, address):
        self.agents.append(address)

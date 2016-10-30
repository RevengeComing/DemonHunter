import asyncio

from demonhunter.nodes.manager import Manager


class DemonHunter:

    honeypots = list()
    servers = list()
    agents = list()

    def __init__(self, loop):
        self.loop = loop

    def add_honeypot(self, honeypot):
        self.honeypots.append(honeypot)

    def add_agent(self, agent):
        self.agents.append(agent)

    def start(self):
        for honeypot in self.honeypots:
            for interface in honeypot.interfaces:
                coro = self.loop.create_server(lambda: honeypot.handler(honeypot), interface, honeypot.port)
                server = self.loop.run_until_complete(coro)
                self.servers.append(server)
                print('Serving on {0}'.format(server.sockets[0].getsockname()))

    def stop(self):
        for server in self.servers:
            server.close()
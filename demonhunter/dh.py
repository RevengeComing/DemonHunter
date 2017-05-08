import asyncio


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
            server = honeypot.create_server(self.loop)
            self.servers.append(server)

    def stop(self):
        for server in self.servers:
            server.close()
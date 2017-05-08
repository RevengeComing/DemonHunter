import asyncio
import concurrent.futures

# from demonhunter.nodes.manager import Manager
current_hunter = None

def get_current_hunter():
    if current_hunter:
        return current_hunter
    raise Exception("You should create a DemonHunter instance before calling this function")

class DemonHunter:

    honeypots = list()
    servers = list()
    agents = list()

    executor = concurrent.futures.ThreadPoolExecutor(
        max_workers=1,
    )

    def __init__(self, loop):
        self.loop = loop
        global current_hunter
        if current_hunter:
            raise Exception("You Alreade made a DemonHunter instance ...")
        current_hunter = self

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
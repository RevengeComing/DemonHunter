import asyncio
import concurrent.futures

from demonhunter.nodes.honeypots import BaseHoneypot, Agent

# from demonhunter.nodes.manager import Manager
current_hunter = None

def get_current_hunter():
    if current_hunter:
        return current_hunter
    raise Exception("You should create a DemonHunter instance before calling this function")

class DemonHunter:
    """
        I am main class of this project, if u need to add honeypot or agent,
        you have to add it by my functions, also i have a function to start
        and stop honeypots.
    """

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
            raise Exception("You already made a DemonHunter instance ...")
        current_hunter = self

    def add_honeypot(self, honeypot):
        """ 
            To add honeypot protocol you shoud use me with input argument
            honeypot inheritted from BaseHoneypot class
        """
        if isinstance(honeypot, BaseHoneypot):
            self.honeypots.append(honeypot)
        else:
            raise Exception("honeypot has to be instance of BaseHoneypot class.")

    def add_agent(self, agent):
        """ 
            To add Agent to send data 
        """
        if isinstance(agent, Agent):
            self.agents.append(agent)
        else:
            raise Exception("agent has to be instance of Agent class.")

    def start(self):
        """ To start agents and honeypots you should call me. """
        for honeypot in self.honeypots:
            server = honeypot.create_server(self.loop)
            self.servers.append(server)

    def stop(self):
        """ To stop agents and honeypots you should call me. """
        for server in self.servers:
            server.close()

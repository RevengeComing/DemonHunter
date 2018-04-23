import asyncio
import json
import logging
import aiohttp

from demonhunter.core.loggers.logfile import FileLogger


class BaseHandler:
    # https://svn.nmap.org/nmap/nmap-service-probes

    def save_data(self, data):
        if self.honeypot.sqlite:
            self.save_in_sqlite(data)
        if self.honeypot.logfile:
            self.save_logfile(data)
        self.alter_agents(data)

    def alter_agents(self, data):
        for agent in self.honeypot.agents:
            asyncio.ensure_future(agent.send_data(data))

    def save_in_sqlite(self, data):
        pass

    def save_logfile(self, data):
        self.honeypot.file_logger.log(data)


class BaseHoneypot(object):
    
    active_attacks = 0

    def __init__(self, logfile=None, sqlite=None, interfaces=['0.0.0.0']):
        self.logfile = logfile
        self.sqlite = sqlite
        self.interfaces = interfaces

        if self.logfile:
            self.file_logger = FileLogger(self.logfile)

        self.agents = []

    def add_agent(self, agent):
        self.agents.append(agent)

    def create_server(self, loop):
        coro = loop.create_server(lambda: self.handler(self), self.interfaces, self.port)
        server = loop.run_until_complete(coro)
        for socket in server.sockets:
            logging.info('Serving on {0}'.format(socket.getsockname()))
        return server


class Agent():
    def __init__(self, manager_address, honeypots, token):
        for honeypot in honeypots:
            honeypot.agents.append(self)

        self.manager_address = manager_address
        if manager_address.endswith('/'):
            self.manager_address = manager_address[:-1]
        self.token = token

    @property
    def _address(self):
        return "%s/agents/call/%s/" % (self.manager_address, self.token)

    async def send_data(self, data):
        async with aiohttp.ClientSession() as session:
            async with session.post(self._address, json=data) as resp:
                pass
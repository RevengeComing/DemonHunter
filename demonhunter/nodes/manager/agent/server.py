import asyncio
import json


class AgentManager(asyncio.Protocol):
	'''
	ask for password and send password to trust each other
	'''

	state = 0

	def __init__(self, manager):
		self.manager = manager

	def connection_made(self, transport):
		self.transport = transport
		if not self.transport.get_extra_info('peername')[0] in self.manager.agents:
			# TODO: Log Stupid Connections
			self.transport.close()
		else:
			self.transport = transport
			data = b"Hello Agent!"
			if self.manager.agent_password:
				data +=  b' Give Me The Night Word'
			else:
				self.state = 1
			self.transport.write(data)

	def data_received(self, data):
		if not self.transport.get_extra_info('peername')[0] in self.manager.agents:
			return		
		if self.state == 0: # getting password
			if self.manager.agent_password == data:
				self.transport.write('Now Tell Me The Report')
				self.state = 1
		elif self.state == 1:
			data = json.loads(data.decode())
			data['attack_to'] = self.transport.get_extra_info('peername')[0]
			self.manager.file_logger.log(data)
			self.transport.close()
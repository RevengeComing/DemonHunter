import asyncio

from demonhunter import DemonHunter
from demonhunter.nodes.honeypots.telnet import TelnetHoneypot, MicrosoftTelnet
from demonhunter.nodes.honeypots import Agent

loop = asyncio.get_event_loop()

# Create A DemnonHunter Instance , its the heart of our honeypot
hp = DemonHunter(loop)

# Create your honeypot instaces, telnet/ssh/...
telnet = TelnetHoneypot()
# Which Handler You Prefer for your honeypot ?
telnet.handler = MicrosoftTelnet
# Add your honeypots to handler
hp.add_honeypot(telnet)

# Create An Agent, Where Should data transfered ?
agent = Agent(["127.0.0.1"], [telnet], loop)
# Add The Agent To your DemonHunter Instance
hp.add_agent(agent)

# Start The Honeypot
hp.start()

try:
    # Run The Loop
	loop.run_forever()
except KeyboardInterrupt:
	hp.stop()
	print("\nServer Closed")

loop.close()
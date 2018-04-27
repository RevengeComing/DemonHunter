import asyncio

from demonhunter import DemonHunter
from demonhunter.nodes.honeypots.telnet import TelnetHoneypot, MicrosoftTelnet
from demonhunter.nodes.honeypots.vnc import VNCHoneypot
from demonhunter.nodes.honeypots import Agent

loop = asyncio.get_event_loop()

# Create A DemnonHunter Instance , its the heart of our honeypot
hp = DemonHunter(loop)

# Create your honeypot instaces, telnet/ssh/...
vnc = VNCHoneypot(interfaces=["b.b.b.b"])
# Add your honeypots to DemnonHunter Instance
hp.add_honeypot(vnc)

# Create your honeypot instaces, telnet/ssh/...
telnet = TelnetHoneypot(port=8023, handler=MicrosoftTelnet, interfaces=["x.x.x.x", "y.y.y.y"])
# Add your honeypots to DemnonHunter Instance
hp.add_honeypot(telnet)

# Create An Agent, Where Should data transfered ?
agent = Agent(["http://localhost:8000"], [telnet, vnc], loop)
# Add The Agent To your DemonHunter Instance
hp.add_agent(agent)

# Create An Agent, and only send telnet data's ?
agent = Agent(["a.a.a.a"], [telnet], loop)
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
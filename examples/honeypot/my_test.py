import asyncio

from demonhunter import DemonHunter
from demonhunter.nodes.honeypots.telnet import TelnetHoneypot, MicrosoftTelnet
from demonhunter.nodes.honeypots.vnc import VNCHoneypot
from demonhunter.nodes.honeypots.http import HTTPHoneypot

loop = asyncio.get_event_loop()
hp = DemonHunter(loop)


vnc = VNCHoneypot(interfaces=["0.0.0.0"])
hp.add_honeypot(vnc)

telnet = TelnetHoneypot(port=23, handler=MicrosoftTelnet, interfaces=["0.0.0.0"])
hp.add_honeypot(telnet)

hp.start()

try:
    # Run The Loop
	loop.run_forever()
except KeyboardInterrupt:
	hp.stop()
	print("\nServer Closed")

loop.close()
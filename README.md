# DemonHunter

If you want to create low interaction Honepot Server in less than an hour you should follow this repository. 

## Installation:
install DemonHunter from pypi:
```
pip install demonhunter
```

---------------------------

To run a simple Honeypot:
```
import asyncio

from demonhunter import DemonHunter
from demonhunter.nodes.honeypots.telnet import TelnetHoneypot, DebianTelnet, MicrosoftTelnet
from demonhunter.nodes.honeypots import Agent

loop = asyncio.get_event_loop()

hp = DemonHunter(loop)

telnet = TelnetHoneypot()
telnet.handler = MicrosoftTelnet # or DebianTelnet
hp.add_honeypot(telnet)

hp.start()

try:
	loop.run_forever()
except KeyboardInterrupt:
	hp.stop()
	print("\nServer Closed")

loop.close()
```

if you want a honeypot with agent:

```
import asyncio

from demonhunter import DemonHunter
from demonhunter.nodes.honeypots.telnet import TelnetHoneypot, DebianTelnet, MicrosoftTelnet
from demonhunter.nodes.honeypots import Agent

loop = asyncio.get_event_loop()

hp = DemonHunter(loop)

telnet = TelnetHoneypot()
telnet.handler = MicrosoftTelnet # or DebianTelnet
hp.add_honeypot(telnet)

agent = Agent(["127.0.0.1"], [telnet], loop) # change 127.0.0.1 with yout Agent Manager Address
hp.add_agent(agent)

hp.start()

try:
	loop.run_forever()
except KeyboardInterrupt:
	hp.stop()
	print("\nServer Closed")

loop.close()
```

for agent based honeypot you need an Agent Manager to get data from agents:

```
import asyncio

from demonhunter import Manager

loop = asyncio.get_event_loop()

manager = Manager(loop, logfile='test.log')
manager.add_agent_address('127.0.0.1')

try:
    loop.run_forever()
except KeyboardInterrupt:
    print("\nServer Closed")

loop.close()
```

The Agent Manager Server runs on port 16742, it has also a web_app running on port 8080 but not yet complete.


###### TODO:
- Create Example Code
- Create Web App For Manager
- Documentation

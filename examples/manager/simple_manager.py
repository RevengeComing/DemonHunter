import asyncio

from demonhunter import Manager

loop = asyncio.get_event_loop()

# You can set logfile location to any place like "/var/log/demonhunter.log"
manager = Manager(loop, logfile='test.log')
# Specify The Location of Agents ?
manager.add_agent_address('127.0.0.1')

try:
    # Run The Loop
    loop.run_forever()
except KeyboardInterrupt:
    print("\nServer Closed")

loop.close()
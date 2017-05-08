import asyncio
from demonhunter import Manager

loop = asyncio.get_event_loop()

# You can set logfile location to any place like "/var/log/demonhunter.log"
# specify management IP via server_address
# manager = Manager(loop, server_address='10.10.10.10', logfile='events.log')
manager = Manager(loop, server_address=None, logfile='events.log')
# Specify The Location of Agents ?
manager.add_agent_address("107.170.73.18")

try:
    loop.run_forever()
except KeyboardInterrupt:
    print("\nServer Closed")

loop.close()
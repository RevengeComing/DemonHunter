import asyncio
from demonhunter import Manager

loop = asyncio.get_event_loop()

# You can set logfile location to any place like "/var/log/demonhunter.log"
# specify management IP via server_address
# specify web application address via webapp_address
# specify the server port via port
#
#     openssl req -x509 -newkey rsa:2048 -keyout selfsigned.key -nodes \
#                 -out selfsigned.cert -sha256 -days 1000
#
# use 'localhost' as Common Name

manager = Manager(loop, server_address='127.0.0.1', logfile='events.log', webapp_address='0.0.0.0', port=8888,
                  certificate='selfsigned.cert', key='selfsigned.key')

# Specify The Location of Agents ?
manager.add_agent_address("127.0.0.1")

try:
    loop.run_forever()
except KeyboardInterrupt:
    print("\nServer Closed")

loop.close()

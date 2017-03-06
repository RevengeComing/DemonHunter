import asyncio

try:
    import aioodbc
except:
    raise Exception("Please Install aioodbc package from pypi if u want to use sqlite database : \"apt-get install unixodbc unixodbc-dev;pip install aioodbc\"")

class LogSQLite():

    def __init__(self, sqlite_file, loop):
        self.sqlite_file = sqlite_file
        self.loop = loop

    def get_cstring(self):
        return 'Driver=SQLite;Database=test_db.sqlite'
        # return 'Driver=SQLite;Database=%s' % self.sqlite_file

    async def get_pool(self):
        await aioodbc.create_pool(dsn=self.get_cstring(), loop=self.loop)

    async def execute(self, sql):
        pool = await self.get_pool()
        async with pool.acquire() as conn:
            cur = await conn.cursor()
            await cur.execute(sql)
            r = await cur.fetchall()
            print(r)
        # conn = await aioodbc.connect(dsn=get_cstring(), loop=self.loop)

        # cur = await conn.cursor()
        # await cur.execute("SELECT 42;")
        # r = await cur.fetchall()
        # print(r)
        # await cur.close()
        # await conn.close()

if __name__ == "__main__":    
    loop = asyncio.get_event_loop()

    logsql = LogSQLite('/home/azarakhsh/works/DemonHunter/test.db', loop)
    print(logsql.get_cstring())
    loop.run_until_complete(logsql.execute('''CREATE TABLE stocks
             (date text, trans text, symbol text, qty real, price real)'''))

    loop.close()
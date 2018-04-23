from .webapp import app


class Manager:
    agents = list()
    def __init__(self, host, port,
    			 pg_host, pg_user,
                 pg_pass, pg_database):
        self.host = host
        self.port = port

        self.pg_host = pg_host
        self.pg_user = pg_user
        self.pg_pass = pg_pass
        self.pg_database = pg_database

        self.app = app
        self.app.dh_manager = self

    def run_webapp(self):
        from meinheld import server, middleware
        server.listen(("0.0.0.0", 8000))
        server.run(middleware.WebSocketMiddleware(self.app))
import os
import string

from random import choice

from .webapp import app, db, sockets, login_manager


alphabet = string.ascii_letters + string.digits


class Master:
    agents = list()
    def __init__(self, host, port, db_type,
    			 sqlite=None, pg_host=None, pg_user=None,
                 pg_pass=None, pg_database=None):
        self.host = host
        self.port = port

        if db_type == "sqlite" and not sqlite.startswith('/'):
            sqlite = str(os.getcwd() + '/' + sqlite)
            
        if db_type == "sqlite":
            self.db_string = "sqlite:///%s" % sqlite
        elif db_type == "postgres":
            self.db_string = 'postgresql://{pg_user}:{pg_pass}@\
            {pg_host}/{pg_database}'.format(pg_user=pg_user, pg_pass=pg_pass,
                                            pg_host=pg_host, pg_database=pg_database)

        app.dh_manager = self
        self.configure_webapp()
        self.init_extensions()

    def configure_webapp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = self.db_string
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SECRET_KEY'] = ''.join(choice(alphabet) for i in range(64))

    def init_extensions(self):
        login_manager.login_view = "login"
        login_manager.init_app(app)
        db.init_app(app)
        sockets.init_app(app)

    def run_webapp(self):
        from meinheld import server, middleware
        server.listen((self.host, self.port))
        server.run(middleware.WebSocketMiddleware(app))
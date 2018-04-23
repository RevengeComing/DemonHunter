from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_sockets import Sockets

login_manager = LoginManager()
db = SQLAlchemy()
sockets = Sockets()
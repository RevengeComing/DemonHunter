import datetime
import asyncio
import bcrypt


from itsdangerous import URLSafeSerializer

from flask_login import UserMixin

from .ext import db, login_manager

__all__ = (
    'User', 'HoneypotData', "Agent"
)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)

    username = db.Column(db.String(32), unique=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, _password):
        self.password_hash = bcrypt.hashpw(_password.encode('utf8'),
            bcrypt.gensalt()).decode()

    def check_password(self, _password):
        return bcrypt.checkpw(_password.encode('utf8'),
            self.password.encode('utf8'))


@login_manager.user_loader
def load_user(session_token):
    return User.query.filter_by(id=session_token).first()    


class HoneypotData(db.Model):
    __tablename__ = "honeypot_datas"
    id = db.Column(db.Integer(), primary_key=True)

    honeypot_address = db.Column(db.String(16), nullable=False)
    from_address = db.Column(db.String(16), nullable=False)
    attack_time = db.Column(db.Integer())
    
    protocol = db.Column(db.String(32))
    data = db.Column(db.Text)

    def utc_time(self):
        dt = datetime.datetime.utcfromtimestamp(self.attack_time)
        return "%s/%s/%s %s:%s:%s" % (
                dt.year, dt.month, dt.day,
                dt.hour, dt.minute, dt.second
            )


class Agent(db.Model):
    __tablename__ = "agents"
    id = db.Column(db.Integer(), primary_key=True)

    address = db.Column(db.String(32), index=True, nullable=False)
    token = db.Column(db.String(64), index=True)
    last_message = db.Column(db.Integer)

    def generate_token(self):
        s = URLSafeSerializer('secret-key')        
        self.token = s.dumps(self.address)
        return self.token

    def utc_time(self):
        if self.last_message:
            dt = datetime.datetime.utcfromtimestamp(self.last_message)
            return "%s/%s/%s %s:%s:%s" % (
                    dt.year, dt.month, dt.day,
                    dt.hour, dt.minute, dt.second
                )
        else:
            return "never"
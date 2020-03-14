from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from mors_module import db, login_manager


class ChatMessages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(64), index=True)
    text = db.Column(db.String(280))
    timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return '<Message {0} from {1}>'.format(self.id, self.author)


class Program(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    broadcast_id = db.Column(db.Integer)
    time = db.Column(db.String(15))
    title = db.Column(db.String(140), index=True)
    hosts = db.Column(db.String(240), index=True)

    def __repr__(self):
        return '<Schedule for {}>'.format(self.title)


class Broadcast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)

    def __repr__(self):
        return '<Broadcast {}>'.format(self.date)


class CurrentProgram(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    time = db.Column(db.String(140))

    def __repr__(self):
        return '<Current {}>'.format(self.name)


class User(db.Model, UserMixin):
    '''
        модель юзверя
    '''
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(32))
    email = db.Column(db.String(140))
    name = db.Column(db.String(32))
    password_hash = db.Column(db.String(140))

    def set_password(self, password):
        '''
            сеттим пароль
        '''
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        '''
            чекаем пароль
        '''

        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))

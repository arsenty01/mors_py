from mors_module import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Chat_messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(64), index=True)
    text = db.Column(db.String(280))
    timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return '<Message {0} from {1}>'.format(self.id, self.author)


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    title = db.Column(db.String(140), index=True)
    guests = db.Column(db.String(240), index=True)

    def __repr__(self):
        return '<Schedule for {}>'.format(self.title)
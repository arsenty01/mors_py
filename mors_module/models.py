from mors_module import db


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
    date = db.Column(db.String(10))

    def __repr__(self):
        return '<Broadcast {}>'.format(self.date)


class CurrentProgram(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    time = db.Column(db.String(140))

    def __repr__(self):
        return '<Current {}>'.format(self.name)



from mors_module import db
from mors_module.models import ChatMessages, Program, Broadcast
from datetime import datetime


def get_schedule(date):
    broadcast_id = list(map(lambda x: x.id, db.session.query(Broadcast.id).filter(Broadcast.date == datetime.strptime(date, '%d.%m.%Y'))))[0]
    return list(map(lambda x: {'time': x.time, 'title': x.title, 'hosts': x.hosts}, db.session.query(Program.time, Program.title, Program.hosts).filter(Program.broadcast_id == broadcast_id)))

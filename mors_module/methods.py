from mors_module.models import Broadcast
from mors_module import db


def get_nearest_date(tmp_date):
    """Выбирает ближайшую дату к исходной
    :param: tmp_date - исходная дата"""
    next_date = db.session.query(db.func.min(Broadcast.date)).filter(Broadcast.date >= tmp_date).one()[0]
    previous_date = db.session.query(db.func.max(Broadcast.date)).filter(Broadcast.date <= tmp_date).one()[0]
    return next_date if (next_date - tmp_date) < (tmp_date - previous_date) else previous_date

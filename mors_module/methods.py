from mors_module.models import Broadcast, Program, ChatMessages, CurrentProgram
from mors_module import db
import datetime


def get_next_or_last_broadcast(tmp_date):
    """Возвращает дату следующего эфира, если он есть. Если нет, то дату последнего эфира
    :param: tmp_date - исходная дата
    :return: ближайшая дата
    """
    select_min = db.func.min(Broadcast.date)  # Выбор минимального
    where_next = Broadcast.date >= tmp_date   # из следующих
    select_max = db.func.min(Broadcast.date)  # Выбор максимального
    where_prev = Broadcast.date <= tmp_date   # из предыдущих

    next_date = db.session.query(select_min).filter(where_next).one()[0]
    if next_date:
        return next_date
    previous_date = db.session.query(select_max).filter(where_prev).one()[0]
    if previous_date:
        return previous_date
    raise Exception('Таблица эфиров пустая')


def get_schedule_by_date(date: datetime):
    """
    Возвращает расписание на выбранную дату
    :param date: дата
    :return: Расписание
    """
    bobj = Broadcast.query.filter(Broadcast.date == date).first()
    schedule = Program.query.filter(Program.broadcast_id == bobj.id).all()
    programs_json = []
    for item in schedule:
        programs_json.append({
            'title': item.title,
            'hosts': item.hosts,
            'time': item.time
        })
    return programs_json

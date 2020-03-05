from mors_module import application, socketio
from mors_module import db
from mors_module.currently_playing import *
from mors_module.models import ChatMessages, Program, Broadcast
from mors_module.methods import get_nearest_date
from flask import render_template
from flask_socketio import emit
from datetime import datetime


@application.route('/')
@application.route('/index')
def index():
    cp_obj = CurrentlyPlaying()
    current_program = cp_obj.now_playing()
    broadcasts = Broadcast.query.all()
    today = datetime.today()
    #todo Здесь нужен метод получающий расписание по дейттайму
    schedule = Program.query.filter(Broadcast.date == get_nearest_date(today)).all()
    chat_messages = ChatMessages.query.order_by(ChatMessages.id.desc()).limit(20)

    print('broadcasts', broadcasts)
    print('schedule', schedule)

    return render_template('main_page.html',
                           schedule=schedule,
                           broadcasts=broadcasts,
                           version='20.31 (alpha)',
                           chat_messages=chat_messages,
                           current_program=current_program)


@socketio.on('sent_message')
def get_messages(message):
    msg = ChatMessages(**message, timestamp=datetime.today())
    db.session.add(msg)
    db.session.commit()
    emit('new_message', {
        'author': message['author'],
        'text': message['text'],
        'timestamp': msg.timestamp.strftime('%d.%m.%Y, %H:%M:%S')
    }, broadcast=True)


@socketio.on('cp_request')
def currently_playing():
    cp_obj = CurrentlyPlaying()
    emit('cp_response', cp_obj.now_playing())


@socketio.on('refresh_schedule')
def refresh_schedule(date):
    date_dt = datetime.strptime(date, '%d.%m.%Y')
    #todo сюдой тоже
    broadcast = Broadcast.query.filter(Broadcast.date == date_dt).first()
    if broadcast:
        broadcast_id = broadcast.id
        schedule = Program.query.filter(Program.broadcast_id == broadcast_id).all()
    else:
        schedule = []
    programs_json = []
    for item in schedule:
        programs_json.append({
            'title': item.title,
            'hosts': item.hosts,
            'time': item.time
        })
    emit('new_schedule', programs_json)

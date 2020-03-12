from mors_module import application, socketio
from mors_module.currently_playing import *
from mors_module.methods import *
from flask import render_template
from flask_socketio import emit
from datetime import datetime


@application.route('/')
@application.route('/index')
def index():
    cp_obj = CurrentlyPlaying()
    current_program = cp_obj.now_playing()
    broadcasts = Broadcast.query.all()
    b_cast_date = get_next_or_last_broadcast(datetime.today())
    schedule = get_schedule_by_date(b_cast_date)
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
    schedule = get_schedule_by_date(date_dt)
    emit('new_schedule', schedule)

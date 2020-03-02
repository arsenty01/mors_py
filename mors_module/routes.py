from mors_module import application, socketio
from mors_module import db
from mors_module.currently_playing import *
from mors_module.models import ChatMessages, Program, Broadcast
from flask import render_template
from flask_socketio import emit
from datetime import datetime


@application.route('/')
@application.route('/index')
def index():
    cp_obj = CurrentlyPlaying()
    current_program = cp_obj.now_playing()
    broadcasts = Broadcast.query.all()
    # todo костыль
    schedule = Program.query.filter(Broadcast.date == '26.01.2020').all()
    chat_messages = ChatMessages.query.order_by(ChatMessages.id.desc()).limit(20)

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
        'timestamp': msg.timestamp.strftime("%d.%m.%Y, %H:%M:%S")
    }, broadcast=True)


@socketio.on('cp_request')
def currently_playing():
    cp_obj = CurrentlyPlaying()
    emit('cp_response', cp_obj.now_playing())


@socketio.on('refresh_schedule')
def refresh_schedule(date):
    broadcast = Broadcast.query.filter(Broadcast.date == date).first().id
    schedule = Program.query.filter(Program.broadcast_id == broadcast).all()
    print(schedule)
    programs_json = []
    for item in schedule:
        programs_json.append({
            'title': item.title,
            'hosts': item.hosts,
            'time': item.time
        })
    emit('new_schedule', programs_json)

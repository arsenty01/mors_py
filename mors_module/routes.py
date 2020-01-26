from mors_module import app, db
from mors_module.currently_playing import *
from mors_module.models import ChatMessages, Program, Broadcast
from flask import render_template
from flask_socketio import SocketIO, emit
from datetime import datetime
import time
socketio = SocketIO(app)


@app.route('/')
@app.route('/index')
def index():

    current_program = CurrentlyPlaying.now_playing()
    broadcasts = Broadcast.query.all()
    schedule = Program.query.filter(Broadcast.date == '26.01.2020').all()
    chat_messages = ChatMessages.query.order_by(ChatMessages.id.desc()).limit(20)

    return render_template('main_page.html',
                           schedule=schedule,
                           broadcasts=broadcasts,
                           version='20.11 (alpha)',
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
    while True:
        time.sleep(30)
        current_program = CurrentlyPlaying.now_playing()
        emit('cp_response', current_program)

from mors_module import app, db
from mors_module.models import Chat_messages
from flask import render_template
from flask_socketio import SocketIO, emit
from datetime import datetime

socketio = SocketIO(app)


@app.route('/')
@app.route('/index')
def index():

    schedule = [{
        "time": "12:00 - 13:00",
        "name": "Очень крутая передача",
        "guest": "Крутой гость"
    }]

    news = [{
        "title": "Тестовый заголовок",
        "shortcut": "Тестовый шорткат",
        "img": "news.jpeg"
    }]

    current_program = {
        "name": "Тестовая передача",
        "time": "12:00 - 13:00"
    }

    menu_items = [
        ("команда", "team/"),
        ("фотогалерея", "gallery/"),
        ("архив новостей", "archive/"),
        ("архив записей", "programs/")
    ]

    return render_template('content.html', schedule=schedule,
                           news=news, version='19.71 (inside)', current_program=current_program)


@socketio.on('sent_message')
def get_messages(message):
    msg = Chat_messages(**message, timestamp=datetime.today())
    db.session.add(msg)
    db.session.commit()
    msgs = Chat_messages.query.order_by(Chat_messages.timestamp.desc()).limit(20)
    msgs_for_json = []
    for msg in msgs:
        msgn = {
            "author": msg.author,
            "text": msg.text,
            "timestamp": msg.timestamp.strftime("%m/%d/%Y, %H:%M:%S")
        }
        msgs_for_json.append(msgn)
    print(msgs_for_json)
    emit('messages_list', {'messages': msgs_for_json}, broadcast=True)


@socketio.on('mybroadcast')
def get_messages(message):
    emit('my response', {'data': message['data']}, broadcast=True)


@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected'})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')
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

    chat_messages = Chat_messages.query.order_by(Chat_messages.id.desc()).limit(20)
    # db.session.execute('''DELETE FROM chat_messages''')
    # db.session.commit()

    return render_template('content.html',
                           schedule=schedule,
                           news=news,
                           version='19.71 (inside)',
                           current_program=current_program,
                           chat_messages=chat_messages)


@socketio.on('sent_message')
def get_messages(message):
    msg = Chat_messages(**message, timestamp=datetime.today())
    db.session.add(msg)
    db.session.commit()
    print(msg)
    emit('new_message',
         {'author': message['author'], 'text': message['text'], 'timestamp': msg.timestamp.strftime("%d.%m.%Y, %H:%M:%S")},
         broadcast=True)
from mors_module import app, db
from mors_module.models import Chat_messages
from flask import render_template
from flask_socketio import SocketIO, emit
from datetime import datetime

socketio = SocketIO(app)


@app.route('/')
@app.route('/index')
def index():

    schedule_date = datetime.today().strftime("%d.%m.%Y")

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

    return render_template('base_template.html',
                           schedule=schedule,
                           schedule_date=schedule_date,
                           news=news,
                           version='19.81 (inside)',
                           current_program=current_program,
                           chat_messages=chat_messages)


@app.route('/admin')
def admin():
    return render_template('admin.html')


@socketio.on('sent_message')
def get_messages(message):
    msg = Chat_messages(**message, timestamp=datetime.today())
    db.session.add(msg)
    db.session.commit()
    emit('new_message',
         {'author': message['author'], 'text': message['text'], 'timestamp': msg.timestamp.strftime("%d.%m.%Y, %H:%M:%S")},
         broadcast=True)
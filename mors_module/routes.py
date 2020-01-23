from mors_module import app, db
from mors_module.models import Chat_messages
from flask import render_template
from flask_socketio import SocketIO, emit
from datetime import datetime
socketio = SocketIO(app)


@app.route('/')
@app.route('/index')
def index():

    schedule = [
        {
            "time": "12:00 - 12:50",
            "name": "Новости",
            "guest": "Андрей Шарыгин и Дима Яснов"
        }, {
            "time": "12:55 - 13:10",
            "name": "Гороскоп",
            "guest": "Яна Смолина"
        }, {
            "time": "13:15 - 14:15",
            "name": "В тренде",
            "guest": "Максим Поправко и Руслан Нагатов"
        }, {
            "time": "14:20 - 15:00",
            "name": "Звук Жив",
            "guest": "HARDBALLS"
        }, {
            "time": "15:05 - 15:40",
            "name": "Спорт",
            "guest": "Андрей Галкин и Flying disk"
        }, {
            "time": "15:45 - 16:20",
            "name": "В гостях",
            "guest": "проект 'Лёд для всех'"
        }
    ]

    news = [{
        "title": "Тестовый заголовок",
        "shortcut": "Тестовый шорткат",
        "img": "news.jpeg"
    }]

    current_program = {
        "name": "Просто музыка",
        "time": "до следующего эфира"
    }

    menu_items = [

    ]

    broadcasts = [
        "26.01.2020"
    ]

    chat_messages = Chat_messages.query.order_by(Chat_messages.id.desc()).limit(20)
    # db.session.execute('''DELETE FROM chat_messages''')
    # db.session.commit()

    return render_template('main_page.html',
                           schedule=schedule,
                           news=news,
                           broadcasts=broadcasts,
                           version='20.11 (alpha)',
                           current_program=current_program,
                           chat_messages=chat_messages,
                           menu_items=menu_items)

@app.route('/super-secret-admin')
def admin():
    chat_messages = Chat_messages.query.order_by(Chat_messages.id.desc()).limit(100)

    schedule = [
        {
            "time": "12:00 - 12:50",
            "name": "Новости",
            "guest": "Андрей Шарыгин и Дима Яснов"
        }, {
            "time": "12:55 - 13:10",
            "name": "Гороскоп",
            "guest": "Яна Смолина"
        }, {
            "time": "13:15 - 14:15",
            "name": "В тренде",
            "guest": "Максим Поправко и Руслан Нагатов"
        }, {
            "time": "14:20 - 15:00",
            "name": "Звук Жив",
            "guest": "HARDBALLS"
        }, {
            "time": "15:05 - 15:40",
            "name": "Спорт",
            "guest": "Андрей Галкин и Flying disk"
        }, {
            "time": "15:45 - 16:20",
            "name": "В гостях",
            "guest": "проект 'Лёд для всех'"
        }
    ]

    broadcasts = [
        "26.01.2020"
    ]

    return render_template('admin.html',
                           chat_messages=chat_messages,
                           deletion=True,
                           version='20.11 (alpha)',
                           schedule=schedule,
                           broadcasts=broadcasts)

@socketio.on('sent_message')
def get_messages(message):
    msg = Chat_messages(**message, timestamp=datetime.today())
    db.session.add(msg)
    db.session.commit()
    emit('new_message', {
        'author': message['author'],
        'text': message['text'],
        'timestamp': msg.timestamp.strftime("%d.%m.%Y, %H:%M:%S")
    }, broadcast=True)
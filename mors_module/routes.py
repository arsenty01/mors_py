from mors_module import app, db
from mors_module.models import ChatMessages, Program, Broadcast
from flask import render_template
from flask_socketio import SocketIO, emit
from datetime import datetime
from mors_module.db_dispatcher import get_schedule
socketio = SocketIO(app)


@app.route('/')
@app.route('/index')
def index():

    broadcasts = map(lambda res: res.date.strftime('%d.%m.%Y'), db.session.query(Broadcast.date))

    schedule = get_schedule('26.01.2020')
    print(schedule)
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

    # some_broadcast = Broadcast(**{'date': datetime.strptime('26.01.2020', '%d.%m.%Y')})
    # db.session.add(some_broadcast)
    # some_broadcast = Broadcast(**{'date': datetime.strptime('02.02.2020', '%d.%m.%Y')})
    # db.session.add(some_broadcast)
    # broadcast_id = list(map(lambda x: x.id, db.session.query(Broadcast.id).filter(Broadcast.date == datetime.strptime('26.01.2020', '%d.%m.%Y'))))[0]
    # print(broadcast_id)
    # some_program = Program(**{'broadcast_id':broadcast_id,
    #                           "time": "12:00 - 12:50",
    #                           "title": "Новости",
    #                           "hosts": "Андрей Шарыгин и Дима Яснов"})
    # db.session.add(some_program)
    # some_program = Program(**{'broadcast_id':broadcast_id,
    #                           "time": "12:55 - 13:10",
    #                           "title": "Гороскоп",
    #                           "hosts": "Яна Смолина"})
    # db.session.add(some_program)
    # some_program = Program(**{'broadcast_id':broadcast_id,
    #                           "time": "13:15 - 14:15",
    #                           "title": "В тренде",
    #                           "hosts": "Максим Поправко и Руслан Нагатов"
    #                           })
    # db.session.add(some_program)
    # some_program = Program(**{'broadcast_id':broadcast_id,
    #                           "time": "14:20 - 15:00",
    #                           "title": "Звук Жив",
    #                           "hosts": "HARDBALLS"
    #                           })
    # db.session.add(some_program)
    # some_program = Program(**{'broadcast_id':broadcast_id,
    #                           "time": "15:05 - 15:40",
    #                           "title": "Спорт",
    #                           "hosts": "Андрей Галкин и Flying disk"
    #                           })
    # db.session.add(some_program)
    # some_program = Program(**{'broadcast_id':broadcast_id,
    #                           "time": "15:45 - 16:20",
    #                           "title": "В гостях",
    #                           "hosts": "проект 'Лёд для всех'"
    #                           })
    # db.session.add(some_program)
    # db.session.commit()


    chat_messages = ChatMessages.query.order_by(ChatMessages.id.desc()).limit(20)
    # db.session.execute('''DELETE FROM chat_messages''')
    # db.session.commit()


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
    chat_messages = ChatMessages.query.order_by(ChatMessages.id.desc()).limit(100)
    # schedule = Program.query.filter_(date=)


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
    msg = ChatMessages(**message, timestamp=datetime.today())
    db.session.add(msg)
    db.session.commit()
    emit('new_message', {
        'author': message['author'],
        'text': message['text'],
        'timestamp': msg.timestamp.strftime("%d.%m.%Y, %H:%M:%S")
    }, broadcast=True)


# @socketio.on('get_schedule')
# def get_schedule(date):
#     broadcast_id = list(map(lambda x: x.id, db.session.query(Broadcast.id).filter(Broadcast.date == datetime.strptime(date, '%d.%m.%Y'))))[0]


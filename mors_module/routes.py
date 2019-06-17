from mors_module import app
from flask import render_template


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
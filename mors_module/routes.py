import flask
from flask_login import login_user, current_user, logout_user
from werkzeug.utils import redirect

from mors_module import application, socketio, db, login_manager
from mors_module.currently_playing import *
from mors_module.forms import LoginForm
from mors_module.models import ChatMessages, Program, Broadcast, User
from flask import render_template, url_for, flash
from flask_socketio import emit
from datetime import datetime

# Стандартные роуты
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
                           version='20.03.1 (alpha)',
                           chat_messages=chat_messages,
                           menu_items=[('Войти', '/login')],
                           current_program=current_program)


# Специфичные роуты
@application.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неверное имя пользователя или пароль')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Вход', form=form)


@application.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# Обработчики сокетов
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

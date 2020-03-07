from flask import Flask
from mors_module.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_login import LoginManager

application = Flask(__name__)
application.config.from_object(Config)
login_manager = LoginManager(application)
db = SQLAlchemy(application)
migrate = Migrate(application, db)
socketio = SocketIO(application)

from mors_module import routes, models

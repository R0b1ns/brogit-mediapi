from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_wtf import CSRFProtect
from flask_babel import Babel

socketio = SocketIO()
login_manager = LoginManager()
csrf = CSRFProtect()
babel = Babel()
from flask_limiter.util import get_remote_address
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_wtf import CSRFProtect
from flask_babel import Babel
from flask_limiter import Limiter

socketio = SocketIO()
login_manager = LoginManager()
limiter = Limiter(get_remote_address)
csrf = CSRFProtect()
babel = Babel()

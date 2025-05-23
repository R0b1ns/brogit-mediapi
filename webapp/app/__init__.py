import os
import time
import unicodedata
from http import HTTPStatus
from urllib.parse import urlparse

from flask import Flask
from flask_cors import CORS

from app.config import register_modules
from app.core.locale.models import get_locale, get_timezone
from app.lib.common import setup_logging


def create_app():
    app = Flask(__name__)

    # TODO: Replace key with something from config
    app.secret_key = 'your_secret_key'

    app.config['DEBUG'] = True
    app.config['PROPAGATE_EXCEPTIONS'] = True

    # Flask-Babel config
    # Supported languages
    app.config['LANGUAGES'] = ['en', 'de']
    app.config['BABEL_DEFAULT_LOCALE'] = 'en'
    # base_dir = os.path.abspath(os.path.dirname(__file__))
    # app.config['BABEL_TRANSLATION_DIRECTORIES'] = os.path.join(base_dir, "translations")
    # https://python-babel.github.io/flask-babel/
    # TODO: Load config from config file
    # BABEL_TRANSLATION_DIRECTORIES=/path/to/translations;/another/path/
    # BABEL_DOMAIN=messages;myapp

    # Basic Logging configuration
    # setup_logging()

    from app.extensions import csrf, babel, socketio, login_manager, limiter

    # Init Extensions
    socketio.init_app(app)
    csrf.init_app(app)
    babel.init_app(app, locale_selector=get_locale, timezone_selector=get_timezone, default_locale='en', default_domain='messages', default_translation_directories='translations')
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    limiter.init_app(app)
    CORS(app, resources={r"/": {"origins": "*"}})

    # Load backend
    register_modules()

    with app.app_context():
        from app.core.auth import auth_bp
        from app.core.main import main_bp

        app.register_blueprint(auth_bp)
        app.register_blueprint(main_bp)

        return app, socketio
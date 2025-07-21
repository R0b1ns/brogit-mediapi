import logging
import os
import socket
import time
import unicodedata
from http import HTTPStatus
from urllib.parse import urlparse

from flask import Flask
from flask_cors import CORS

from app.extensions import migrate, bcrypt
from app.module_init import register_modules
from app.core.locale.models import get_locale, get_timezone
from app.lib.common import setup_logging
from app.lib.config_management import load_config


def create_app():
    app = Flask(__name__)

    # TODO: Config
    # TODO: Better solution for path resolve
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    os.chdir(PROJECT_ROOT)

    env_path = os.path.join(PROJECT_ROOT, '.env')
    config = load_config(env_path, 'CONFIG_FILE')

    cors_allowed_origins = [
        f"{ 'https' if config['app']['SSL_ENABLED'] else 'http' }://localhost:{config['app']['PORT']}",
        # Add config from nginx or hostname
        f"https://{ socket.gethostname() }" if config['environment']['NGINX_HOST'] == "default" else config['environment']['NGINX_HOST']
    ]

    config['app']['ALLOWED_ORIGINS'] = cors_allowed_origins
    app.config.update(config['app'])
    app.secret_key = config['app'].get('SECRET_KEY', 'your_secret_key')

    log_level = {
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'debug': logging.DEBUG
    }

    # Basic Logging configuration
    setup_logging(log_level.get(config['app'].get('LOGGING', 'info'), logging.INFO))

    logging.info(f"Cors Allowed Origins: { cors_allowed_origins }")

    from app.extensions import csrf, babel, socketio, login_manager, limiter

    # Init Extensions
    socketio.init_app(app, cors_allowed_origins=cors_allowed_origins)
    csrf.init_app(app)
    babel.init_app(app, locale_selector=get_locale, timezone_selector=get_timezone)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.session_protection = "strong"
    login_manager.login_message_category = "info"
    limiter.init_app(app)
    migrate.init_app(app)
    bcrypt.init_app(app)
    CORS(app, resources={r"/": {"origins": cors_allowed_origins}})

    # Load modules
    register_modules(app, config)

    with app.app_context():
        from app.core.auth import auth_bp
        from app.core.main import main_bp
        from app.core.api import api_bp

        app.register_blueprint(auth_bp)
        app.register_blueprint(main_bp)
        app.register_blueprint(api_bp)

        return app, socketio
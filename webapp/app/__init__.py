import os
import time
import unicodedata
from http import HTTPStatus
from urllib.parse import urlparse

from flask import Flask, render_template, session, request, jsonify, redirect, flash, url_for, abort, \
    send_from_directory
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_socketio import SocketIO, emit
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from app.config import register_modules
from app.lib.common import setup_logging


def create_app():
    app = Flask(__name__)

    # TODO: Replace key with something from config
    app.secret_key = 'your_secret_key'

    from app.extensions import csrf, babel, socketio, login_manager

    # Init Extensions
    socketio.init_app(app)
    csrf.init_app(app)
    babel.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    CORS(app, resources={r"/": {"origins": "*"}})

    # Konfiguration von Flask-Babel
    app.config['LANGUAGES'] = ['en', 'de']  # Beispiel für unterstützte Sprachen
    app.config['BABEL_DEFAULT_LOCALE'] = 'en'
    # https://python-babel.github.io/flask-babel/
    # Load config from config file
    # BABEL_TRANSLATION_DIRECTORIES=/path/to/translations;/another/path/
    # BABEL_DOMAIN=messages;myapp

    # from webapp.app.config import register_modules
    # from webapp.app.core.auth import auth_bp
    # from webapp.app.core.auth.models import User
    # from webapp.app.core.auth.routes import login
    # from webapp.app.core.main import main_bp
    # from webapp.app.lib.Backend import Backend
    # from webapp.app.lib.common import setup_logging
    #
    # from webapp.app.lib.django_utils_http_partly import url_has_allowed_host_and_scheme
    # from webapp.app.lib.pam import verify_user
    # from webapp.app.lib.wifi import WifiHelper

    #
    # limiter = Limiter(
    #     get_remote_address,
    #     app=app
    # )

    # Basic Logging configuration
    # setup_logging()

    # Load backend
    register_modules()

    from app.core.auth import auth_bp
    from app.core.main import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app, socketio





#
#
# if __name__ == '__main__':
#     socketio.run(app, host='0.0.0.0', port=80, debug=True, allow_unsafe_werkzeug=True)

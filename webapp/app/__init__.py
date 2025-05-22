import os
import time
import unicodedata
from http import HTTPStatus
from urllib.parse import urlparse

from flask import Flask, render_template, session, request, jsonify, redirect, flash, url_for, abort, \
    send_from_directory
from flask_cors import CORS

from app.config import register_modules
from app.lib.common import setup_logging


def create_app():
    app = Flask(__name__)

    # TODO: Replace key with something from config
    app.secret_key = 'your_secret_key'

    from app.extensions import csrf, babel, socketio, login_manager, limiter

    # Init Extensions
    socketio.init_app(app)
    csrf.init_app(app)
    babel.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    limiter.init_app(app)
    CORS(app, resources={r"/": {"origins": "*"}})

    # Konfiguration von Flask-Babel
    app.config['LANGUAGES'] = ['en', 'de']  # Beispiel für unterstützte Sprachen
    app.config['BABEL_DEFAULT_LOCALE'] = 'en'
    # https://python-babel.github.io/flask-babel/
    # Load config from config file
    # BABEL_TRANSLATION_DIRECTORIES=/path/to/translations;/another/path/
    # BABEL_DOMAIN=messages;myapp

    # Basic Logging configuration
    # setup_logging()

    # Load backend
    register_modules()

    from app.core.auth import auth_bp
    from app.core.main import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app, socketio

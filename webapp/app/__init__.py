import socket
import time
import unicodedata
from http import HTTPStatus
from urllib.parse import urlparse

from flask import Flask, render_template, session, request, jsonify, redirect, flash, url_for, abort
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_socketio import SocketIO, emit
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from app.lib.wifi import scan_wifi, connect_to_wifi
from wtforms.fields.simple import PasswordField, BooleanField, SubmitField, EmailField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email
from flask_wtf.csrf import CSRFProtect

from app.lib.django_utils_http_partly import url_has_allowed_host_and_scheme

from app.extensions import csrf

app = Flask(__name__)
app.secret_key = 'your_secret_key'
socketio = SocketIO(app)
CORS(app, resources={r"/": {"origins": "*"}})

csrf.init_app(app)

limiter = Limiter(
    get_remote_address,
    app=app
)

app.secret_key = 'your_secret_key'  # Ersetze 'your_secret_key' durch einen sicheren Wert

# Flask-Login einrichten
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# Benutzerklasse für einen einzelnen Benutzer
class User(UserMixin):
    id = "1"  # Feste Benutzer-ID


class LoginForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    def validate(self, extra_validators=None):
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False

        if self.password.data != "112358":
            return False
        # user = User.query.filter_by(email=self.email.data).first()
        # if not user:
        #     self.email.errors.append('Unknown email')
        #     return False
        # if not user.verify_password(self.password.data):
        #     self.password.errors.append('Invalid password')
        #     return False
        return True


@login_manager.unauthorized_handler
def unauthorized():
    if request.blueprint == 'api':
        abort(HTTPStatus.UNAUTHORIZED)
    return redirect(url_for('site.login'))


@login_manager.user_loader
def load_user(user_id):
    if user_id == User.id:
        return User()
    return None


@app.route('/hotspot-detect.html')
def hotspot_detect():
    return index()


@app.route('/')
def index():
    if not current_user.is_authenticated:
        return login()

    hostname = socket.getfqdn()
    return render_template('index.html', hostname="http://{}".format(socket.gethostname()))


@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per hour")
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        user = User()
        # user should be an instance of your `User` class
        login_user(user)

        flash('Logged in successfully.')

        next_url = request.args.get('next')
        # url_has_allowed_host_and_scheme should check if the url is safe
        # for redirects, meaning it matches the request host.
        # See Django's url_has_allowed_host_and_scheme for an example.
        if next_url and not url_has_allowed_host_and_scheme(next_url, request.host):
            return abort(400)

        return redirect(next_url or url_for('index'))
    return render_template('login.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/settings")
@login_required
def settings():
    pass


@socketio.on('request_wifi')
def handle_request_wifi():
    networks = scan_wifi()
    emit('response_wifi', {'networks': networks})


@app.route('/api/connect', methods=['GET'])
def connect_to_network():
    ssid = request.args.get('ssid')
    password = request.args.get('password')

    if not ssid:
        return jsonify({"error": "SSID is required"}), 400

    try:
        connect_to_wifi(ssid, password)
        return jsonify({"message": f"Connected to {ssid}"}), 200
    except Exception as e:
        print(e)

        return jsonify({"message": str(e)}), 500


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=80, debug=True, allow_unsafe_werkzeug=True)

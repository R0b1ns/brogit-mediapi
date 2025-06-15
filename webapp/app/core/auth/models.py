import json
import logging
from http import HTTPStatus

from flask import request, abort, redirect, url_for, current_app, session
from flask_babel import _
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms.fields.simple import PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired

from app.extensions import login_manager

class User(UserMixin):
    def __init__(self, username: str):
        self.username = username
        # TODO: Implement this on a better way
        self.locale = 'default'
        self.timezone = 'UTC+2'
        # self.__load_config()

    def get_id(self):
        return self.username

    def update_locale(self, locale):
        if (locale not in current_app.config.get('LANGUAGES')) and (locale != 'default'):
            return False

        self.locale = locale
        session['user'] = self.to_dict()
        return self.locale

    def to_dict(self):
        return {
            k: v for k, v in self.__dict__.items()
            if not k.startswith('_') and not callable(v)
        }

    @classmethod
    def from_dict(cls, user_id, data):
        obj = cls(user_id)
        for key, value in data.items():
            setattr(obj, key, value)
        return obj

class LoginForm(FlaskForm):
    username = StringField(_('Username'))
    password = PasswordField(_('Password'), validators=[DataRequired()])
    submit = SubmitField(_('Log In'))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    def validate(self, extra_validators=None):
        initial_validation = super(LoginForm, self).validate()
        # if not initial_validation:
        #     return False

        return initial_validation

        # TODO: No credential check here. Here just validate. Maybe if policy is archived etc.
        # if verify_user(self.username.data, self.password.data):
        #     return True
        # else:
        #     flash('Invalid credentials')

        # TODO: Find out how we can append an error to an field
        # -> make it to self   => username.append('Test')
        # user = User.query.filter_by(email=self.email.data).first()
        # if not user:
        #     self.email.errors.append('Unknown email')
        #     return False
        # if not user.verify_password(self.password.data):
        #     self.password.errors.append('Invalid password')
        #     return False
        # return False

@login_manager.user_loader
def load_user(user_id):
    logging.debug("load_user: "+user_id)
    user_data = session.get('user')
    if user_data:
        return User.from_dict(user_id, user_data)
    return User(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    if request.blueprint == 'api':
        abort(HTTPStatus.UNAUTHORIZED)
    return redirect(url_for('site.login'))
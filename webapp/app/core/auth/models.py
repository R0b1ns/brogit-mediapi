from http import HTTPStatus

from flask import flash, request, abort, redirect, url_for
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms.fields.simple import PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired

from app.extensions import login_manager
from app.lib.pam import verify_user


class User(UserMixin):
    def __init__(self, username: str):
        self.username = username
        # TODO: Implement this on a better way
        self.locale = 'en'
        self.timezone = 'UTC+2'

    def get_id(self):
        return self.username

class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

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
    return User(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    if request.blueprint == 'api':
        abort(HTTPStatus.UNAUTHORIZED)
    return redirect(url_for('site.login'))
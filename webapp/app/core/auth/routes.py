import json

from flask import redirect, url_for, request, abort, render_template, flash, g, session
from flask_login import login_required, logout_user, login_user
from flask_babel import _

from app.core.auth import auth_bp
from app.core.auth.models import User, LoginForm
from app.extensions import limiter
from app.lib.django_utils_http_partly import url_has_allowed_host_and_scheme
from app.lib.pam import verify_user


@auth_bp.route('/login', methods=['GET', 'POST'])
# TODO: Bug here. We do not want to prevent to open up login page 10 per hour, but we want to prevent 10 logins
@limiter.limit("10 per hour")
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if verify_user(username, password):
            user = User(username)
            login_user(user)
            # g.user is only for this one request
            # g.user = user
            session['user'] = user.to_dict()
            # TODO: Log the login to logfile
        else:
            flash(_('Invalid credentials.'))

        next_url = request.args.get('next')
        # url_has_allowed_host_and_scheme should check if the url is safe
        # for redirects, meaning it matches the request host.
        # See Django's url_has_allowed_host_and_scheme for an example.
        if next_url and not url_has_allowed_host_and_scheme(next_url, request.host):
            return abort(400)

        return redirect(next_url or url_for('main.index'))

    return render_template('login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth_bp.route('/change-password')
def change_password():
    pass
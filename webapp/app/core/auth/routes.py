from flask import redirect, url_for, request, abort, render_template
from flask_login import login_required, logout_user, login_user

from app.core.auth import auth_bp
from app.core.auth.models import User, LoginForm
from app.lib.django_utils_http_partly import url_has_allowed_host_and_scheme


@auth_bp.route('/login', methods=['GET', 'POST'])
# TODO: Bug here. We do not want to prevent to open up login page 10 per hour, but we want to prevent 10 logins
# @limiter.limit("10 per hour")
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

        # TODO: Do not flash. Log the login to logfile
        # flash('Logged in successfully.')

        next_url = request.args.get('next')
        # url_has_allowed_host_and_scheme should check if the url is safe
        # for redirects, meaning it matches the request host.
        # See Django's url_has_allowed_host_and_scheme for an example.
        if next_url and not url_has_allowed_host_and_scheme(next_url, request.host):
            return abort(400)

        return redirect(next_url or url_for('index'))
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('core.auth.login'))
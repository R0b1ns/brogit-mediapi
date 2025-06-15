import logging

from flask import current_app, request, g, has_request_context
from flask_login import current_user


# @babel.localeselector
def get_locale():
    default_locale = current_app.config.get('BABEL_DEFAULT_LOCALE', 'en')
    request_context_locale = None

    # if a user is logged in, use the locale from the user settings
    # user = getattr(g, 'user', None)
    # if user is not None:
    #     print(f"get_locale: User context = {user.locale}")
    #     return user.locale
    # otherwise try to guess the language from the user accept
    # header the browser transmits. The best match wins.

    # TODO: This locale selector works not as intended. It should get executed on every request.
    #  But it does only once before request context
    #  It will get fired on every request if _() is used in the request, but not for templates
    if has_request_context():
        request_context_locale = request.accept_languages.best_match(current_app.config['LANGUAGES'])

    if current_user:
        logging.debug(f"get_locale: User context = {current_user.locale}")
        if current_user.locale == 'default':
            return request_context_locale or default_locale
        return current_user.locale

    if request_context_locale:
        logging.debug(f"get_locale: Request context = {request_context_locale}")
        return request_context_locale

    logging.debug(f"get_locale: Default = {default_locale}")
    return default_locale

def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone

    return None
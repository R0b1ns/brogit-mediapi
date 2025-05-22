from flask import current_app, request, g

from app.extensions import babel


# @babel.localeselector
def get_locale():
    # if a user is logged in, use the locale from the user settings
    user = getattr(g, 'user', None)
    if user is not None:
        return user.locale
    # otherwise try to guess the language from the user accept
    # header the browser transmits. The best match wins.
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])

def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone

    return None
from flask import current_app, request, g, has_request_context


# @babel.localeselector
def get_locale():
    print("get_locale")
    # if a user is logged in, use the locale from the user settings
    user = getattr(g, 'user', None)
    if user is not None:
        return user.locale
    # otherwise try to guess the language from the user accept
    # header the browser transmits. The best match wins.

    # TODO: This locale selector works not as intended. It should get executed on every request.
    #  But it does only once before request context
    #  It will get fired on every request if _() is used in the request, but not for templates
    if has_request_context():
        print("Request context")
        return request.accept_languages.best_match(current_app.config['LANGUAGES'])
    # return 'en'
    return 'de'

def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone

    return None
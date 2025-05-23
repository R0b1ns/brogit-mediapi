# Start

gunicorn app:app -b localhost:80 &

# Getting started

## Password

# Multi-Language (babel)

pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot .
pybabel init -i messages.pot -d translations -l de
pybabel compile -d translations
pybabel update -i messages.pot -d translations


## Benutze eine benutzerdefinierte Domain
    greeting = _('Hello', domain='custom_translations')
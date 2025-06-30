# Start

gunicorn app:app -b localhost:80 &

# Getting started

## Password

# Multi-Language (babel)

## Extract. You always will do when you update
pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot .

## If its new, then init. Otherwise, skip
pybabel init -i messages.pot -d translations -l de

## Not new, then update everytime
pybabel update -i messages.pot -d translations

## You are done with your translatons. At least compile
pybabel compile -d translations



## Benutze eine benutzerdefinierte Domain
    greeting = _('Hello', domain='custom_translations')
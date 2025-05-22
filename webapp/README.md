# Start

gunicorn app:app -b localhost:80 &

# Getting started

## Password

# Multi-Language

translations/de/LC_MESSAGES/messages.po

    # Erstellen einer PO-Datei (Beispiel)
    pybabel init -i messages.pot -d translations -l de


~~msgid "Welcome"
msgstr "Willkommen"

msgid "This is a multilingual Flask web application."
msgstr "Dies ist eine mehrsprachige Flask-Webanwendung."~~


pybabel compile -d translations


# Benutze eine benutzerdefinierte Domain
    greeting = _('Hello', domain='custom_translations')


# @app.route('/change_language', methods=['POST'])
# def change_language():
#     language = request.json.get('language')
#     if language in app.config['LANGUAGES']:
#         # Setze die Sprache (dies könnte auch in einer Session gespeichert werden)
#         app.config['BABEL_DEFAULT_LOCALE'] = language
#         return jsonify({'message': 'Sprache geändert'}), 200
#     return jsonify({'message': 'Ungültige Sprache'}), 400
#
#
# @app.route('/get_translations', methods=['GET'])
# def get_translations():
#     # Dynamisch alle übersetzbaren Texte vom Template sammeln
#     # Hier wäre eine Lösung, um alle gettext-Keys aufzulisten (z.B. durch Scannen von Templates)
#
#     # Beispiel: Stelle alle möglichen Strings in einem Dictionary zusammen
#     translations = {
#         'greeting': _('Willkommen'),
#         'description': _('Dies ist eine mehrsprachige Flask-Webanwendung.')
#     }
#
#     # Wenn du dynamische Texte hast, die sich im Code befinden, kannst du sie hier anfügen
#     # Dies könnte auch über bestimmte Regeln oder Muster geschehen, um das gesamte HTML-Template dynamisch zu scannen
#     return jsonify(translations)
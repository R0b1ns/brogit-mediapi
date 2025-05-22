import os

from flask import send_from_directory, current_app, render_template, request, jsonify, flash
from flask_login import login_required, current_user
from flask_socketio import emit

from app.core.auth.routes import login
from app.core.main import main_bp
from app.extensions import socketio
from app.lib.Backend import Backend
from app.lib.wifi import WifiHelper


@main_bp.route('/')
def index():
    print(current_user.is_authenticated)
    if not current_user.is_authenticated:
        return login()

    # hostname = socket.getfqdn()
    return render_template('index.html', hostname=Backend().system.get_hostname(), backend=Backend())

@main_bp.route('/hotspot-detect.html')
def hotspot_detect():
    return index()

@main_bp.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# TODO: Move that route
@main_bp.route('/api/connect', methods=['GET'])
def connect_to_network():
    ssid = request.args.get('ssid')
    password = request.args.get('password')

    if not ssid:
        return jsonify({"error": "SSID is required"}), 400

    try:
        WifiHelper.get_instance().connect(ssid, password)
        return jsonify({"message": f"Connected to {ssid}"}), 200
    except Exception as e:
        flash("It was unable to connect to the new network. Please check your credentials")
        return jsonify({"message": str(e)}), 500

# TODO: Move that route
@main_bp.route("/settings")
@login_required
def settings():
    pass

# TODO: Move that route
@socketio.on('request_wifi')
def handle_request_wifi():
    networks = WifiHelper.get_instance().scan()
    emit('response_wifi', {'networks': networks})

# # @babel.localeselector
# # def get_locale():
# #     # return session.get('lang', 'en')
# #     return request.accept_languages.best_match(app.config['LANGUAGES'])
#
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
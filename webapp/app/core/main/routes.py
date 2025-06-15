import os

from flask import send_from_directory, current_app, render_template, request, jsonify, flash
from flask_login import login_required, current_user
from flask_socketio import emit
from flask_babel import _, lazy_gettext

from app.core.auth.routes import login
from app.core.main import main_bp
from app.extensions import socketio
from app.lib.Backend import Backend
from app.lib.wifi import WifiHelper


@main_bp.route('/')
def index():
    if not current_user.is_authenticated:
        return login()

    modules = []
    for name in Backend().list_modules():
        info = Backend().get(name).get_info()
        modules.append(info)

    # hostname = socket.getfqdn()
    return render_template('index.html', hostname=Backend().system.get_hostname(), backend=Backend(), modules=modules, languages=current_app.config['LANGUAGES'])

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
        return jsonify({"error": _("SSID is required")}), 400

    try:
        WifiHelper.get_instance().connect(ssid, password)
        return jsonify({"message": _(f"Connected to %(value)", ssid)}), 200
    except Exception as e:
        flash(_("It was unable to connect to the new network. Please check your credentials"))
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

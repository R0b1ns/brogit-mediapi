import time

from flask import jsonify, request, abort, current_app
from flask_login import current_user

from app.core.api import api_bp
from app.lib.Backend import Backend
from app.lib.ssl_gen import validate_and_update_ssl_certificate


@api_bp.route('/settings/<section>', methods=['GET'])
def get_settings(section):
    module = Backend().get(section)
    if not module:
        return jsonify({"error": "Unknown section"}), 404
    return jsonify(module.get_settings())

@api_bp.route('/settings/<section>', methods=['POST'])
def update_settings(section):
    module = Backend().get(section)
    if not module:
        return jsonify({"error": "Unknown section"}), 404
    try:
        success = module.set_settings(request.json or {})
        return jsonify({"success": success})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/settings/<section>/<action>', methods=['POST'])
def call_action(section, action):
    module = Backend().get(section)
    if not module:
        return jsonify({"error": "Unknown section"}), 404
    method = getattr(module, f"action_{action}", None)
    if not callable(method):
        return jsonify({"error": f"Unknown action: {action}"}), 404
    try:
        result = method(request.json or {})
        return jsonify({"success": True, "result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# TODO: Move that routes to a dedicated general route file


@api_bp.route('/settings/general', methods=['GET'])
def get_settings_general():
    if not request.is_json:
        abort(400, description="Request must be JSON")

    data = request.get_json()

    if 'language' in data:
        value = data['language']
        return jsonify(message=f"Received language: {value}")

    if 'hostname' in data:
        value = data['name']
        return jsonify(message=f"Received name: {value}")

    return jsonify(message="Not implemented"), 404

@api_bp.route('/settings/general/language', methods=['POST'])
def update_settings_general_language():
    data = request.get_json()
    language = data.get('language')

    if not language:
        return jsonify(message="Missing fields"), 400

    if not current_user.update_locale(language):
        # TODO: Update bad response
        return jsonify(message="Unknown language"), 400

    return jsonify(message=f"Updated language: {language}")

@api_bp.route('/settings/general/hostname', methods=['POST'])
def update_settings_general_hostname():
    data = request.get_json()

    hostname = data.get('hostname')

    if not hostname:
        return jsonify(message="Missing fields"), 400

    print(hostname)
    time.sleep(1)

    # return jsonify(message=f"Changed Hostname to: {hostname}")
    return jsonify(message="Not implemented"), 404

@api_bp.route('/settings/general/certificate', methods=['POST'])
def update_settings_general_certificate():
    data = request.get_json()
    publickey = data.get('publickey')
    privatekey = data.get('privatekey')

    if not publickey or not privatekey:
        return jsonify({'error': 'Both publickey and privatekey are required'}), 400

    cert_path = current_app.config['SSL_CERT_PATH']
    key_path = current_app.config['SSL_KEY_PATH']

    try:
        success = validate_and_update_ssl_certificate(publickey, privatekey, cert_path, key_path)
    except Exception as e:
        return jsonify({'error': e}), 400

    if not success:
        return jsonify({'error': 'Updating SSL configuration was not successful out of unknown reason'}), 400

    return jsonify({'success': True}), 200

@api_bp.route('/settings/general/certificate/restore', methods=['POST'])
def update_settings_general_certificate_restore():
    # TODO
    return jsonify(message="Not implemented"), 404
from flask import jsonify, request, abort, current_app
from flask_login import current_user

from app.core.api import api_bp
from app.lib.Backend import Backend


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

    return jsonify({"error": "Not implemented"}), 404

@api_bp.route('/settings/general', methods=['POST'])
def update_settings_general():
    if not request.is_json:
        abort(400, description="Request must be JSON")

    data = request.get_json()

    if 'language' in data:
        value = data['language']

        if not current_user.update_locale(value):
            # TODO: Update bad response
            return jsonify({"error": "Unknown language"}), 400

        return jsonify(message=f"Updated language: {value}")

    if 'hostname' in data:
        value = data['name']
        return jsonify(message=f"Received name: {value}")

    return jsonify({"error": "Not implemented"}), 404
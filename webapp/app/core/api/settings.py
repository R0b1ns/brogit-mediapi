from flask import jsonify, request

from app.core.api import api
from app.lib.Backend import Backend


@api.route('/settings/<section>', methods=['GET'])
def get_settings(section):
    module = Backend().get(section)
    if not module:
        return jsonify({"error": "Unknown section"}), 404
    return jsonify(module.get_settings())

@api.route('/settings/<section>', methods=['POST'])
def update_settings(section):
    module = Backend().get(section)
    if not module:
        return jsonify({"error": "Unknown section"}), 404
    try:
        success = module.set_settings(request.json or {})
        return jsonify({"success": success})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route('/settings/<section>/<action>', methods=['POST'])
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

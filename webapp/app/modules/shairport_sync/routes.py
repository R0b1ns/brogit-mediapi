from flask import request, jsonify

from app.lib.Backend import Backend
from app.modules.shairport_sync import module_bp

@module_bp.route('/api/config', methods=['GET'])
def config():
    return jsonify(Backend().shairport_sync.get())

@module_bp.route('/api/enabled', methods=['POST'])
def install():
    data = request.get_json()

    enabled = data.get('enabled')

    if not isinstance(enabled, bool):
        return jsonify(error="Missing or invalid confirmation."), 400

    if enabled:
        try:
            Backend().shairport_sync.install(confirm=True)
        except Exception as e:
            return jsonify(error=f"Installation failed: {str(e)}"), 500
    else:
        try:
            Backend().shairport_sync.uninstall(confirm=True)
        except Exception as e:
            return jsonify(error=f"Uninstallation failed: {str(e)}"), 500

    return '', 200
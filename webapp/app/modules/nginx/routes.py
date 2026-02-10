from flask import request, jsonify, current_app

from app.lib.Backend import Backend
from app.modules.nginx import module_bp

@module_bp.route('/api/config', methods=['GET'])
def config():
    return jsonify(Backend().nginx.get())

@module_bp.route('/api/enabled', methods=['POST'])
def install():
    data = request.get_json()

    enabled = data.get('enabled')

    if enabled:
        try:
            Backend().nginx.install(confirm=True)
        except Exception as e:
            return jsonify(error=f"Installation failed: {str(e)}"), 500
    else:
        try:
            Backend().nginx.uninstall(confirm=True)
        except Exception as e:
            return jsonify(error=f"Uninstallation failed: {str(e)}"), 500

    return '', 200

@module_bp.route('/api/settings', methods=['POST'])
def change_nginx_settings():
    data = request.get_json()

    if not data:
        return jsonify(error="Request body is empty."), 400  # Bad Request

    # TODO: Add config for Update certificate

    current_app.logger.debug("Change nginx settings ...")

    # Backend().nginx.update_certificate(public_key, private_key)
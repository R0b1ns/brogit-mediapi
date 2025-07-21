from flask import request, jsonify, current_app

from app.lib.Backend import Backend
from app.modules.bluetooth import module_bp


@module_bp.route('/api/config', methods=['GET'])
def bluetooth_config():
    return jsonify(Backend().bluetooth.get_config())


@module_bp.route('/api/enabled', methods=['POST'])
def bluetooth_install():
    data = request.get_json()

    enabled = data.get('enabled')

    if not isinstance(enabled, bool):
        return jsonify(error="Missing or invalid confirmation."), 400

    if enabled:
        try:
            Backend().bluetooth.install(confirm=True)
        except Exception as e:
            return jsonify(error=f"Installation failed: {str(e)}"), 500
    else:
        try:
            Backend().bluetooth.uninstall(confirm=True)
        except Exception as e:
            return jsonify(error=f"Uninstallation failed: {str(e)}"), 500

    return '', 200

@module_bp.route('/api/settings', methods=['POST'])
def change_bluetooth_settings():
    data = request.get_json()

    if not data:
        return jsonify(error="Request body is empty."), 400  # Bad Request

    current_app.logger.debug("Change bluetooth settings ...")

    backend = Backend().bluetooth
    invalid_keys = []
    failed_keys = []

    for k, v in data.items():
        result = backend.set(k, v)
        current_app.logger.debug(f"Change bluetooth settings: Set k={k}; v={v}")
        if result is None:
            current_app.logger.debug(f"Change bluetooth settings: Invalid k={k}")
            invalid_keys.append(k)
        elif result is False:
            current_app.logger.debug(f"Change bluetooth settings: Failed k={k}")
            failed_keys.append(k)

    if invalid_keys and failed_keys:
        return jsonify(
            error="Some keys are invalid and some failed to update.",
            invalid_keys=invalid_keys,
            failed_keys=failed_keys
        ), 422  # Unprocessable Entity

    if invalid_keys:
        return jsonify(
            error="One or more provided keys are invalid.",
            invalid_keys=invalid_keys
        ), 400  # Bad Request

    if failed_keys:
        return jsonify(
            error="Some settings could not be applied.",
            failed_keys=failed_keys
        ), 409  # Conflict

    current_app.logger.debug("Change bluetooth settings: Successful!")

    return '', 200

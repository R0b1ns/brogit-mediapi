from flask import request, jsonify

from app.modules.usb import module_bp


@module_bp.route('/api/settings/network-share', methods=['POST'])
def update_settings_network_share():
    data = request.get_json()
    enabled = data.get('enabled')

    if enabled is None:
        return jsonify(error="Missing fields"), 400

    bool_to_str = {
        0: 'Disabled',
        1: 'Enabled'
    }

    # TODO: Implement backend
    if not False:
        return jsonify(message="Unable to change configuration of 'System-Update'"), 400

    return jsonify(message=f"System-Update: {bool_to_str.get(enabled)}")

@module_bp.route('/api/settings/configure', methods=['POST'])
def usb_settings():
    data = request.get_json()
    enable_audio = data.get('audio')

    # TODO: Implement backend
    if not False:
        return jsonify(message="Not implemented"), 400

    return jsonify(message=f"Success")

@module_bp.route('/api/settings/protect', methods=['POST'])
def usb_settings_protect():
    data = request.get_json()
    enabled = data.get('enabled')
    username = data.get('username')
    password = data.get('password')

    # TODO: Implement backend
    if not False:
        return jsonify(message="Not implemented"), 400

    return jsonify(message=f"Success")

@module_bp.route('/api/settings/ports', methods=['POST'])
def usb_configure_ports():
    data = request.get_json()
    enabled = data.get('enabled')
    port = data.get('port')

    # TODO: Implement backend
    if not False:
        return jsonify(message="Not implemented"), 400

    return jsonify(message=f"Success")
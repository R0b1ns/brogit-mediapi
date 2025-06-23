from flask import request, jsonify

from app.lib.Backend import Backend
from app.modules.bluetooth import module_bp


@module_bp.route('/api/test', methods=['GET'])
def bluetooth_test():
    r = Backend().bluetooth.read()
    return jsonify(message=r)


@module_bp.route('/api/settings/enable', methods=['POST'])
def bluetooth_enable():
    data = request.get_json()
    enabled = data.get('enabled')

    # TODO: Implement backend
    if not False:
        return jsonify(message="Not implemented"), 400

    return jsonify(message=f"Success")

@module_bp.route('/api/settings/audio', methods=['POST'])
def bluetooth_audio_device():
    data = request.get_json()
    audio_device = data.get('audio_device')

    # TODO: Implement backend
    if not False:
        return jsonify(message="Not implemented"), 400

    return jsonify(message=f"Success")
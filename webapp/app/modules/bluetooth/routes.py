from flask import request, jsonify, current_app

from app.lib.Backend import Backend
from app.modules.bluetooth import module_bp


@module_bp.route('/api/test', methods=['GET'])
def bluetooth_test():
    print(current_app.config)
    r = Backend().bluetooth.get_config()
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

@module_bp.route('/api/settings', methods=['POST'])
def change_bluetooth_settings():
    data = request.get_json()

    if not data:
        return jsonify(message="No data"), 400

    result = {}

    for k, v in data.items():
        result.update({
            k: Backend().bluetooth.set(k, v)
        })

    # for k, f in valid_options.items():
    #     value = data.get(k)
    #
    #     if value is not None:
    #         result.update({
    #             k: False
    #         })
    #
    #     if f(value):
    #         Backend().bluetooth.set(k, value)
    #         result[k] = True
    #
    # if not result:
    #     return jsonify(message=f"Wrong keys. Valid keys: {valid_options.keys()}"), 400



    return jsonify(response=result)
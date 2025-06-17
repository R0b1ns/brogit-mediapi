import time

from flask import request, jsonify

from app.modules.system import module_bp


@module_bp.route('/api/settings/system-update', methods=['POST'])
def update_settings_system_update():
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

@module_bp.route('/api/settings/app-update', methods=['POST'])
def update_settings_app_update():
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
        return jsonify(message="Unable to change configuration of 'App-Update'"), 400

    return jsonify(message=f"App-Update: {bool_to_str.get(enabled)}")

@module_bp.route('/api/app-update', methods=['POST'])
def update_app():
    data = request.get_json()
    branch = data.get('branch')
    commit = data.get('commit')

    if branch is None or commit is None:
        return jsonify(error="Missing fields"), 400

    bool_to_str = {
        0: 'Disabled',
        1: 'Enabled'
    }

    time.sleep(1)

    # TODO: Implement backend
    if not False:
        return jsonify(message="Unable to change configuration of 'App-Update'"), 400

    return jsonify(message=f"Updated [Applicationname] to Version/Branch/Commit")

@module_bp.route('/api/shutdown', methods=['POST'])
def system_shutdown():
    time.sleep(1)

    # TODO: Implement backend
    if not False:
        return jsonify(message="Unable to shutdown the system"), 400

    return jsonify(message=f"Success")

@module_bp.route('/api/reboot', methods=['POST'])
def system_reboot():
    # TODO: Implement backend
    if not False:
        return jsonify(message="Not implemented"), 400

    return jsonify(message=f"Success")

@module_bp.route('/api/reset-factory-defaults', methods=['POST'])
def system_reset_factory_defaults():
    # TODO: Perform this in 2 steps. User has to confirm with password or other
    if not False:
        return jsonify(message="Not implemented"), 400

    return jsonify(message=f"Success")
from app.modules.nginx import module_bp


@module_bp.route('/api/enabled', methods=['POST'])
def install():
    pass

# Update certificate
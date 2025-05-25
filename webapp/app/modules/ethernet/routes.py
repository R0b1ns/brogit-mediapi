from flask import jsonify

from app.lib.Backend import Backend
from app.modules.ethernet import module_bp


@module_bp.route('/api/settings', methods=['GET'])
def get_settings():
    eth_adapter = Backend().network.interface('ethernet')

    return jsonify({
        "status": eth_adapter.is_connected(),
        "interface": eth_adapter.get_ip_info(),
        'dns': eth_adapter.get_dns_info()
    })

@module_bp.route('/api/settings/interface', methods=['POST'])
def set_interface():
    eth_adapter = Backend().network.interface('ethernet')

    # Note: subnet is for example 24. So the netmask e.g. 255.255.255.0 has to be translated
    # eth_adapter.set_static_ip(ip, subnet, gateway)

    # eth_adapter.enable_dhcp()

    return jsonify({"error": "Not implemented"})

@module_bp.route('/api/settings/dns', methods=['POST'])
def set_dns():
    eth_adapter = Backend().network.interface('ethernet')

    # eth_adapter.set_dns(dns_servers)

    # Note: This is to go for dhcp managed dns
    # eth_adapter.reset_dns()

    return jsonify({"error": "Not implemented"})
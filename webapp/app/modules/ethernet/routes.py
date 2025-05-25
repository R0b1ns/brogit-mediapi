from flask import jsonify, request

from app.lib.Backend import Backend
from app.lib.common import netmask_to_cidr, is_valid_ip
from app.modules.ethernet import module_bp


@module_bp.route('/api/settings', methods=['GET'])
def get_settings():
    eth_adapter = Backend().network.interface('ethernet')

    # Fake result for testing
    return jsonify({
        "status": True,
        "interface": {
            "ip": "192.168.1.100",
            "subnet": "24",
            "gateway": "192.168.1.1",
            "method": "dhcp"
        },
        "dns": {
            "method": "auto",
            "dns": ["8.8.8.8", "8.8.4.4"]
        }
    })

    # return jsonify({
    #     # is_connected: Returns bool
    #     "status": eth_adapter.is_connected(),
    #     # get_ip_info: Returns a dictionary with keys: ip, subnet, gateway, method (manual|dhcp).
    #     "interface": eth_adapter.get_ip_info(),
    #     # get_dns_info: Returns {method: auto|manual, dns: [list of servers] }
    #     'dns': eth_adapter.get_dns_info()
    # })

@module_bp.route('/api/settings/interface', methods=['POST'])
def set_interface():
    eth_adapter = Backend().network.interface('ethernet')
    data = request.get_json()

    method = data.get("method")
    ip = data.get("ip", "")
    netmask = data.get("netmask", "")
    gateway = data.get("gateway", "")

    if method not in ["manual", "dhcp"]:
        return jsonify({"success": False, "error": "Invalid method"}), 400

    if method == "manual":
        if not all([ip, netmask, gateway]):
            return jsonify({"success": False, "error": "Missing parameters"}), 400
        if not is_valid_ip(ip):
            return jsonify({"success": False, "error": "Invalid IP"}), 400
        if not is_valid_ip(gateway):
            return jsonify({"success": False, "error": "Invalid Gateway"}), 400

        subnet = netmask_to_cidr(netmask)
        if subnet is None:
            return jsonify({"success": False, "error": "Invalid Netmask"}), 400

    # Fake response
    return jsonify({"success": True})

    # Real Call
    # try:
    #     if method == "dhcp":
    #         eth_adapter.enable_dhcp()
    #     else:
    #         eth_adapter.set_static_ip(ip, subnet, gateway)
    #     return jsonify({"success": True})
    # except Exception:
    #     return jsonify({"success": False}), 500


@module_bp.route('/api/settings/dns', methods=['POST'])
def set_dns():
    eth_adapter = Backend().network.interface('ethernet')
    data = request.get_json()

    method = data.get("method")
    dns_list = data.get("dns", [])

    if method not in ["auto", "manual"]:
        return jsonify({"success": False, "error": "Invalid method"}), 400

    if method == "manual":
        if not isinstance(dns_list, list) or not dns_list:
            return jsonify({"success": False, "error": "DNS list missing"}), 400
        for entry in dns_list:
            if not is_valid_ip(entry):
                return jsonify({"success": False, "error": f"Invalid DNS: {entry}"}), 400

    # Fake response
    return jsonify({"success": True})

    # Real Call
    # try:
    #     if method == "auto":
    #         eth_adapter.reset_dns()
    #     else:
    #         eth_adapter.set_dns(dns_list)
    #     return jsonify({"success": True})
    # except Exception:
    #     return jsonify({"success": False}), 500
#!/bin/bash

set -u

ACTION="${1:-}"
TARGET="${2:-}"

require_root() {
    if [[ "$EUID" -ne 0 ]]; then
        echo "This action requires root privileges." >&2
        exit 1
    fi
}

print_help() {
    cat <<EOF
Usage: $0 <action> <target> [args...]

Actions:
  is_connected <interface>
      Returns 1 if interface is up, else 0.

  get_ip_info <interface>
      Prints ip, subnet (CIDR), gateway, and method (auto/manual).

  set_static_ip <interface> <ip> <subnet> [gateway]
      Sets a static IP address with optional gateway.

  enable_dhcp <connection_name>
      Enables DHCP for the specified NetworkManager connection.

  get_interfaces
      Lists all network interfaces.

  get_connections
      Lists all NetworkManager connections.

  help
      Shows this help text.
EOF
}

is_connected() {
    [[ -e "/sys/class/net/$TARGET/operstate" ]] && \
        [[ "$(cat /sys/class/net/$TARGET/operstate)" == "up" ]] && echo "1" || echo "0"
}

get_ip_info() {
    IP_INFO=$(ip -o -f inet addr show "$TARGET" 2>/dev/null | awk '{print $4}')
    IP=${IP_INFO%%/*}
    CIDR=${IP_INFO##*/}

    GATEWAY=$(nmcli -t -f IP4.GATEWAY device show "$TARGET" 2>/dev/null | grep -v '^$' | head -n1)
    [[ -z "$GATEWAY" ]] && \
        GATEWAY=$(ip route show dev "$TARGET" 2>/dev/null | awk '/^default via/ {print $3; exit}')

    METHOD=$(nmcli -t -f IP4.METHOD device show "$TARGET" 2>/dev/null | grep -v '^$' | head -n1)

    echo "ip=${IP:-}"
    echo "subnet=${CIDR:-}"
    echo "gateway=${GATEWAY:-}"
    echo "method=${METHOD:-unknown}"
}

set_static_ip() {
    require_root

    IP="${3:-}"
    SUBNET="${4:-}"
    GATEWAY="${5:-}"

    if [[ -z "$IP" || -z "$SUBNET" ]]; then
        echo "Missing IP or subnet." >&2
        exit 1
    fi

    ip addr flush dev "$TARGET" || exit 1
    ip addr add "$IP/$SUBNET" dev "$TARGET" || exit 1
    ip link set "$TARGET" up || exit 1

    if [[ -n "$GATEWAY" ]]; then
        ip route del default 2>/dev/null || true
        ip route add default via "$GATEWAY" dev "$TARGET" || exit 1
    fi

    echo "OK"
}

enable_dhcp() {
    require_root

    # TARGET ist hier der Verbindungsname
    nmcli con mod "$TARGET" ipv4.method auto || {
        echo "Failed to set DHCP method on connection $TARGET" >&2
        exit 1
    }
    nmcli con up "$TARGET" || {
        echo "Failed to bring connection $TARGET up" >&2
        exit 1
    }

    echo "OK"
}

get_interfaces() {
    ip -o link show | awk -F': ' '{print $2}'
}

get_connections() {
    nmcli -t -f NAME con show
}

# === Dispatcher ===

if [[ "$ACTION" == "help" || "$ACTION" == "--help" || "$ACTION" == "-h" ]]; then
    print_help
    exit 0
fi

if [[ "$ACTION" != "help" && "$ACTION" != "get_interfaces" && "$ACTION" != "get_connections" && -z "${TARGET:-}" ]]; then
    echo "Error: Target (interface or connection) not specified." >&2
    print_help
    exit 1
fi

case "$ACTION" in
    is_connected) is_connected ;;
    get_ip_info) get_ip_info ;;
    set_static_ip) set_static_ip "$@" ;;
    enable_dhcp) enable_dhcp ;;
    get_interfaces) get_interfaces ;;
    get_connections) get_connections ;;
    *)
        echo "Unknown action: $ACTION" >&2
        print_help
        exit 1
        ;;
esac

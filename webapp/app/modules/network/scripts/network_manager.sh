#!/bin/bash

set -u

ACTION="${1:-}"
IFACE="${2:-}"

require_root() {
    if [[ "$EUID" -ne 0 ]]; then
        echo "This action requires root privileges." >&2
        exit 1
    fi
}

print_help() {
    cat <<EOF
Usage: $0 <action> <interface> [args...]

Actions:
  is_connected <interface>
      Returns 1 if interface is up, else 0.

  get_ip_info <interface>
      Prints IP, subnet (CIDR), gateway, and method (auto/manual).

  set_static_ip <interface> <ip> <subnet> [gateway]
      Sets a static IP address with optional gateway.

  enable_dhcp <interface>
      Enables DHCP via NetworkManager.

  help
      Shows this help text.
EOF
}

is_connected() {
    [[ -e "/sys/class/net/$IFACE/operstate" ]] && \
        [[ "$(cat /sys/class/net/$IFACE/operstate)" == "up" ]] && echo "1" || echo "0"
}

get_ip_info() {
    IP_INFO=$(ip -o -f inet addr show "$IFACE" 2>/dev/null | awk '{print $4}')
    IP=${IP_INFO%%/*}
    CIDR=${IP_INFO##*/}

    GATEWAY=$(nmcli -t -f IP4.GATEWAY device show "$IFACE" 2>/dev/null | grep -v '^$' | head -n1)
    [[ -z "$GATEWAY" ]] && \
        GATEWAY=$(ip route show dev "$IFACE" 2>/dev/null | awk '/^default via/ {print $3; exit}')

    METHOD=$(nmcli -t -f IP4.METHOD device show "$IFACE" 2>/dev/null | grep -v '^$' | head -n1)

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

    ip addr flush dev "$IFACE" || exit 1
    ip addr add "$IP/$SUBNET" dev "$IFACE" || exit 1
    ip link set "$IFACE" up || exit 1

    if [[ -n "$GATEWAY" ]]; then
        ip route del default 2>/dev/null
        ip route add default via "$GATEWAY" dev "$IFACE" || exit 1
    fi

    echo "OK"
}

enable_dhcp() {
    require_root

    if ! nmcli con show "$IFACE" &>/dev/null; then
        nmcli con add type ethernet ifname "$IFACE" con-name "$IFACE" || exit 1
    fi

    nmcli con mod "$IFACE" ipv4.method auto || exit 1
    nmcli con up "$IFACE" || exit 1
    echo "OK"
}

# === Dispatcher ===

if [[ "$ACTION" == "help" || "$ACTION" == "--help" || "$ACTION" == "-h" ]]; then
    print_help
    exit 0
fi

if [[ "$ACTION" != "help" && -z "${IFACE:-}" ]]; then
    echo "Error: Interface not specified." >&2
    print_help
    exit 1
fi

case "$ACTION" in
    is_connected) is_connected ;;
    get_ip_info) get_ip_info ;;
    set_static_ip) set_static_ip "$@" ;;
    enable_dhcp) enable_dhcp ;;
    *)
        echo "Unknown action: $ACTION" >&2
        print_help
        exit 1
        ;;
esac

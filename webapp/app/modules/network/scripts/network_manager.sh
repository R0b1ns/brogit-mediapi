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
Usage: $0 <action> <interface> [args...]

Actions:
  is_connected <interface>
      Returns 1 if interface is up, else 0.

  get_ip_info <interface>
      Prints IP, subnet (CIDR), gateway, and method (auto/manual).

  get_dns <interface>
      Prints the currently configured DNS servers.

  set_dns <interface> <dns1> [dns2] [...]
      Sets one or more static DNS servers.

  reset_dns <interface>
      Restores DNS from DHCP and clears static DNS entries.

  set_static_ip <interface> <ip> <subnet> [gateway]
      Sets a static IP address with optional gateway.

  enable_dhcp <interface>
      Enables DHCP via NetworkManager.

  get_interfaces
      Lists available network interfaces.

  get_connections
      Lists NetworkManager connections.

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

    CON_NAME=$(nmcli -t -f NAME,DEVICE con show --active | grep ":$TARGET\$" | cut -d: -f1)
    if [[ -n "$CON_NAME" ]]; then
        METHOD=$(nmcli -g ipv4.method con show "$CON_NAME" 2>/dev/null)
    else
        METHOD="unknown"
    fi

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

    # Finde passende Verbindung für das Interface
    CON_NAME=$(nmcli -t -f NAME,DEVICE con show --active | grep ":$TARGET\$" | cut -d: -f1)
    if [[ -z "$CON_NAME" ]]; then
        CON_NAME=$(nmcli -t -f NAME,DEVICE con show | grep ":$TARGET\$" | cut -d: -f1 | head -n1)
    fi

    if [[ -z "$CON_NAME" ]]; then
        echo "No connection found for interface: $TARGET" >&2
        exit 1
    fi

    # Setze Methode auf DHCP und aktiviere
    nmcli con mod "$CON_NAME" ipv4.method auto || {
        echo "Failed to set DHCP method for $CON_NAME" >&2
        exit 1
    }

    nmcli con up "$CON_NAME" || {
        echo "Failed to bring up $CON_NAME" >&2
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

get_dns() {
    nmcli -t -f IP4.DNS device show "$TARGET" 2>/dev/null | grep -v '^$' | tr ';' '\n'
}

set_dns() {
    require_root

    # Mindestens 3 Argumente: script, set_dns, interface, dns1 ...
    if [[ $# -lt 3 ]]; then
        echo "Usage: $0 set_dns <interface> <dns1> [dns2] [...]" >&2
        exit 1
    fi

    # Interface ist $2, DNS ab $3
    TARGET="$2"
    shift 2
    DNS_LIST="$*"

    # Verbindung finden
    CON_NAME=$(nmcli -t -f NAME,DEVICE con show --active | grep ":$TARGET\$" | cut -d: -f1)
    if [[ -z "$CON_NAME" ]]; then
        CON_NAME=$(nmcli -t -f NAME,DEVICE con show | grep ":$TARGET\$" | cut -d: -f1 | head -n1)
    fi

    if [[ -z "$CON_NAME" ]]; then
        echo "Connection for interface $TARGET not found." >&2
        exit 1
    fi

    nmcli con mod "$CON_NAME" ipv4.ignore-auto-dns yes || exit 1
    nmcli con mod "$CON_NAME" ipv4.dns "$DNS_LIST" || exit 1
    nmcli con up "$CON_NAME" || exit 1

    echo "OK"
}

reset_dns() {
    require_root

    if [[ $# -lt 2 ]]; then
        echo "Usage: $0 reset_dns <interface>" >&2
        exit 1
    fi

    TARGET="$2"

    # Verbindung finden
    CON_NAME=$(nmcli -t -f NAME,DEVICE con show --active | grep ":$TARGET\$" | cut -d: -f1)
    if [[ -z "$CON_NAME" ]]; then
        CON_NAME=$(nmcli -t -f NAME,DEVICE con show | grep ":$TARGET\$" | cut -d: -f1 | head -n1)
    fi

    if [[ -z "$CON_NAME" ]]; then
        echo "Connection for interface $TARGET not found." >&2
        exit 1
    fi

    nmcli con mod "$CON_NAME" ipv4.ignore-auto-dns no || exit 1
    nmcli con mod "$CON_NAME" ipv4.dns "" || exit 1
    nmcli con up "$CON_NAME" || exit 1

    echo "OK"
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
    get_dns) get_dns ;;
    set_dns) set_dns "$@" ;;
    reset_dns) reset_dns "$@" ;;
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


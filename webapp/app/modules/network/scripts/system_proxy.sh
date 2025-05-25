#!/bin/bash

set -u

ACTION="${1:-}"

PROXY_VARS=("http_proxy" "https_proxy" "no_proxy")

print_help() {
    cat <<EOF
Usage: $0 <action> [args...]

Actions:
  get_proxy
      Prints the current proxy settings (http_proxy, https_proxy, no_proxy).

  set_proxy <http_proxy> [https_proxy] [no_proxy]
      Sets proxy environment variables.
      If https_proxy or no_proxy are omitted, https_proxy defaults to http_proxy,
      no_proxy defaults to empty.

  clear_proxy
      Clears proxy environment variables.

  help
      Shows this help text.
EOF
}

get_proxy() {
    for var in "${PROXY_VARS[@]}"; do
        val="${!var:-}"
        echo "$var=${val}"
    done
}

set_proxy() {
    if [[ -z "${2:-}" ]]; then
        HTTP_PROXY="$2"
        HTTPS_PROXY="$2"
        NO_PROXY=""
    else
        HTTP_PROXY="$2"
        HTTPS_PROXY="${3:-$HTTP_PROXY}"
        NO_PROXY="${4:-}"
    fi

    # Export shell environment variables (uppercase and lowercase)
    for var in "${PROXY_VARS[@]}"; do
        val=""
        case "$var" in
            http_proxy) val="$HTTP_PROXY" ;;
            https_proxy) val="$HTTPS_PROXY" ;;
            no_proxy) val="$NO_PROXY" ;;
        esac
        export "$var"="$val"
        export "$(echo $var | tr 'a-z' 'A-Z')"="$val"
    done

    # Optional: set git proxy config globally
    if command -v git >/dev/null 2>&1; then
        git config --global http.proxy "$HTTP_PROXY"
        git config --global https.proxy "$HTTPS_PROXY"
    fi

    echo "Proxy set."
}

clear_proxy() {
    for var in "${PROXY_VARS[@]}"; do
        unset "$var"
        unset "$(echo $var | tr 'a-z' 'A-Z')"
    done

    # Optional: clear git proxy config
    if command -v git >/dev/null 2>&1; then
        git config --global --unset http.proxy || true
        git config --global --unset https.proxy || true
    fi

    echo "Proxy cleared."
}

if [[ "$ACTION" == "help" || "$ACTION" == "-h" || "$ACTION" == "--help" ]]; then
    print_help
    exit 0
fi

case "$ACTION" in
    get_proxy) get_proxy ;;
    set_proxy)
        if [[ $# -lt 2 ]]; then
            echo "Usage: $0 set_proxy <http_proxy> [https_proxy] [no_proxy]" >&2
            exit 1
        fi
        set_proxy "$@" ;;
    clear_proxy) clear_proxy ;;
    *)
        echo "Unknown action: $ACTION" >&2
        print_help
        exit 1
        ;;
esac

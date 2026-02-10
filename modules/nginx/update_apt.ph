#!/bin/sh

# brogit (c) 2026
# Author: r0b1ns

set -e

PKG="$1"

if [ -z "$PKG" ]; then
  echo "Usage: $0 <package-name>" >&2
  exit 2
fi

apt-get update -qq

if apt-get install -y --only-upgrade "$PKG"; then
  echo "$PKG updated successfully."
  exit 0   # Erfolg
else
  echo "Failed to update $PKG." >&2
  exit 1   # Fehler
fi

#!/bin/sh
set -e

# TODO: THIS FILE IS COMPLETLY GENERIC AND SHOULD BE MOVED TO A GENERIC PLACE WHERE OTHERS ALSO USE THAT

PKG="$1"

if [ -z "$PKG" ]; then
  echo "Usage: $0 <package-name>" >&2
  exit 1
fi

# refresh package lists
apt-get update -qq

# check if package is upgradable
if apt list --upgradable 2>/dev/null | grep -q "^$PKG/"; then
  exit 0
else
  exit 1
fi

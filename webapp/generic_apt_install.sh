#!/bin/bash

set -e  # Exit on error

# Check for root permissions
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run with sudo or as root."
   exit 1
fi

# Use default file if no argument is given
REQUIREMENTS_FILE="${1:-apt-requirements.txt}"

# Check if the file exists
if [[ ! -f "$REQUIREMENTS_FILE" ]]; then
    echo "Requirements file '$REQUIREMENTS_FILE' not found!"
    exit 1
fi

echo "Installing packages from $REQUIREMENTS_FILE..."

apt update

# Filter out comments and empty lines before passing to xargs
grep -vE '^\s*#|^\s*$' "$REQUIREMENTS_FILE" | xargs apt install -y

echo "Done."

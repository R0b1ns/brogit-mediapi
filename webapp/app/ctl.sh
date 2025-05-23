#!/bin/bash

# Check if at least two arguments are passed
if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <module> <command> [additional arguments]"
  exit 1
fi

# First argument: Module name
MODULE=$1

# Second argument: Command
COMMAND=$2

# Additional arguments (optional)
shift 2
ADDITIONAL_ARGS="$@"

# Path to the module script
MODULE_SCRIPT="modules/$MODULE/modulectl.sh"

# Check if the module script exists
if [ ! -f "$MODULE_SCRIPT" ]; then
  echo "Error: Module script '$MODULE_SCRIPT' not found."
  exit 1
fi

# Execute the module script with the passed arguments
bash "$MODULE_SCRIPT" "$COMMAND" $ADDITIONAL_ARGS

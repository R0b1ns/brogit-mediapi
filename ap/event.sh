#!/bin/bash

# brogit (c) 2024
# Author: r0b1ns

echo "$1"
echo "$2"

if [[ "$2" == "up" ]]; then
  echo "Up"
elif [[ "$2" == "down" ]]; then
  echo "Down"
fi

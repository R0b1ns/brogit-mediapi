#!/bin/bash

if [ ! -d ".venv" ]; then
    echo "Create virtual environment..."
    python3 -m venv .venv
fi

source ./.venv/bin/activate

echo "Install dependencies ..."
pip3 install -r requirements.txt

echo "Run ..."
source ./.venv/bin/activate
python3 ./app.py
#!/bin/bash

# brogit (c) 2025
# Author: r0b1ns

systemctl disable gmediarender
systemctl stop gmediarender

sudo rm /etc/systemd/system/gmediarender.service

sudo systemctl daemon-reload
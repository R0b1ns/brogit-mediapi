#!/bin/bash

PROJECT_RELATIVE_ROOT="../"
PROJECT_ROOT_PATH=$(realpath "$PROJECT_RELATIVE_ROOT")
LOCALE="de-DE"
CONNECT_TEXT="Verbunden mit: \$DEVICES"
AUDIO_DEVICE="hci0"

apt install -y --no-install-recommends bluez-tools bluez-alsa-utils libttspico-utils

# Bluetooth adapter configuration
if [[ ! -f /etc/bluetooth/main.conf.bak ]]; then
  cp /etc/bluetooth/main.conf /etc/bluetooth/main.conf.bak
  echo "Created Backup of /etc/bluetooth/main.conf"
fi
cat << 'EOF' | sudo tee /etc/bluetooth/main.conf > /dev/null
[General]
Class = 0x200414
DiscoverableTimeout = 0
PairableTimeout = 0

[Policy]
AutoEnable=true
EOF

# Bluetooth Agent Service
cat << 'EOF' | sudo tee /etc/systemd/system/bt-agent@.service > /dev/null
[Unit]
Description=Bluetooth Agent
Requires=bluetooth.service
After=bluetooth.service

[Service]
ExecStartPre=/usr/bin/bluetoothctl discoverable on
ExecStartPre=/bin/hciconfig %I piscan
ExecStartPre=/bin/hciconfig %I sspmode 1
ExecStart=/usr/bin/bt-agent --capability=NoInputNoOutput
RestartSec=5
Restart=always
KillSignal=SIGUSR1

[Install]
WantedBy=multi-user.target
EOF

# Event script when connect or disconnect happens
BT_SOUND_FILE_PATH="$PROJECT_ROOT_PATH/bt/dyn_bt_connect_event.sh"

cat << EOF | sudo tee $BT_SOUND_FILE_PATH > /dev/null
#!/bin/bash

if [[ "\$1" == "add" ]]; then
    aplay ./connect.wav
    DEVICES=\$(bluetoothctl devices Connected | grep "Device" | awk '{print \$3, \$4}' | paste -sd ',' - | sed 's/,/, /g')
    TEMP_FILE_NAME="temp_output_\$(date +%s).wav"
    pico2wave -w \$TEMP_FILE_NAME -l "$LOCALE" "$CONNECT_TEXT"
    aplay $TEMP_FILE_NAME
    rm $TEMP_FILE_NAME
elif [[ "\$1" == "remove" ]]; then
    aplay ./disconnect.wav
fi
EOF

# Make file executeable
chmod +x $BT_SOUND_FILE_PATH

# UDEV Rule for Connect/Disconnect event sound
cat << EOF | sudo tee /etc/udev/rules.d/99-bluetooth-connect.rules > /dev/null
ACTION=="add", SUBSYSTEM=="bluetooth", RUN+="$BT_SOUND_FILE_PATH add"
ACTION=="remove", SUBSYSTEM=="bluetooth", RUN+="$BT_SOUND_FILE_PATH remove"
EOF

sudo udevadm control --reload-rules
sudo udevadm trigger

# Enable and Start services
sudo systemctl daemon-reload

# Autostart Agent for audio device agent
sudo systemctl enable bt-agent@${AUDIO_DEVICE}.service
sudo systemctl start bt-agent@${AUDIO_DEVICE}.service

sudo systemctl enable bluetooth
sudo systemctl start bluetooth

sudo systemctl enable bluealsa
sudo systemctl start bluealsa
# Dev Helper
udevadm monitor --environment --udev

# Udev alternative:
ACTION=="add", SUBSYSTEM=="input", GROUP="input", MODE="0660" KERNEL=="input[0-9]*", RUN+="/root/bt-sound.sh add $env{NAME}"
ACTION=="remove", SUBSYSTEM=="input", GROUP="input", MODE="0660" KERNEL=="input[0-9]*", RUN+="/root/bt-sound.sh remove $env{NAME}"

## Trust script
sudo nano /etc/udev/rules.d/99-bluetooth-trust.rules
SUBSYSTEM=="input", GROUP="input", MODE="0660" KERNEL=="input[0-9]*", RUN+="/usr/bin/bluetoothctl -- trust %b"
sudo udevadm control --reload-rules

# DEV Notes

aplay um einen sound aus dem terminal abzuspielen

## Pipewire with Bluetooth
#### !!! Kein Pipewire oder Pulseaudio, da diese für GUI gedacht sind und erst nach Benutzersitzung ausgeführt werden.
apt install pipewire pipewire-audio-client-libraries pipewire-media-session
sudo systemctl enable bluetooth
sudo systemctl start bluetooth
pipewire --version

# ALSA mit dmix um device busy problem zu lösen.
apt install alsa-utils
~/.asoundrc

# BluezAlsa (Bluetooth Audio)
git clone https://github.com/arkq/bluez-alsa.git
cd bluez-alsa
autoreconf --install
./configure --enable-systemd
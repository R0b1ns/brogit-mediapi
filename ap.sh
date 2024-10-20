sudo apt-get install -y hostapd dnsmasq

sudo systemctl stop hostapd
sudo systemctl stop dnsmasq

# Konfiguriere hostapd
cat <<EOL | sudo tee /etc/hostapd/hostapd.conf
interface=wlan0
driver=nl80211
ssid=$(hostname)-AP
hw_mode=g
channel=6
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=0
EOL
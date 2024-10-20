sudo apt-get install -y hostapd dnsmasq nodogsplash

sudo systemctl stop hostapd
sudo systemctl stop dnsmasq
sudo systemctl stop nodogsplash

# Konfiguriere hostapd
cat <<EOL | sudo tee /etc/hostapd/hostapd.conf > /dev/null
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

# Konfiguriere dnsmasq
cat <<EOL | sudo tee /etc/dnsmasq.conf > /dev/null
interface=wlan0      # Use the required interface
dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
EOL

# Setze die Schnittstelle wlan0 auf statische IP
if ! grep -q "interface wlan0" /etc/dhcpcd.conf; then
    sudo bash -c 'cat <<EOL >> /etc/dhcpcd.conf
interface wlan0
static ip_address=192.168.4.1/24
nohook wpa_supplicant
EOL'
fi

cat <<EOL | sudo tee /etc/nodogsplash/nodogsplash.conf > /dev/null
GatewayInterface wlan0
GatewayPort 80
MaxClients 50
SplashURL http://localhost
EOL

# Unmask hostapd to enable the start
sudo systemctl unmask hostapd

sudo systemctl start hostapd
sudo systemctl start dnsmasq
sudo systemctl start nodogsplash
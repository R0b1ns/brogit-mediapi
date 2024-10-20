sudo apt-get install -y hostapd dnsmasq dhcpcd5

sudo systemctl stop hostapd
sudo systemctl stop dnsmasq
sudo systemctl stop dhcpcd

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

apt install libmicrohttpd-dev iptables git
git clone https://github.com/NoDogSplash/NoDogSplash.git
cd NoDogSplash
sudo make
sudo make install

cat <<EOL | sudo tee /etc/nodogsplash/nodogsplash.conf > /dev/null
GatewayInterface wlan0
GatewayPort 80
MaxClients 50
EOL

# Unmask hostapd to enable the start
sudo systemctl unmask hostapd

# Starte die Dienste in der richtigen Reihenfolge
sudo systemctl start dhcpcd   # Setzt die statische IP
sudo systemctl start dnsmasq  # Startet den DHCP-Server
sudo systemctl start hostapd  # Startet den Access Point

# Starte NoDogSplash
# sudo nodogsplash

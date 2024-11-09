create_log_with_rotation() {
    local log_dir="$1"
    local log_name="$2"
    local log_file="$log_dir/$log_name.log"

    # Erstellen des Log-Verzeichnisses, falls es nicht existiert
    sudo mkdir -p "$log_dir"

    # Erstellen der Log-Datei, falls sie nicht existiert
    sudo touch "$log_file"

    # logrotate-Konfiguration erstellen
    local logrotate_conf="/etc/logrotate.d/$(basename "$log_name")"

    sudo tee "$logrotate_conf" > /dev/null <<EOF
$log_file {
    size 1M               # Rotation bei Überschreiten von 1 MB
    rotate 10             # Bis zu 10 rotierte Archive behalten
    compress              # Ältere Log-Dateien komprimieren
    delaycompress         # Verzögert die Komprimierung um eine Rotation
    missingok             # Überspringen, wenn Log-Datei fehlt
    notifempty            # Nicht rotieren, wenn Log-Datei leer ist
    create 0640 root root # Neue Log-Dateien mit Berechtigungen 0640 erstellen
}
EOF

    echo "$log_file"
}

log_message() {
    local log_file="$1"
    local message="$2"
    echo "$(date +'%Y-%m-%d %H:%M:%S') - $message" >> "$log_file"
}
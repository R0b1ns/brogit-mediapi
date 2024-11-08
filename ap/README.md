# Trigger Skript
We proceed to resolve this problem with a network manager dispatcher script

## Alternative: wpa_supplicant
It is also possible to resolve this problem with an event script executed by wpa_supplicant

## install.sh
Installs the dispatcher which executes event.sh

## event.sh
Executes delayed_start.sh with config AP_START_DELAY_AFTER_DISCONNECT when wifi is down
or cancels the delayed_start.sh when the connection comes back (up)

## delayed_start.sh
Controls when the start.sh will be executed

## start.sh
Starts the Access Point <- Will be started automatically

## stop.sh
Stops the Access Point <- Should be executed with the WebApp
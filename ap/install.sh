#!/bin/bash

PROJECT_RELATIVE_ROOT="../"
PROJECT_ROOT_PATH="$(realpath "$(dirname "${BASH_SOURCE[0]}")/$PROJECT_RELATIVE_ROOT")"

# Event when connect state change
cat << EOF | sudo tee /etc/NetworkManager/dispatcher.d/99-wifi-event.sh > /dev/null
#!/bin/bash

# Redirect event to eventhandler
$PROJECT_ROOT_PATH/event.sh wifi "\$@"
EOF

sudo chmod +x /etc/NetworkManager/dispatcher.d/99-wifi-event.sh


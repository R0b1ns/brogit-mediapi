$(document).ready(function() {
    var socket = io();

    function fetchNetworks() {
        $('#networks').html($('template.network-list-loading').html());
        $('#connected-network').hide();
        $('#network-list-refresh').prop('disabled', true);
        socket.emit('request_wifi');
    }

    socket.on('response_wifi', function(data) {
        const connectedNetworkElement = $('#current-network');
        const networksDiv = $('#networks');
        const selectedNetworkElement = $('#selected-network');
        const connectedNetworkContainer = $('#connected-network');

        networksDiv.empty(); // Clear the networks div
        connectedNetworkElement.empty(); // Clear the connected network element
        selectedNetworkElement.empty(); // Clear the selected network element

        // Separate the connected network from the others
        let connectedNetwork = null;
        let otherNetworks = [];

        data.networks.forEach(function(network) {
            if (network.connected) {
                connectedNetwork = network;
            } else {
                otherNetworks.push(network);
            }
        });

        // Display the connected network if any
        if (connectedNetwork) {
            const passwordIcon = connectedNetwork.protected ? '<i class="bi bi-lock-fill protected"></i>' : '<i class="bi bi-unlock"></i>';
            connectedNetworkElement.html(`${passwordIcon} ${connectedNetwork.ssid} (${connectedNetwork.band})`);
            connectedNetworkContainer.show(); // Show the connected network
        } else {
            connectedNetworkContainer.hide(); // Hide if no connected network
        }

        // Display the other networks using the template
        otherNetworks.forEach(function(network) {
            const icon = network.known
                ? '<i class="bi bi-star known"></i>'  // Star icon for known networks
                : '<i class="bi bi-wifi-off"></i>';  // WiFi off icon for unknown networks

            const passwordIcon = network.protected ? '<i class="bi bi-lock-fill protected"></i>' : '<i class="bi bi-unlock"></i>';

            // Clone the template and replace the placeholders
            const template = $('#network-template').html();
            const radioOption = template
                .replace(/\[\[ssid\]\]/g, network.ssid)
                .replace(/\[\[band\]\]/g, network.band)
                .replace(/\[\[known\]\]/g, network.known ? '✓' : '')
                .replace(/\[\[icon\]\]/g, icon)
                .replace(/\[\[passwordIcon\]\]/g, passwordIcon);

            networksDiv.append(radioOption);
        });

        // Set up click event for network selection
        $('input[name="network"]').on('change', function() {
            // Get the selected SSID
            selectNetwork($(this).val());
        });

        $('input[name="network"]').on('click', function() {
            // Get the selected SSID
            selectNetwork($(this).val());
        });

        $('#network-list-refresh').prop('disabled', false);
    });

    function selectNetwork(ssid) {
        if(ssid) {
            $('#network-ssid').attr('type', 'hidden');
            $('#network-ssid').val(ssid);

            $('#selected-network').text("for " + ssid);
            $('label[for="network-ssid"]').hide();
        }
        else {
            $('#network-ssid').attr('type', 'text');
            $('#network-ssid').val('');

            $('#selected-network').text("");
            $('label[for="network-ssid"]').show();
        }
        nextPage();
    }

    function previousPage() {
        $('#network-connect').fadeOut(null, function() {
            $('#network-select').fadeIn();
        });
    }

    function nextPage() {
        $('#network-select').fadeOut(null, function() {
            $('#network-connect').fadeIn();
            // Push a new state to the history
            window.history.pushState({ page: 'network-connect' }, '', '#network-connect');
        });
    }

    $('#network-list-refresh').click(fetchNetworks);

    $('button#other-network').click(function() {
        selectNetwork();
        nextPage();
    });


    $('#connect-button').click(function() {
        const password = $('#network-password').val();
        const selectedNetwork = $('input[name="network"]:checked');
        if (selectedNetwork.length) {
            const ssid = selectedNetwork.val();
            // Add your code to connect to the network using the selected SSID and password
            console.log(`Connecting to ${ssid} with password ${password}`);
        }
    });

    // Initial fetch of networks on page load
    fetchNetworks();

    window.onpopstate = function(event) {
        if (event.state && event.state.page === 'network-connect') {
            previousPage();
        }
    };
});

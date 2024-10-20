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
            const signalIcon = connectedNetwork.signal > 66
                ? '<i class="bi bi-wifi"></i>'
                : connectedNetwork.signal > 33 ?
                '<i class="bi bi-wifi-2"></i>'
                : '<i class="bi bi-wifi-1"></i>';

            const passwordIcon = connectedNetwork.protected ? '<i class="bi bi-lock-fill protected" title="Protected"></i>' : '<i class="bi bi-unlock" title="Unprotected"></i>';
            connectedNetworkElement.html(`${signalIcon} ${passwordIcon} ${connectedNetwork.ssid} (${connectedNetwork.band})`);
            connectedNetworkContainer.show(); // Show the connected network
        } else {
            connectedNetworkContainer.hide(); // Hide if no connected network
        }

        // Display the other networks using the template
        otherNetworks.forEach(function(network) {
            const signalIcon = network.signal > 66
                ? '<i class="bi bi-wifi"></i>'
                : network.signal > 33 ?
                '<i class="bi bi-wifi-2"></i>'
                : '<i class="bi bi-wifi-1"></i>';

            const passwordIcon = network.protected ? '<i class="bi bi-lock-fill protected" title="Protected"></i>' : '<i class="bi bi-unlock" title="Unprotected"></i>';

            // Clone the template and replace the placeholders
            const template = $('#network-template').html();
            const radioOption = template
                .replace(/\[\[ssid\]\]/g, network.ssid)
                .replace(/\[\[band\]\]/g, network.band)
                .replace(/\[\[known\]\]/g, network.known ? '✓' : '')
                .replace(/\[\[signal\]\]/g, signalIcon)
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

    $('form#connect').on('submit', function(e) {
        e.preventDefault();
        $(this).find('input[type=submit]').prop('disabled', true);

        const ssid = $('#network-ssid').val();
        const password = $('#network-password').val();
        const errorMessageContainer = $('#error-message');

        if (ssid.length) {
            let url = $(this).attr('action');
            url += `?ssid=${encodeURIComponent(ssid)}`;

            if (password) {
                url += `&password=${encodeURIComponent(password)}`;
            }

            $.get(url, function(response) {
                alert('Hier passiert was');
                console.log(response);
                if (response.success) {
                    errorMessageContainer.hide();

                    console.log(`Waiting for device at hostname: ${deviceHostname}`);

                    // Warte und überprüfe, ob das Gerät unter dem neuen Hostnamen erreichbar ist
                    const checkInterval = setInterval(function() {
                        $.get(`http://${deviceHostname}/api/status`, function(statusResponse) {
                            if (statusResponse.success) {
                                clearInterval(checkInterval);  // Stoppe die Abfrage
                                window.location.href = `http://${deviceHostname}`;  // Redirect auf die neue IP
                            }
                        }).fail(function() {
                            console.log('Gerät noch nicht erreichbar, warte weiter...');
                        });
                    }, 3000);  // Überprüfe alle 3 Sekunden

                } else {
                    errorMessageContainer.text(response.error + ': ' + response.details).show();
                }
            }).fail(function(error) {
                errorMessageContainer.text(error.responseJSON.error + ': ' + error.responseJSON.details).show();
            });
        } else {
            errorMessageContainer.text('No SSID is given.').show();
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

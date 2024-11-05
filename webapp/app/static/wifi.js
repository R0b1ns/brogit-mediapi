function connect_wifi(ssid, password, callback_function) {
    // callback_function(status, msg)

    if(!ssid.length) {
        callback_function("error", "No SSID is given.");
        return false;
    }

    let url = wifi_connect_endpoint;
    url += `?ssid=${encodeURIComponent(ssid)}`;

    if (password) {
        url += `&password=${encodeURIComponent(password)}`;
    }

    // status: Wait for disconnect
    callback_function("wait", "Wait for disconnect");

    // `http://mediapi2.local/api/connect`
    $.ajax({
        url: url,
        success: function(response){
            callback_function("success", "Success");
        },
        error: function(jqXHR, textStatus, errorThrown) {
            if(textStatus == "timeout" && errorThrown == "timeout" && !jqXHR.responseText) {
                // Successful disconnect
                callback_function("success", "Timeout");
            }
            else if(jqXHR.responseText) {
                // Response with error
                callback_function("error", jqXHR.responseJSON.message);
            }
            else {
                // Unknown error
                callback_function("error", "Unknown error. The server most likely closed the connection.");
            }
        },
        timeout: 5000 //in milliseconds
    });
}

function connect_wifi_gui(ssid, password) {
    // Prepare GUI

    var delay1 = 500;
    var delay2 = 500;

    if($('#settingsModal').hasClass('show')) {
        delay1 = 0;
    }

    if($('#v-pills-wifi-tab').hasClass('active')) {
        delay2 = 0;
    }

    $({})
        .queue(function(next) {
            $('#settingsModal').modal('show');
            next();
        })
        .delay(delay1)
        .queue(function(next) {
            bootstrap.Tab.getOrCreateInstance($('#v-pills-wifi-tab')).show();
            next();
        })
        .delay(delay2)
        .queue(function(next) {
            // Cleanup modal
            //$('#connect-step-disconnect').find('section').hide();
            $('#settings-wifi-connect').modal('show');
            next();
        });

    // Start
    const errorMessageContainer = $('#error-message');

    connect_wifi(ssid, password, function(status, message) {
        if(status == "wait") {
            $('#connect-step-disconnect').find('section.wait').fadeIn();
        }
        else if(status == "success") {
            if(message == "Timeout") {
                // Connection lost -> redirect
                $('#connect-step-disconnect').find('section.wait').fadeOut(400, function() {
                    $('#connect-step-disconnect').find('section.success').slideDown(400, function() {
                        // Check redirect
                        deviceRedirect();
                    });
                });
            }
            else if(message == "Success") {
                // Got the response, so were connected over another way
                // No reconnect required
                $('#connect-step-disconnect').find('section.wait').fadeOut(400, function() {
                    $('#connect-step-disconnect').find('section.success').slideDown();
                });
            }
        }
        else if(status == "error") {
            $('#connect-step-disconnect').find('section.failed .error-area').text(message);

            $('#connect-step-disconnect').find('section.wait').fadeOut(400, function() {
                $('#connect-step-disconnect').find('section.failed').slideDown();
            });
        }
        //$('#connect-step-disconnect').find('section.failed .error-area').text(jqXHR.responseJSON.message);
    });
}

function deviceRedirect() {
    $('#connect-step-wait-for-reconnect').find('section.wait').slideDown();

    let connect_retry = 0;
    let max_retry = 15;
    const checkInterval = setInterval(function() {
        // Multicheck
        url = 'http://' + deviceHostname;
        if(connect_retry % 2) {
            url += ".local";
        }

        $.ajax({
            url: url,
            complete: function(jqXHR, textStatus) {
                if(jqXHR.status != 0) {
                    // There may be an error on the page, but the host is alive
                    // Success
                    $('a.device-url').attr('href', url).text(url);
                    $('#connect-step-wait-for-reconnect').find('section.wait').fadeOut(400, function() {
                        $('#connect-step-wait-for-reconnect').find('section.success').slideDown(400, function() {
                            window.location.replace(url);
                        });
                    });
                }
                else {
                    // Failed
                    $('#connect-step-wait-for-reconnect').find('section.wait [data-name="redirect-info"]').text("Retry " + connect_retry + " / " + max_retry);
                    connect_retry++;

                    // only try 10 times stop interval
                    if(connect_retry > max_retry) {
                        clearInterval(checkInterval);
                        $('#connect-step-wait-for-reconnect').find('section.wait').fadeOut(400, function() {
                            $('#connect-step-wait-for-reconnect').find('section.failed').slideDown();
                        });
                    }
                }
            },
            crossDomain: true,
            timeout: 2000 //in milliseconds
        });

    }, 3000);
}

$(document).ready(function() {
    var socket = io();

    $('#settings-wifi-connect').on('hide.bs.modal', function() {
        $('#connect-step-disconnect').find('section').hide();
    });

    $('a.device-url').attr('href', 'http://'+deviceHostname).text(deviceHostname);

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
            const template = $('#settings-wifi-network-template').html();
            const radioOption = template
                .replace(/\[\[ssid\]\]/g, network.ssid)
                .replace(/\[\[band\]\]/g, network.band)
                .replace(/\[\[known\]\]/g, network.known ? '✓' : '')
                .replace(/\[\[signal\]\]/g, signalIcon)
                .replace(/\[\[passwordIcon\]\]/g, passwordIcon);

            const radioOptionElement = $(radioOption);

            const password_required = !(network.known || !network.protected);

            radioOptionElement.on('click', function() {
                selectNetwork($(this).val(), password_required);
            });

            networksDiv.append(radioOptionElement);
        });

        $('#network-list-refresh').prop('disabled', false);
    });

    function selectNetwork(ssid, password_required) {
        if(ssid && !password_required) {
            connect_wifi_gui(ssid);
        }
        else if(ssid) {
            define_wifi(ssid);
        }
        else {
            define_wifi();
        }
    }

    function define_wifi(ssid) {
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
        $('#settings-wifi-define').modal('show');
    }

    $('#network-list-refresh').click(fetchNetworks);

    $('button#other-network').click(function() {
        selectNetwork();
    });

    $('form#connect').on('submit', function(e) {
        e.preventDefault();

        $(this).find('input[type=submit]').prop('disabled', true);

        const ssid = $('#network-ssid').val();
        const password = $('#network-password').val();

        connect_wifi_gui(ssid, password);
    });


    // Initial fetch of networks on page load
    fetchNetworks();


    /*$('#connect-step-disconnect').find('section.wait').fadeIn();
    $('#connect-step-disconnect').find('section.wait').slideUp(400, function() {
        $('#connect-step-disconnect').find('section.success').fadeIn();
    });*/
});


/*$.get(url, function(response) {
    console.log(response);
    // Wir sind noch immer mit dem selben netzwerk verbunden.

    if (response.success) {

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
        alert("No success");
        errorMessageContainer.text(response.error + ': ' + response.details).show();
    }
}).fail(function(error) {
    console.log("A");
    console.log(error);
    alert(error.statusText);
    errorMessageContainer.text('Error: ' + error.responseJSON.message).show();
});*/

/*// Do perform check
// Warte und überprüfe, ob das Gerät unter dem neuen Hostnamen erreichbar ist
let connect_retry = 0;
const checkInterval = setInterval(function() {
    console.log("REQ");
    $.ajax({
        url: `http://mediapi2.local/api/connect`,
        success: function(data){
            console.log("Is available");
            window.location.href = `http://${deviceHostname}.local`;
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.log(jqXHR);
            console.log(textStatus);
            console.log(errorThrown);
            // device not ready
            // textStatus==="timeout"

            // Hopefully CORS error is here.
            // textStatus==="error" && errorThrown===""

            connect_retry++;
            console.log("Connect retry..." + connect_retry);

            // only try 10 times stop interval
            if(connect_retry > 9) {
                clearInterval(checkInterval);
            }
        },
        crossDomain:true,
        timeout: 2000 //in milliseconds
    });

}, 3000);*/
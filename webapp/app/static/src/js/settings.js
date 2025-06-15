// Save settings in cookie
function saveSettingsToCookies() {
    var objectPosition = $('#objectPositionSelect').val();
    var objectFit = $('#objectFitSelect').val();
    document.cookie = "objectPosition=" + objectPosition + "; SameSite=Strict";
    document.cookie = "objectFit=" + objectFit + "; SameSite=Strict";
}

// Load settings from cookie
function loadSettingsFromCookies() {
    var cookies = document.cookie.split(';');
    var settings = {};
    cookies.forEach(function(cookie) {
        var parts = cookie.split('=');
        var key = parts[0].trim();
        var value = parts[1];
        settings[key] = value;
    });
    return settings;
}

// jQuery for Object Position Modal
$(document).ready(function(){
    // TODO: Remove this
    $('#settingsModal').modal('show');

    // Init from cookie settings
    var settings = loadSettingsFromCookies();
    $('#objectPositionSelect').val(settings.objectPosition);
    $('#objectFitSelect').val(settings.objectFit);

    // General configuration
    $.ajaxSetup({
        headers: {
            'X-CSRFToken': csrf_token
        }
    });

});
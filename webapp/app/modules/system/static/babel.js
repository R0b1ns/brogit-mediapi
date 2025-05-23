// TODO: Implement this. Its not in use right now
$('#language-selector').on('change', function() {
    var language = $(this).val();

    // Sende die neue Sprache an den Server
    $.ajax({
        url: '/change_language',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ language: language }),
        success: function(response) {
            // Wenn die Sprache erfolgreich geändert wurde, lade die neuen Übersetzungen
            loadTranslations();
        },
        error: function(error) {
            alert("Fehler beim Wechseln der Sprache");
        }
    });
});

function loadTranslations() {
    $.ajax({
        url: '/get_translations',
        type: 'GET',
        success: function(response) {
            // Durchlaufe alle zurückgegebenen Übersetzungen und aktualisiere die HTML-Elemente
            for (var key in response) {
                // Jedes Element auf der Seite, das eine ID hat und mit einem Übersetzungskey übereinstimmt, wird ersetzt
                var element = $('#' + key);
                if (element.length) {
                    element.text(response[key]);
                }
            }
        },
        error: function(error) {
            alert("Fehler beim Laden der Übersetzungen");
        }
    });
}

$(document).ready(function() {
    loadTranslations();
});
$(document).ready(function() {
  // Wenn ein Tab gezeigt wird, lade die aktuellen Settings
  $('#v-pills-tab button[data-bs-toggle="pill"]').on('shown.bs.tab', function (e) {
    const targetSelector = $(e.target).data('bsTarget');
    const section = $(targetSelector).data('section');
    // loadSettings(section, $(targetSelector));
  });

  // Initiales Laden für aktiven Tab
  const initialSection = $('#settings-container > div.tab-pane.active').data('section');
  if (initialSection) {
    // loadSettings(initialSection, $('#settings-container > div.tab-pane.active'));
  }

  // Änderungsevents (delegated) für alle Sektionen
  // TODO: This is productive some how. Please enable or move it with right selector
/*  $('#settings-container').on('change', 'input, select, textarea', function() {
    const sectionDiv = $(this).closest('[data-section]');
    const section = sectionDiv.data('section');

    if($(this).data('role') == 'form') {
        const id = $(this).attr('id');
        const key = id.replace(`settings-${section}-`, '');
        console.debug("Send data-form: "+key);

        let data = {};

        if ($(this).is(':checkbox')) {
            data[key] = $(this).prop('checked');
        } else {
            data[key] = $(this).val();
        }

        // TODO: Its disabled cause generic handles it
        //update_setting(section, data);
    }
    else {
        // TODO: Its disabled to send whole inputs
        //saveSettings(section, sectionDiv);
    }
  });*/

  // Funktion: Settings laden
  function loadSettings(section, container) {
    $.get(`/api/settings/${section}`, function(data) {
      if (!data || typeof data !== 'object') return;
      // Iteriere über alle Schlüssel im Response-Objekt
      for (const [key, value] of Object.entries(data)) {
        // Finde Input mit passendem ID suffix z.B. settings-ethernet-ip
        const input = container.find(`#settings-${section}-${key}`);
        if (!input.length) continue;

        if (input.is(':checkbox')) {
          input.prop('checked', Boolean(value));
        } else {
          input.val(value);
        }
      }
    });
  }

  // Funktion: Settings speichern
  function saveSettings(section, container) {
    // Sammle alle Inputs in einem Objekt
    let data = {};
    container.find('input, select, textarea').each(function() {
      const id = $(this).attr('id');
      if (!id) return;

      // Extrahiere key z.B. settings-ethernet-ip → ip
      const key = id.replace(`settings-${section}-`, '');
      if ($(this).is(':checkbox')) {
        data[key] = $(this).prop('checked');
      } else {
        data[key] = $(this).val();
      }
    });

    $.ajax({
      url: `/api/settings/${section}`,
      method: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(data),
      success: function(res) {
        console.log(`Settings for ${section} saved.`);
      },
      error: function(err) {
        console.error(`Failed to save settings for ${section}`, err);
      }
    });
  }

  function update_setting(section, data) {
    $.ajax({
      url: `/api/settings/${section}`,
      method: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(data),
      success: function(res) {
        console.log(`Setting for ${section}. saved.`);
      },
      error: function(err) {
        console.error(`Failed to save settings for ${section}`, err);
      }
    });
  }
});

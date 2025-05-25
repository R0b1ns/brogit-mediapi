$(function() {
  const $placeholder = $('#ethernet-placeholder');
  const $settings = $('#ethernet-settings');
  const $saveBtn = $('#settings-ethernet-save');

  let originalData = {};
  let dirtyFields = new Set();
  let dnsSaveTimeout;

  // Hilfsfunktion IP-Validierung (IPv4)
  function isValidIP(ip) {
    const regex = /^(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}$/;
    return regex.test(ip);
  }

  // Hilfsfunktion Netmask Validierung (IPv4 Netmask)
  function isValidNetmask(mask) {
    // Valid subnet masks in decimal notation
    const validMasks = [
      "128.0.0.0","192.0.0.0","224.0.0.0","240.0.0.0","248.0.0.0","252.0.0.0",
      "254.0.0.0","255.0.0.0","255.128.0.0","255.192.0.0","255.224.0.0","255.240.0.0",
      "255.248.0.0","255.252.0.0","255.254.0.0","255.255.0.0","255.255.128.0",
      "255.255.192.0","255.255.224.0","255.255.240.0","255.255.248.0","255.255.252.0",
      "255.255.254.0","255.255.255.0","255.255.255.128","255.255.255.192",
      "255.255.255.224","255.255.255.240","255.255.255.248","255.255.255.252",
      "255.255.255.254","255.255.255.255"
    ];
    return validMasks.includes(mask);
  }

  // Setzt Status der Inputs und Save-Button
    // updateInterfaceInputs() passt Save-Button Sichtbarkeit an:
    function updateInterfaceInputs() {
      const dhcp = $('#settings-ethernet-ip-dhcp').prop('checked');
      $('#settings-ethernet-ip, #settings-ethernet-netmask, #settings-ethernet-gateway').prop('disabled', dhcp);

      if (!dhcp && dirtyFields.size > 0) {
        $saveBtn.removeClass('d-none');
      } else {
        $saveBtn.addClass('d-none');
      }
    }

  // Setzt Status der DNS Inputs
  function updateDnsInputs() {
    const dhcp = $('#settings-ethernet-dns-dhcp').prop('checked');
    $('#settings-ethernet-dns-servers').prop('disabled', dhcp);
  }

  // Lädt Daten vom Backend und zeigt Formular
  function loadSettings() {
    $.getJSON('/module/ethernet/api/settings', function(data) {
      // Status
      if (data.status) {
        $('#settings-ethernet-connected').removeClass('text-danger').addClass('text-success').html('Connected <i class="bi bi-check-circle align-top"></i>');
      } else {
        $('#settings-ethernet-connected').removeClass('text-success').addClass('text-danger').text('Disconnected');
      }

      // Interface
      const iface = data.interface || {};
      $('#settings-ethernet-ip-dhcp').prop('checked', iface.method === 'dhcp');
      $('#settings-ethernet-ip').val(iface.ip || '');
      $('#settings-ethernet-netmask').val(cidrToNetmask(iface.subnet) || '');
      $('#settings-ethernet-gateway').val(iface.gateway || '');

      // DNS
      const dns = data.dns || {};
      $('#settings-ethernet-dns-dhcp').prop('checked', dns.method === 'auto');
      $('#settings-ethernet-dns-servers').val((dns.dns || []).join('\n'));

      // Speichern für Dirty Check
      originalData = {
        ip: $('#settings-ethernet-ip').val(),
        netmask: $('#settings-ethernet-netmask').val(),
        gateway: $('#settings-ethernet-gateway').val(),
        ipDhcp: $('#settings-ethernet-ip-dhcp').prop('checked'),
        dnsDhcp: $('#settings-ethernet-dns-dhcp').prop('checked'),
        dnsServers: $('#settings-ethernet-dns-servers').val()
      };

      dirtyFields.clear();

      updateInterfaceInputs();
      updateDnsInputs();

      // Show real settings & hide shimmer
      $placeholder.hide();
      $settings.removeClass('d-none');
    }).fail(function() {
      alert('Failed to load Ethernet settings.');
    });
  }

  // Helper: CIDR (number) to Netmask string
  function cidrToNetmask(cidr) {
    if (cidr === undefined || cidr === null) return '';
    const mask = [];
    for(let i=0; i<4; i++) {
      if (cidr >= 8) {
        mask.push(255);
        cidr -= 8;
      } else {
        mask.push(256 - Math.pow(2, 8 - cidr));
        cidr = 0;
      }
    }
    return mask.join('.');
  }

  // Prüft Felder & markiert Eingaben als geändert
  function checkDirty(field) {
    let changed = false;
    switch(field) {
      case 'ip':
        changed = $('#settings-ethernet-ip').val() !== originalData.ip;
        break;
      case 'netmask':
        changed = $('#settings-ethernet-netmask').val() !== originalData.netmask;
        break;
      case 'gateway':
        changed = $('#settings-ethernet-gateway').val() !== originalData.gateway;
        break;
      case 'ipDhcp':
        changed = $('#settings-ethernet-ip-dhcp').prop('checked') !== originalData.ipDhcp;
        break;
      case 'dnsDhcp':
        changed = $('#settings-ethernet-dns-dhcp').prop('checked') !== originalData.dnsDhcp;
        break;
      case 'dnsServers':
        changed = $('#settings-ethernet-dns-servers').val() !== originalData.dnsServers;
        break;
    }
    if (changed) {
      dirtyFields.add(field);
      markFieldChanged(field, true);
    } else {
      dirtyFields.delete(field);
      markFieldChanged(field, false);
    }
  }

  // Markiert Input farblich, wenn geändert
  function markFieldChanged(field, changed) {
    let $el;
    switch(field) {
      case 'ip': $el = $('#settings-ethernet-ip'); break;
      case 'netmask': $el = $('#settings-ethernet-netmask'); break;
      case 'gateway': $el = $('#settings-ethernet-gateway'); break;
      case 'ipDhcp': $el = $('#settings-ethernet-ip-dhcp'); break;
      case 'dnsDhcp': $el = $('#settings-ethernet-dns-dhcp'); break;
      case 'dnsServers': $el = $('#settings-ethernet-dns-servers'); break;
      default: return;
    }
    if (changed) {
      $el.addClass('border border-warning');
    } else {
      $el.removeClass('border border-warning');
    }
  }

  // Speichert Interface Einstellungen
  function saveInterface() {
    const method = $('#settings-ethernet-ip-dhcp').prop('checked') ? 'dhcp' : 'manual';
    const ip = $('#settings-ethernet-ip').val();
    const netmask = $('#settings-ethernet-netmask').val();
    const gateway = $('#settings-ethernet-gateway').val();

    // Validierung
    if (method === 'manual') {
      if (!isValidIP(ip)) {
        alert('Invalid IP address');
        return;
      }
      if (!isValidNetmask(netmask)) {
        alert('Invalid netmask');
        return;
      }
      if (gateway && !isValidIP(gateway)) {
        alert('Invalid gateway address');
        return;
      }
    }

    $.ajax({
      url: '/module/ethernet/api/settings/interface',
      method: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({method, ip, netmask, gateway}),
      success: function(resp) {
        if (resp.success) {
          alert('Settings saved successfully.');
          // Update original data & reset dirty
          originalData.ip = ip;
          originalData.netmask = netmask;
          originalData.gateway = gateway;
          originalData.ipDhcp = method === 'dhcp';
          dirtyFields.clear();
          updateInterfaceInputs();
          markFieldChanged('ip', false);
          markFieldChanged('netmask', false);
          markFieldChanged('gateway', false);
          markFieldChanged('ipDhcp', false);
          $saveBtn.addClass('d-none');
        } else {
          alert('Failed to save settings.');
        }
      },
      error: function() {
        alert('Error saving settings.');
      }
    });
  }

  // Speichert DNS Einstellungen live mit Debounce
  function saveDns() {
    clearTimeout(dnsSaveTimeout);
    dnsSaveTimeout = setTimeout(function() {
      const method = $('#settings-ethernet-dns-dhcp').prop('checked') ? 'auto' : 'manual';
      const serversRaw = $('#settings-ethernet-dns-servers').val().trim();
      const dnsServers = serversRaw ? serversRaw.split('\n').map(s => s.trim()).filter(Boolean) : [];

      // Validierung DNS IPs (optional)
      for (const ip of dnsServers) {
        if (!isValidIP(ip)) {
          alert('Invalid DNS server IP: ' + ip);
          return;
        }
      }

      $.ajax({
        url: '/module/ethernet/api/settings/dns',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({method, dns: dnsServers}),
        success: function(resp) {
          if (resp.success) {
            originalData.dnsDhcp = method === 'auto';
            originalData.dnsServers = $('#settings-ethernet-dns-servers').val();
            dirtyFields.delete('dnsDhcp');
            dirtyFields.delete('dnsServers');
            markFieldChanged('dnsDhcp', false);
            markFieldChanged('dnsServers', false);
          } else {
            alert('Failed to save DNS settings.');
          }
        },
        error: function() {
          alert('Error saving DNS settings.');
        }
      });
    }, 800);
  }

  // Event Listeners

  // DHCP Toggle Interface
  $('#settings-ethernet-ip-dhcp').change(function() {
    checkDirty('ipDhcp');
    updateInterfaceInputs();
  });

  // Inputs Interface
  $('#settings-ethernet-ip, #settings-ethernet-netmask, #settings-ethernet-gateway').on('input', function() {
    const fieldMap = {
      'settings-ethernet-ip': 'ip',
      'settings-ethernet-netmask': 'netmask',
      'settings-ethernet-gateway': 'gateway'
    };
    checkDirty(fieldMap[this.id]);
    updateInterfaceInputs();
  });

  // Save Button
  $saveBtn.click(function() {
    saveInterface();
  });

  // DHCP Toggle DNS
  $('#settings-ethernet-dns-dhcp').change(function() {
    checkDirty('dnsDhcp');
    updateDnsInputs();
    saveDns();
  });

  // DNS Servers textarea
  $('#settings-ethernet-dns-servers').on('input', function() {
    checkDirty('dnsServers');
    saveDns();
  });

  // Initial load
  //loadSettings();

  load_manual = loadSettings
});

load_manual = null
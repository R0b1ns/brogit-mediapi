$(() => {
  $.fn.genericInputAsFormHandler = function () {
    return this.each(function () {
      const $el = $(this);

      const action = $el.data('action');
      const method = ($el.data('method') || 'POST').toUpperCase();
      const selector = $el.data('response-target');
      const successCallback = $el.data('on-success');
      const errorCallback = $el.data('on-error');
      const $response = selector ? $(selector) : $();
      const isAutoDisable = !$el.is('[data-no-disable]');
      const name = $el.attr('name');

      let timeout = null;

      const setStateClass = (state) => {
        $el.removeClass('is-valid is-invalid');
        if (state === 'success') $el.addClass('is-valid');
        if (state === 'error') $el.addClass('is-invalid');
      };

      const send = () => {
        clearTimeout(timeout);

        let payload;
        if (name) {
          let value;
          if ($el.is(':checkbox')) {
            value = $el.prop('checked');
          } else {
            value = $el.val();
          }
          payload = { [name]: value };
        } else {
          payload = {};
        }

        if (isAutoDisable) $el.prop('disabled', true);
        $.ajax({
          url: action,
          method,
          contentType: 'application/json',
          data: JSON.stringify(payload),
          success: () => {
            $response.text('');
            setStateClass('success');
            if (successCallback && typeof window[successCallback] === 'function') {
              window[successCallback]($el);
            }
          },
          error: xhr => {
            const msg = xhr.responseJSON?.message || 'Unexpected error';
            console.error('Error:', msg);
            $response.text(msg);
            setStateClass('error');
            if (errorCallback && typeof window[errorCallback] === 'function') {
              window[errorCallback]($el, msg);
            }
          },
          complete: () => {
            if (isAutoDisable) $el.prop('disabled', false);
          }
        });
      };

      const schedule = () => {
        clearTimeout(timeout);
        timeout = setTimeout(send, 3000);
      };

      const resetStateClass = () => {
        $el.removeClass('is-valid is-invalid');
      };

      if ($el.is('input[type="text"], textarea')) {
        $el.on('input', () => {
          resetStateClass();
          schedule();
        });
        $el.on('blur', send);
        $el.on('keydown', e => {
          if (e.key === 'Enter') send();
        });
      } else if ($el.is('button')) {
        $el.on('click', () => {
          resetStateClass();
          send();
        });
      } else {
        $el.on('change', () => {
          resetStateClass();
          send();
        });
      }
    });
  };

  $('input[data-role="form"], select[data-role="form"], textarea[data-role="form"], button[data-role="form"]').genericInputAsFormHandler();
});

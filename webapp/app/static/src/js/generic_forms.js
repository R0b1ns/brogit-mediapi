$(() => {
  $.fn.genericFormHandler = function () {
    return this.each(function () {
      const $form = $(this);
      const $submit = $form.find('button[type="submit"], input[type="submit"]');
      if (!$submit.length) return;

      const selector = $form.attr('data-response-target');
      const $response = selector ? $(selector) : $form.find('[data-response-target]');
      console.log($form.attr('data-response-target'));
      console.log($response);
      const useFeedback = !$submit.is('[data-no-feedback]');
      const isAutoDisable = !$submit.is('[data-no-disable]');
      const useOutline = $submit.is('[class*="btn-outline-"]');

      let initialData = $form.serialize();
      let resetTimer = null;

      const makeBtnClass = base => useOutline ? `btn-outline-${base}` : `btn-${base}`;

      const states = {
        idle:    { color: 'secondary', icon: 'bi-dash', text: '' },
        dirty:   { color: 'primary',   icon: 'bi-pencil-square', text: 'Save' },
        success: { color: 'success',   icon: 'bi-check-lg', text: 'Saved' },
        error:   { color: 'danger',    icon: 'bi-exclamation-triangle', text: 'Error' },
        retry:   { color: 'warning',   icon: 'bi-exclamation-circle', text: 'Retry' }
      };

      const setSubmitContent = html => {
        $submit.each(function () {
          if (this.tagName === 'INPUT') {
            $(this).val(html.replace(/<[^>]+>/g, ''));
          } else {
            $(this).html(html);
          }
        });
      };

      const setButtonState = (state) => {
        if (!useFeedback) return;

        const s = states[state];
        if (!s) return;

        $submit.stop(true, true)
          .removeClass((_, cls) => cls.split(' ').filter(c => c.startsWith('btn-')).join(' '))
          .addClass(makeBtnClass(s.color));

        setSubmitContent(`<i class="bi ${s.icon} me-1"></i>${s.text}`);

        if (state === 'success' || state === 'error') {
          $submit.clearQueue().delay(3000).queue(next => {
            if (state === 'success') {
              const idle = states.idle;
              $submit.removeClass(makeBtnClass(s.color)).addClass(makeBtnClass(idle.color));
              setSubmitContent(`<i class="bi ${idle.icon} me-1"></i>${idle.text}`);
            } else if (state === 'error') {
              const retry = states.retry;
              $submit.removeClass(makeBtnClass(s.color)).addClass(makeBtnClass(retry.color));
              setSubmitContent(`<i class="bi ${retry.icon} me-1"></i>${retry.text}`);
            }
            next();
          });
        }
      };

      const updateState = (updateButton = true) => {
        if (!isAutoDisable) return;
        const changed = $form.serialize() !== initialData;
        $submit.prop('disabled', !changed);
        if (useFeedback && updateButton) setButtonState(changed ? 'dirty' : 'idle');
      };

      if (isAutoDisable) $submit.prop('disabled', true);
      updateState();

      $form.on('input change', updateState);

      $form.on('submit', e => {
        e.preventDefault();
        if (isAutoDisable) $submit.prop('disabled', true);

        const originalHtml = $submit.is('input') ? $submit.val() : $submit.html();
        setSubmitContent('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>');

        const action = $form.attr('action');
        const method = ($form.attr('method') || 'GET').toUpperCase();
        if (!action) {
          console.error('Missing form action');
          $submit.prop('disabled', false);
          setSubmitContent(originalHtml);
          return;
        }

        const data = Object.fromEntries(new FormData($form[0]).entries());

        $.ajax({
          url: action,
          method,
          contentType: 'application/json',
          data: JSON.stringify(data),
          success: res => {
            console.log('Success:', res);
            initialData = $form.serialize();
            $response.text('');
            if (useFeedback) setButtonState('success');
          },
          error: xhr => {
            const msg = xhr.responseJSON?.message || 'Unexpected error';
            console.error('Error:', msg);
            $response.text(msg);
            if (useFeedback) setButtonState('error');
          },
          complete: () => updateState(false),
        });
      });
    });
  };

  $('form[data-method="generic"]').genericFormHandler();
});

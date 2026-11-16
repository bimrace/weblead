(function () {
  'use strict';

  var button = document.querySelector('[data-copy-email]');
  if (!button) return;

  var status = document.getElementById('copy-status');
  function failed(err) {
    status.textContent = 'Clipboard access failed. Please copy the email address above.';
    if (window.console && window.console.error) {
      window.console.error('[BIMRACE] Could not copy associate email:', err);
    }
  }

  button.addEventListener('click', function () {
    if (!navigator.clipboard || !navigator.clipboard.writeText) {
      failed('Clipboard API is unavailable in this browser.');
      return;
    }
    try {
      navigator.clipboard.writeText(button.getAttribute('data-copy-email')).then(function () {
        status.textContent = 'Email address copied to clipboard.';
      }).catch(failed);
    } catch (err) {
      failed(err);
    }
  });
})();

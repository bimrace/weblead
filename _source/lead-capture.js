/* ============================================================================
   BIMRACE — public lead capture
   Attaches to any <form data-lead-form="<form_code>"> on the marketing site.

   Only the anon key is used here. It is safe to publish: RLS grants anonymous
   users INSERT on crm.enquiry_submissions and nothing else, so this key cannot
   read the pipeline, cannot set a lead score, status or owner, and cannot
   touch crm.leads. The service_role key must never appear in this file.
   ========================================================================== */
(function () {
  'use strict';

  var CFG = window.BIMRACE_CONFIG || {};
  if (!CFG.supabaseUrl || !CFG.supabaseAnonKey) return;

  var REST = CFG.supabaseUrl.replace(/\/$/, '') + '/rest/v1/enquiry_submissions';
  var FN   = CFG.supabaseUrl.replace(/\/$/, '') + '/functions/v1/lead-intake';

  /* ------------------------------------------------------- attribution --- */
  var STORE = 'bimrace_attr';

  function readParams() {
    var q = new URLSearchParams(location.search), o = {};
    ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'].forEach(function (k) {
      if (q.get(k)) o[k] = q.get(k);
    });
    return o;
  }

  /* First touch is written once and never overwritten; last touch updates on
     every visit. Original attribution has to survive later campaign clicks. */
  function attribution() {
    var saved;
    try { saved = JSON.parse(sessionStorage.getItem(STORE) || 'null'); } catch (e) { saved = null; }
    var now = readParams();
    var first = (saved && saved.first) || Object.assign({
      landing_page: location.pathname,
      referrer: document.referrer || null,
      at: new Date().toISOString()
    }, now);
    var last = Object.assign({ landing_page: location.pathname }, now);
    var data = { first: first, last: last };
    try { sessionStorage.setItem(STORE, JSON.stringify(data)); } catch (e) { /* private mode */ }

    return {
      source_code: first.utm_source ? 'campaign'
        : (document.referrer.indexOf('google.') > -1 ? 'google_search'
        : (document.referrer.indexOf('linkedin.') > -1 ? 'linkedin' : 'website')),
      utm_source: first.utm_source || null,
      utm_medium: first.utm_medium || null,
      utm_campaign: first.utm_campaign || null,
      utm_content: first.utm_content || null,
      utm_term: first.utm_term || null,
      landing_page: first.landing_page,
      referrer: first.referrer
    };
  }

  /* ----------------------------------------------------------- helpers --- */
  function uuid() {
    if (crypto.randomUUID) return crypto.randomUUID();
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
      var r = Math.random() * 16 | 0;
      return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
    });
  }

  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  var FREE_MAIL = /@(gmail|yahoo|outlook|hotmail|live|icloud|aol|proton|protonmail)\./i;

  function setError(field, message) {
    var box = field.closest('.field');
    if (!box) return;
    var err = box.querySelector('.err');
    field.setAttribute('aria-invalid', message ? 'true' : 'false');
    if (err) err.textContent = message || '';
  }

  function validate(form) {
    var bad = [];
    form.querySelectorAll('[data-required]').forEach(function (f) {
      var v = (f.value || '').trim();
      var msg = '';
      if (!v) msg = 'This field is required.';
      else if (f.type === 'email' && !EMAIL_RE.test(v)) msg = 'Enter a valid email address.';
      else if (f.dataset.minlen && v.length < +f.dataset.minlen)
        msg = 'Please give a little more detail.';
      setError(f, msg);
      if (msg) bad.push(f);
    });

    /* Business email is a scoring signal, not a hard requirement — warn, allow. */
    var email = form.querySelector('input[type=email]');
    if (email && email.value && FREE_MAIL.test(email.value)) {
      var hint = form.querySelector('[data-free-mail-hint]');
      if (hint) hint.hidden = false;
    }
    return bad;
  }

  function collect(form) {
    var payload = {};
    form.querySelectorAll('[name]').forEach(function (f) {
      if (!f.name || f.name.indexOf('_') === 0) return;
      if (f.type === 'checkbox') {
        if (!f.checked) return;
        (payload[f.name] = payload[f.name] || []).push(f.value);
      } else if (f.type === 'radio') {
        if (f.checked) payload[f.name] = f.value;
      } else if (f.multiple) {
        payload[f.name] = Array.from(f.selectedOptions).map(function (o) { return o.value; });
      } else {
        var v = (f.value || '').trim();
        if (v) payload[f.name] = v;
      }
    });
    return payload;
  }

  function status(form, kind, text) {
    var box = form.querySelector('[data-form-status]');
    if (!box) return;
    box.hidden = false;
    box.className = 'form-status form-status--' + kind;
    box.textContent = text;
    box.setAttribute('role', kind === 'error' ? 'alert' : 'status');
  }

  /* ------------------------------------------------------------ submit --- */
  function init(form) {
    var formCode = form.getAttribute('data-lead-form');
    var key = uuid();          // one key per form instance = idempotency
    var sending = false;

    form.querySelectorAll('[data-required]').forEach(function (f) {
      f.addEventListener('blur', function () { validate(form); });
      f.addEventListener('input', function () {
        if (f.getAttribute('aria-invalid') === 'true') validate(form);
      });
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (sending) return;                       // double-click guard

      var bad = validate(form);
      if (bad.length) {
        bad[0].focus();
        status(form, 'error', 'Please correct the highlighted fields.');
        return;
      }

      var btn = form.querySelector('[type=submit]');
      var label = btn ? btn.textContent : '';
      sending = true;
      if (btn) { btn.disabled = true; btn.textContent = 'Sending…'; }
      status(form, 'info', 'Sending your enquiry…');

      var body = Object.assign({
        submission_key: key,
        form_code: formCode,
        payload: collect(form)
      }, attribution());

      var useFn = CFG.useEdgeFunction === true;
      var url = useFn ? FN : REST;
      var headers = { 'content-type': 'application/json' };
      if (!useFn) {
        headers.apikey = CFG.supabaseAnonKey;
        headers.Authorization = 'Bearer ' + CFG.supabaseAnonKey;
        headers['Content-Profile'] = 'crm';
        headers.Prefer = 'return=minimal';
      } else {
        headers.Authorization = 'Bearer ' + CFG.supabaseAnonKey;
      }

      var ctrl = new AbortController();
      var timer = setTimeout(function () { ctrl.abort(); }, 15000);

      fetch(url, { method: 'POST', headers: headers, body: JSON.stringify(body), signal: ctrl.signal })
        .then(function (r) {
          clearTimeout(timer);
          if (r.status === 429) throw new Error('rate');
          if (r.status === 409) return { duplicate: true };   // same key resent
          if (!r.ok) throw new Error('http_' + r.status);
          return r.status === 204 ? {} : r.json().catch(function () { return {}; });
        })
        .then(function () {
          form.hidden = true;
          var done = document.querySelector('[data-form-success]');
          if (done) { done.hidden = false; done.focus(); }
          else if (CFG.thankYouUrl) location.href = CFG.thankYouUrl;
        })
        .catch(function (err) {
          sending = false;
          if (btn) { btn.disabled = false; btn.textContent = label; }
          var msg = err.name === 'AbortError'
            ? 'The request timed out. Please check your connection and try again.'
            : err.message === 'rate'
              ? 'Too many enquiries from this connection. Please try again later, or email ' + (CFG.email || 'us') + '.'
              : 'We could not send your enquiry. Please email ' + (CFG.email || 'us') + ' and we will pick it up.';
          status(form, 'error', msg);
          /* Technical detail stays in the console; the visitor never sees a
             database error. */
          if (window.console) console.error('[BIMRACE lead]', err);
        });
    });
  }

  function boot() {
    document.querySelectorAll('form[data-lead-form]').forEach(init);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();

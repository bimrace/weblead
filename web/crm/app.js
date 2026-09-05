/* ============================================================================
   BIMRACE CRM — internal operations console
   Vanilla JS + supabase-js. Anon key only; every read is gated by RLS, so a
   user sees exactly what their role permits and nothing else.
   ========================================================================== */
const CFG = window.BIMRACE_CONFIG || {};

/* Fail loudly and legibly rather than with an undefined-property error if the
   supabase-js CDN is blocked or config.js was never filled in. */
if (!window.supabase || !CFG.supabaseUrl || !CFG.supabaseAnonKey) {
  document.body.innerHTML =
    '<div class="login"><div class="login__box">' +
    '<h1>Console unavailable</h1>' +
    '<p class="muted">The Supabase client could not be initialised. Check that ' +
    'config.js contains your project URL and anon key, and that the supabase-js ' +
    'script loaded.</p></div></div>';
  throw new Error('BIMRACE CRM: supabase client unavailable');
}

const sb = window.supabase.createClient(CFG.supabaseUrl, CFG.supabaseAnonKey, {
  db: { schema: 'crm' }, auth: { persistSession: true, autoRefreshToken: true }
});

const $ = (s, c = document) => c.querySelector(s);
const $$ = (s, c = document) => [...c.querySelectorAll(s)];
const esc = s => String(s ?? '').replace(/[&<>"']/g, m =>
  ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[m]));
const fmtDate = d => d ? new Date(d).toLocaleDateString('en-GB',
  { day: '2-digit', month: 'short', year: 'numeric' }) : '—';
const fmtWhen = d => d ? new Date(d).toLocaleString('en-GB',
  { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' }) : '—';

const STAGES = ['new', 'contacted', 'qualifying', 'qualified', 'discovery',
  'scope_defined', 'proposal_required', 'proposal_sent', 'negotiation', 'won', 'lost'];

let ME = null;

/* ------------------------------------------------------------------ auth -- */
async function signIn(e) {
  e.preventDefault();
  const btn = $('#login-btn'); btn.disabled = true; btn.textContent = 'Signing in…';
  const { error } = await sb.auth.signInWithPassword({
    email: $('#login-email').value.trim(), password: $('#login-password').value
  });
  btn.disabled = false; btn.textContent = 'Sign in';
  if (error) { $('#login-error').textContent = 'Sign-in failed. Check your credentials.'; return; }
  await start();
}

async function loadMe() {
  const { data: { user } } = await sb.auth.getUser();
  if (!user) return null;
  const { data } = await sb.from('app_users').select('*').eq('id', user.id).maybeSingle();
  return data || { id: user.id, email: user.email, role: 'viewer', full_name: user.email };
}

/* ------------------------------------------------------------ dashboard -- */
async function viewDashboard() {
  const { data, error } = await sb.rpc('fn_dashboard_metrics');
  if (error) return fail(error);
  const m = data || {};
  const card = (k, v, hint) => `<article class="metric"><p class="metric__k">${esc(k)}</p>
    <p class="metric__v">${v ?? 0}</p>${hint ? `<p class="metric__h">${esc(hint)}</p>` : ''}</article>`;

  const dist = (title, obj) => {
    const rows = Object.entries(obj || {}).sort((a, b) => b[1] - a[1]);
    if (!rows.length) return '';
    const max = Math.max(...rows.map(r => r[1]));
    return `<section class="panel"><h2>${esc(title)}</h2><div class="bars">` +
      rows.map(([k, v]) => `<div class="bar"><span class="bar__k">${esc(k)}</span>
        <span class="bar__t"><i style="width:${(v / max * 100).toFixed(1)}%"></i></span>
        <span class="bar__v">${v}</span></div>`).join('') + '</div></section>';
  };

  $('#view').innerHTML = `
    <h1 class="page-title">Dashboard</h1>
    <div class="metrics">
      ${card('New today', m.new_today)}
      ${card('New this week', m.new_this_week)}
      ${card('Open leads', m.open)}
      ${card('Hot', m.hot, 'score 76+')}
      ${card('Qualified', m.qualified)}
      ${card('Proposals open', m.proposals_open)}
      ${card('Follow-ups due', m.followups_due)}
      ${card('Overdue', m.followups_overdue)}
      ${card('Won', m.won)}
      ${card('Lost', m.lost)}
      ${card('India', m.india)}
      ${card('International', m.international)}
    </div>
    <div class="grid-2">
      ${dist('Leads by status', m.by_status)}
      ${dist('Leads by service', m.by_type)}
      ${dist('Leads by country', m.by_country)}
      ${dist('Leads by source', m.by_source)}
    </div>`;
}

/* ---------------------------------------------------------------- leads -- */
async function viewLeads() {
  $('#view').innerHTML = `<h1 class="page-title">Leads</h1>
    <div class="toolbar">
      <input id="q" type="search" placeholder="Search company, contact or email…" aria-label="Search leads">
      <select id="f-status" aria-label="Filter by status"><option value="">All statuses</option>
        ${STAGES.map(s => `<option value="${s}">${s.replace(/_/g, ' ')}</option>`).join('')}</select>
      <select id="f-geo" aria-label="Filter by geography"><option value="">India + International</option>
        <option value="in">India only</option><option value="intl">International only</option></select>
    </div>
    <div id="lead-rows" class="table-wrap"><p class="muted">Loading…</p></div>`;

  const run = async () => {
    let q = sb.from('leads').select(
      'id,lead_number,company_name,contact_name,email,country_code,is_international,' +
      'lead_type,status,priority,lead_score,score_band,created_at,next_follow_up_at,assigned_to'
    ).order('created_at', { ascending: false }).limit(200);

    const s = $('#f-status').value, g = $('#f-geo').value, t = $('#q').value.trim();
    if (s) q = q.eq('status', s);
    if (g === 'in') q = q.eq('country_code', 'IN');
    if (g === 'intl') q = q.eq('is_international', true);
    if (t) q = q.or(`company_name.ilike.%${t}%,contact_name.ilike.%${t}%,email.ilike.%${t}%`);

    const { data, error } = await q;
    if (error) return fail(error);
    $('#lead-rows').innerHTML = data.length ? `
      <table class="table"><thead><tr>
        <th>Lead</th><th>Company</th><th>Contact</th><th>Service</th>
        <th>Geo</th><th>Score</th><th>Status</th><th>Received</th></tr></thead><tbody>
        ${data.map(l => `<tr data-id="${l.id}" tabindex="0">
          <td class="mono">${esc(l.lead_number)}</td>
          <td>${esc(l.company_name || '—')}</td>
          <td>${esc(l.contact_name || '—')}<br><span class="muted">${esc(l.email || '')}</span></td>
          <td>${esc((l.lead_type || '—').replace(/_/g, ' '))}</td>
          <td>${esc(l.country_code || '—')}${l.is_international ? ' <span class="tag">INT</span>' : ''}</td>
          <td><span class="score score--${l.score_band}">${l.lead_score}</span></td>
          <td><span class="pill pill--${l.status}">${esc(l.status.replace(/_/g, ' '))}</span></td>
          <td class="muted">${fmtDate(l.created_at)}</td></tr>`).join('')}
      </tbody></table>` : '<p class="muted">No leads match these filters.</p>';

    $$('#lead-rows tr[data-id]').forEach(r => {
      const go = () => location.hash = '#/lead/' + r.dataset.id;
      r.addEventListener('click', go);
      r.addEventListener('keydown', e => { if (e.key === 'Enter') go(); });
    });
  };

  ['#q', '#f-status', '#f-geo'].forEach(sel => {
    const el = $(sel);
    el.addEventListener(sel === '#q' ? 'input' : 'change', debounce(run, 250));
  });
  run();
}

/* ------------------------------------------------------------- pipeline -- */
async function viewPipeline() {
  const cols = STAGES.filter(s => s !== 'lost');
  const { data, error } = await sb.from('leads').select(
    'id,lead_number,company_name,contact_name,lead_type,country_code,status,priority,lead_score,score_band,next_follow_up_at'
  ).not('status', 'in', '(spam,duplicate,not_qualified)').order('lead_score', { ascending: false });
  if (error) return fail(error);

  $('#view').innerHTML = `<h1 class="page-title">Pipeline</h1>
    <p class="muted">Drag a card to change its stage. Every move is written to the status history.</p>
    <div class="board">${cols.map(st => `
      <section class="col" data-status="${st}">
        <h2>${st.replace(/_/g, ' ')} <span class="count">${data.filter(l => l.status === st).length}</span></h2>
        <div class="col__drop" data-status="${st}">
          ${data.filter(l => l.status === st).map(cardHtml).join('')}
        </div></section>`).join('')}</div>`;

  $$('.card').forEach(c => {
    c.addEventListener('dragstart', e => { e.dataTransfer.setData('text/plain', c.dataset.id); c.classList.add('dragging'); });
    c.addEventListener('dragend', () => c.classList.remove('dragging'));
    c.addEventListener('click', () => location.hash = '#/lead/' + c.dataset.id);
  });
  $$('.col__drop').forEach(z => {
    z.addEventListener('dragover', e => { e.preventDefault(); z.classList.add('over'); });
    z.addEventListener('dragleave', () => z.classList.remove('over'));
    z.addEventListener('drop', async e => {
      e.preventDefault(); z.classList.remove('over');
      const id = e.dataTransfer.getData('text/plain');
      const { error } = await sb.from('leads').update({ status: z.dataset.status }).eq('id', id);
      if (error) return fail(error);
      viewPipeline();
    });
  });
}

const cardHtml = l => `<article class="card" draggable="true" data-id="${l.id}">
  <p class="card__co">${esc(l.company_name || l.contact_name || 'Unnamed')}</p>
  <p class="card__meta">${esc((l.lead_type || '').replace(/_/g, ' '))} · ${esc(l.country_code || '??')}</p>
  <p class="card__foot"><span class="score score--${l.score_band}">${l.lead_score}</span>
    <span class="mono muted">${esc(l.lead_number)}</span></p>
  ${l.next_follow_up_at ? `<p class="card__fu">Follow-up ${fmtDate(l.next_follow_up_at)}</p>` : ''}
</article>`;

/* ---------------------------------------------------------- lead detail -- */
async function viewLead(id) {
  const [lead, notes, tasks, acts, hist, score] = await Promise.all([
    sb.from('leads').select('*').eq('id', id).maybeSingle(),
    sb.from('lead_notes').select('*').eq('lead_id', id).order('created_at', { ascending: false }),
    sb.from('lead_tasks').select('*').eq('lead_id', id).order('due_at'),
    sb.from('activities').select('*').eq('lead_id', id).order('occurred_at', { ascending: false }).limit(50),
    sb.from('lead_status_history').select('*').eq('lead_id', id).order('changed_at', { ascending: false }),
    sb.from('lead_score_history').select('*').eq('lead_id', id).order('computed_at', { ascending: false }).limit(1)
  ]);
  if (lead.error) return fail(lead.error);
  const l = lead.data;
  if (!l) { $('#view').innerHTML = '<p class="muted">Lead not found, or your role cannot view it.</p>'; return; }

  const rules = score.data?.[0]?.breakdown?.rules || [];
  const row = (k, v) => v ? `<div class="kv"><dt>${esc(k)}</dt><dd>${esc(v)}</dd></div>` : '';

  $('#view').innerHTML = `
    <a class="back" href="#/leads">← All leads</a>
    <header class="lead-head">
      <div><h1 class="page-title">${esc(l.company_name || l.contact_name || 'Lead')}</h1>
        <p class="muted mono">${esc(l.lead_number)} · received ${fmtWhen(l.created_at)}</p></div>
      <div class="lead-head__r">
        <span class="score score--${l.score_band} score--lg">${l.lead_score}</span>
        <select id="set-status" aria-label="Lead status">
          ${STAGES.concat(['on_hold', 'not_qualified', 'spam', 'duplicate'])
            .map(s => `<option value="${s}"${s === l.status ? ' selected' : ''}>${s.replace(/_/g, ' ')}</option>`).join('')}
        </select>
      </div>
    </header>

    <div class="grid-2">
      <section class="panel"><h2>Enquiry</h2><dl class="kvs">
        ${row('Contact', l.contact_name)}${row('Email', l.email)}${row('Phone', l.phone)}
        ${row('Job title', l.job_title)}${row('Country', l.country_code)}${row('City', l.city)}
        ${row('Service', (l.lead_type || '').replace(/_/g, ' '))}
        ${row('Project type', l.project_type)}${row('Stage', l.project_stage)}
        ${row('Disciplines', (l.disciplines || []).join(', '))}
        ${row('Services', (l.service_interest || []).join(', '))}
        ${row('Budget', l.estimated_budget ? `${l.currency || ''} ${l.estimated_budget}` : '')}
        ${row('Required by', fmtDate(l.required_delivery_date))}
      </dl>
      ${l.message ? `<h3>Message</h3><p class="msg">${esc(l.message)}</p>` : ''}</section>

      <section class="panel"><h2>Why this score</h2>
        ${rules.length ? `<ul class="rules">${rules.map(r =>
          `<li><span class="pts ${r.points < 0 ? 'neg' : 'pos'}">${r.points > 0 ? '+' : ''}${r.points}</span>
           ${esc(r.label)}</li>`).join('')}</ul>` : '<p class="muted">No scoring history.</p>'}
        <h2 style="margin-top:24px">Status history</h2>
        <ul class="timeline">${(hist.data || []).map(h =>
          `<li><span class="muted mono">${fmtWhen(h.changed_at)}</span>
            ${esc(h.from_status || 'created')} → <strong>${esc(h.to_status)}</strong></li>`).join('') ||
          '<li class="muted">No transitions yet.</li>'}</ul></section>
    </div>

    <div class="grid-2">
      <section class="panel"><h2>Notes</h2>
        <form id="note-form"><textarea id="note-body" rows="3" placeholder="Add an internal note…" required></textarea>
          <button class="btn btn--sm" type="submit">Add note</button></form>
        <ul class="notes">${(notes.data || []).map(n =>
          `<li><p>${esc(n.body)}</p><p class="muted mono">${fmtWhen(n.created_at)}</p></li>`).join('') ||
          '<li class="muted">No notes yet.</li>'}</ul></section>

      <section class="panel"><h2>Follow-ups</h2>
        <form id="task-form" class="task-form">
          <input id="task-title" placeholder="Follow-up action" required>
          <input id="task-due" type="date" required>
          <button class="btn btn--sm" type="submit">Schedule</button></form>
        <ul class="tasks">${(tasks.data || []).map(t =>
          `<li class="${t.status === 'pending' && new Date(t.due_at) < new Date() ? 'overdue' : ''}">
            <label><input type="checkbox" data-task="${t.id}" ${t.status === 'completed' ? 'checked' : ''}>
            ${esc(t.title)}</label>
            <span class="muted mono">${fmtDate(t.due_at)}</span></li>`).join('') ||
          '<li class="muted">Nothing scheduled.</li>'}</ul></section>
    </div>

    <section class="panel"><h2>Activity timeline</h2>
      <ul class="timeline">${(acts.data || []).map(a =>
        `<li><span class="muted mono">${fmtWhen(a.occurred_at)}</span>
          <strong>${esc(a.activity_type.replace(/_/g, ' '))}</strong> — ${esc(a.summary)}</li>`).join('')}</ul>
    </section>

    ${l.status !== 'won' ? `<button class="btn btn--primary" id="convert">Convert to project</button>` : ''}`;

  $('#set-status').addEventListener('change', async e => {
    const { error } = await sb.from('leads').update({ status: e.target.value }).eq('id', id);
    if (error) return fail(error);
    viewLead(id);
  });

  $('#note-form').addEventListener('submit', async e => {
    e.preventDefault();
    const { error } = await sb.from('lead_notes')
      .insert({ lead_id: id, body: $('#note-body').value.trim(), author_id: ME.id });
    if (error) return fail(error);
    viewLead(id);
  });

  $('#task-form').addEventListener('submit', async e => {
    e.preventDefault();
    const due = new Date($('#task-due').value).toISOString();
    const { error } = await sb.from('lead_tasks').insert({
      lead_id: id, title: $('#task-title').value.trim(), due_at: due,
      owner_id: ME.id, created_by: ME.id
    });
    if (error) return fail(error);
    await sb.from('leads').update({ next_follow_up_at: due }).eq('id', id);
    viewLead(id);
  });

  $$('[data-task]').forEach(cb => cb.addEventListener('change', async () => {
    const { error } = await sb.from('lead_tasks').update({
      status: cb.checked ? 'completed' : 'pending',
      completed_at: cb.checked ? new Date().toISOString() : null
    }).eq('id', cb.dataset.task);
    if (error) fail(error);
  }));

  const conv = $('#convert');
  if (conv) conv.addEventListener('click', async () => {
    if (!confirm('Convert this lead to a project and mark it WON?')) return;
    const { error } = await sb.rpc('fn_convert_lead_to_project', { p_lead_id: id, p_name: null });
    if (error) return fail(error);
    viewLead(id);
  });
}

/* --------------------------------------------------------- follow-ups --- */
async function viewFollowups() {
  const { data, error } = await sb.from('lead_tasks')
    .select('*, leads(id,company_name,lead_number,country_code)')
    .eq('status', 'pending').order('due_at').limit(200);
  if (error) return fail(error);
  const now = new Date();
  $('#view').innerHTML = `<h1 class="page-title">Follow-ups</h1>
    ${data.length ? `<table class="table"><thead><tr><th>Due</th><th>Action</th><th>Lead</th><th></th></tr></thead>
      <tbody>${data.map(t => `<tr class="${new Date(t.due_at) < now ? 'overdue' : ''}">
        <td class="mono">${fmtDate(t.due_at)}</td><td>${esc(t.title)}</td>
        <td>${esc(t.leads?.company_name || '—')} <span class="muted mono">${esc(t.leads?.lead_number || '')}</span></td>
        <td><a class="btn btn--sm" href="#/lead/${t.lead_id}">Open</a></td></tr>`).join('')}</tbody></table>`
      : '<p class="muted">Nothing outstanding.</p>'}`;
}

/* -------------------------------------------------------------- helpers -- */
function fail(error) {
  console.error('[CRM]', error);
  $('#view').insertAdjacentHTML('afterbegin',
    `<p class="alert">Could not complete that action. ${esc(error.message || '')}</p>`);
}
function debounce(fn, ms) { let t; return (...a) => { clearTimeout(t); t = setTimeout(() => fn(...a), ms); }; }

/* --------------------------------------------------------------- router -- */
const ROUTES = [
  [/^#\/$|^$|^#$/, viewDashboard],
  [/^#\/leads$/, viewLeads],
  [/^#\/pipeline$/, viewPipeline],
  [/^#\/followups$/, viewFollowups],
  [/^#\/lead\/(.+)$/, viewLead]
];

function route() {
  const h = location.hash;
  $$('.nav a').forEach(a => a.setAttribute('aria-current', a.getAttribute('href') === h ? 'page' : 'false'));
  for (const [re, fn] of ROUTES) {
    const m = h.match(re);
    if (m) return fn(m[1]);
  }
  $('#view').innerHTML = '<p class="muted">Page not found.</p>';
}

async function start() {
  ME = await loadMe();
  if (!ME) { $('#login').hidden = false; $('#app').hidden = true; return; }
  $('#login').hidden = true; $('#app').hidden = false;
  $('#me').textContent = `${ME.full_name || ME.email} · ${ME.role.replace(/_/g, ' ')}`;
  window.addEventListener('hashchange', route);
  route();
}

$('#login-form').addEventListener('submit', signIn);
$('#signout').addEventListener('click', async () => { await sb.auth.signOut(); location.reload(); });
start();

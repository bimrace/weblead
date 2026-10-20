/* ============================================================================
   BIMRACE Portal — leads, contracts and project delivery
   Vanilla JS + supabase-js (vendored). Uses the publishable key only; every
   read and write is enforced by Row Level Security in the crm schema, so the
   role checks in this file only decide what to SHOW. Privileged user
   management goes through the staff-admin Edge Function.
   ========================================================================== */
'use strict';
const CFG = window.BIMRACE_CONFIG || {};

if (!window.supabase || !CFG.supabaseUrl || !CFG.supabaseAnonKey) {
  document.body.innerHTML =
    '<div class="login"><div class="login__box"><h1>Portal unavailable</h1>' +
    '<p class="muted">config.js is missing the Supabase URL or publishable key.</p></div></div>';
  throw new Error('BIMRACE portal: configuration missing');
}

const sb = window.supabase.createClient(CFG.supabaseUrl, CFG.supabaseAnonKey, {
  db: { schema: 'crm' },
  auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true }
});
const FN_STAFF = CFG.supabaseUrl.replace(/\/$/, '') + '/functions/v1/staff-admin';

/* ------------------------------------------------------------- helpers --- */
const $ = (s, c = document) => c.querySelector(s);
const $$ = (s, c = document) => [...c.querySelectorAll(s)];
const esc = s => String(s ?? '').replace(/[&<>"']/g, m =>
  ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[m]));
const label = s => esc(String(s ?? '—').replace(/_/g, ' '));
const fmtDate = d => d ? new Date(d).toLocaleDateString('en-GB',
  { day: '2-digit', month: 'short', year: 'numeric' }) : '—';
const fmtWhen = d => d ? new Date(d).toLocaleString('en-GB',
  { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' }) : '—';
const money = (v, c) => v == null ? '—' : `${esc(c || '')} ${Number(v).toLocaleString('en-IN')}`;
const opts = (list, cur) => list.map(v => `<option value="${esc(v)}"${v === cur ? ' selected' : ''}>${label(v)}</option>`).join('');
const val = id => { const el = $('#' + id); return el ? el.value.trim() : ''; };
const orNull = v => v === '' ? null : v;
function debounce(fn, ms) { let t; return (...a) => { clearTimeout(t); t = setTimeout(() => fn(...a), ms); }; }

function fail(error) {
  console.error('[portal]', error);
  const msg = /row-level security|permission denied/i.test(error?.message || '')
    ? 'Your role does not allow that action.' : (error?.message || 'Something went wrong.');
  $('#view').insertAdjacentHTML('afterbegin', `<p class="alert" role="alert">${esc(msg)}</p>`);
  $('#view').focus();
}
function toast(text) {
  $('#view').insertAdjacentHTML('afterbegin', `<p class="ok" role="status">${esc(text)}</p>`);
}

/* ------------------------------------------------------- roles & nav --- */
const LEAD_STAGES = ['new', 'contacted', 'qualifying', 'qualified', 'discovery',
  'scope_defined', 'proposal_required', 'proposal_sent', 'negotiation', 'won', 'lost'];
const PROJECT_STAGES = ['kickoff', 'inputs_review', 'design', 'modelling', 'coordination',
  'qa_qc', 'issued', 'handover', 'closed'];
const PROJECT_STATUS = ['planned', 'active', 'on_hold', 'completed', 'cancelled'];
const HEALTH = ['on_track', 'at_risk', 'blocked'];
const CONTRACT_STATUS = ['draft', 'sent', 'signed', 'active', 'completed', 'terminated'];
const CONTRACT_TYPES = ['fixed_fee', 'time_and_materials', 'retainer', 'framework'];
const DELIV_STATUS = ['not_started', 'in_progress', 'in_review', 'issued', 'approved', 'rejected'];
const DELIV_CATS = ['native_model', 'federated_model', 'drawing_package', 'schedules_quantities',
  'clash_report', 'design_documentation', 'calculations', 'qa_report', 'revision_register',
  'exchange_files', 'handover_note', 'other'];
const TASK_STATUS = ['todo', 'in_progress', 'blocked', 'done'];
const PRIORITY = ['low', 'normal', 'high', 'urgent'];
const MEMBER_ROLES = ['project_manager', 'bim_manager', 'lead_engineer', 'engineer', 'modeller',
  'coordinator', 'reviewer'];
const ROLES = ['admin', 'sales', 'business_development', 'project_manager', 'bim_manager',
  'engineer', 'viewer'];
const PACKAGES = ['PKG-01 MEP BIM Modeling', 'PKG-02 MEP Design Documentation', 'PKG-03 BIM Coordination',
  'PKG-04 Quantity Takeoff & BOQ', 'PKG-05 MEP Engineering Design', 'PKG-06 As-Built BIM & Handover'];
// The ten items of the catalogue Handover Checklist.
const HANDOVER = [
  ['Native Revit model', 'native_model'], ['Federated coordination model', 'federated_model'],
  ['Drawing package', 'drawing_package'], ['Schedules and quantities', 'schedules_quantities'],
  ['Clash report', 'clash_report'], ['Design documentation', 'design_documentation'],
  ['Model QA/QC report', 'qa_report'], ['Revision register', 'revision_register'],
  ['Exchange files', 'exchange_files'], ['Handover note', 'handover_note']];

let ME = null, USERS = [];
const has = (...roles) => ME && roles.includes(ME.role);
const isLeadRole = () => has('admin', 'sales', 'business_development', 'project_manager', 'bim_manager');
const isCommercial = () => has('admin', 'business_development', 'project_manager', 'sales');
const canWriteContracts = () => has('admin', 'business_development');
const canManageDelivery = () => has('admin', 'project_manager', 'bim_manager', 'business_development');

function buildNav() {
  const items = [['#/', 'Dashboard'], ['#/mywork', 'My work']];
  if (isLeadRole()) items.push(['#/leads', 'Leads'], ['#/pipeline', 'Lead pipeline'], ['#/followups', 'Follow-ups']);
  items.push(['#/projects', 'Projects']);
  if (isCommercial()) items.push(['#/contracts', 'Contracts']);
  if (has('admin')) items.push(['#/team', 'Team']);
  $('#nav').innerHTML = items.map(([h, t]) => `<a href="${h}">${t}</a>`).join('');
}
const userName = id => { const u = USERS.find(x => x.id === id); return u ? (u.full_name || u.email) : '—'; };
const userOpts = (cur, filter) => '<option value="">Unassigned</option>' + USERS
  .filter(u => u.is_active && (!filter || filter(u)))
  .map(u => `<option value="${u.id}"${u.id === cur ? ' selected' : ''}>${esc(u.full_name || u.email)}</option>`).join('');

/* --------------------------------------------------------------- auth --- */
async function signIn(e) {
  e.preventDefault();
  const btn = $('#login-btn'); btn.disabled = true; btn.textContent = 'Signing in…';
  const { error } = await sb.auth.signInWithPassword({
    email: $('#login-email').value.trim(), password: $('#login-password').value });
  btn.disabled = false; btn.textContent = 'Sign in';
  if (error) { $('#login-error').textContent = 'Sign-in failed. Check your email and password.'; return; }
  start();
}

async function forgot() {
  const email = $('#login-email').value.trim();
  if (!email) { $('#login-error').textContent = 'Enter your work email first.'; return; }
  await sb.auth.resetPasswordForEmail(email, { redirectTo: location.origin + location.pathname });
  $('#login-error').textContent = 'If that address has an account, a reset link is on its way. ' +
    'No email? Ask your portal administrator to reset your password.';
}

function showSetPassword() {
  $('#login').hidden = true; $('#app').hidden = true; $('#setpw').hidden = false;
}

async function savePassword(e) {
  e.preventDefault();
  const a = $('#setpw-1').value, b = $('#setpw-2').value;
  const strong = a.length >= 12 && /[A-Za-z]/.test(a) && /\d/.test(a) && /[^A-Za-z0-9]/.test(a);
  if (a !== b) { $('#setpw-error').textContent = 'The passwords do not match.'; return; }
  if (!strong) { $('#setpw-error').textContent = 'Use 12+ characters with letters, a number and a symbol.'; return; }
  const { error } = await sb.auth.updateUser({ password: a, data: { must_change_password: false } });
  if (error) { $('#setpw-error').textContent = error.message; return; }
  $('#setpw').hidden = true;
  history.replaceState(null, '', location.pathname + '#/');
  start();
}

async function loadMe() {
  const { data: { user } } = await sb.auth.getUser();
  if (!user) return null;
  const { data } = await sb.from('app_users').select('*').eq('id', user.id).maybeSingle();
  return { ...(data || { id: user.id, email: user.email, role: 'viewer', full_name: user.email,
                          is_active: true }), must_change: !!user.user_metadata?.must_change_password };
}

async function loadUsers() {
  const { data } = await sb.from('app_users').select('id,email,full_name,role,is_active').order('full_name');
  USERS = data || (ME ? [ME] : []);
}

/* ---------------------------------------------------------- dashboard --- */
async function viewDashboard() {
  const card = (k, v, hint) => `<article class="metric"><p class="metric__k">${esc(k)}</p>
    <p class="metric__v">${esc(v ?? 0)}</p>${hint ? `<p class="metric__h">${esc(hint)}</p>` : ''}</article>`;
  const calls = [sb.rpc('fn_delivery_metrics')];
  if (isLeadRole()) calls.push(sb.rpc('fn_dashboard_metrics'));
  const [del, lead] = await Promise.all(calls);
  const d = del?.data || {}, m = lead?.data || {};
  $('#view').innerHTML = `
    <h1 class="page-title">Dashboard</h1>
    <p class="muted">Signed in as ${esc(ME.full_name || ME.email)} · ${label(ME.role)}</p>
    <h2 class="section-h">Delivery</h2>
    <div class="metrics">
      ${card('Active projects', d.projects_active)}
      ${card('At risk / blocked', d.projects_at_risk)}
      ${card('Deliverables due in 7 days', d.deliverables_due_7d)}
      ${card('My open tasks', d.my_open_tasks)}
      ${d.contracts_signed_value != null ? card('Signed contract value', Number(d.contracts_signed_value).toLocaleString('en-IN')) : ''}
    </div>
    ${isLeadRole() ? `<h2 class="section-h">Leads</h2>
    <div class="metrics">
      ${card('New today', m.new_today)}${card('New this week', m.new_this_week)}
      ${card('Open leads', m.open)}${card('Hot', m.hot, 'score 76+')}
      ${card('Follow-ups due', m.followups_due)}${card('Overdue', m.followups_overdue)}
      ${card('Won', m.won)}${card('International', m.international)}
    </div>` : ''}`;
}

/* --------------------------------------------------------------- my work --- */
async function viewMyWork() {
  const [tasks, dels] = await Promise.all([
    sb.from('project_tasks').select('*, projects(id,name,project_number)').eq('assignee_id', ME.id)
      .neq('status', 'done').order('due_date', { nullsFirst: false }),
    sb.from('project_deliverables').select('*, projects(id,name,project_number)').eq('assignee_id', ME.id)
      .not('status', 'in', '(issued,approved)').order('due_date', { nullsFirst: false })]);
  if (tasks.error) return fail(tasks.error);
  const now = new Date();
  const late = d => d && new Date(d) < now ? ' class="overdue"' : '';
  $('#view').innerHTML = `<h1 class="page-title">My work</h1>
    <section class="panel"><h2>My tasks</h2>${tasks.data.length ? `<table class="table"><thead><tr>
      <th>Task</th><th>Project</th><th>Priority</th><th>Due</th><th>Status</th></tr></thead><tbody>
      ${tasks.data.map(t => `<tr${late(t.due_date)}><td>${esc(t.title)}</td>
        <td><a href="#/project/${t.project_id}">${esc(t.projects?.project_number)} ${esc(t.projects?.name)}</a></td>
        <td>${label(t.priority)}</td><td class="mono">${fmtDate(t.due_date)}</td>
        <td><select data-task="${t.id}" aria-label="Task status">${opts(TASK_STATUS, t.status)}</select></td></tr>`).join('')}
      </tbody></table>` : '<p class="muted">No open tasks assigned to you.</p>'}</section>
    <section class="panel"><h2>My deliverables</h2>${dels.data.length ? `<table class="table"><thead><tr>
      <th>Deliverable</th><th>Project</th><th>Rev</th><th>Due</th><th>Status</th></tr></thead><tbody>
      ${dels.data.map(x => `<tr${late(x.due_date)}><td>${esc(x.name)}</td>
        <td><a href="#/project/${x.project_id}">${esc(x.projects?.project_number)} ${esc(x.projects?.name)}</a></td>
        <td class="mono">${esc(x.revision || '—')}</td><td class="mono">${fmtDate(x.due_date)}</td>
        <td><select data-deliv="${x.id}" aria-label="Deliverable status">${opts(DELIV_STATUS, x.status)}</select></td></tr>`).join('')}
      </tbody></table>` : '<p class="muted">No open deliverables assigned to you.</p>'}</section>`;
  wireStatusSelects(viewMyWork);
}

function wireStatusSelects(reload) {
  $$('[data-task]').forEach(s => s.addEventListener('change', async () => {
    const { error } = await sb.from('project_tasks').update({ status: s.value }).eq('id', s.dataset.task);
    if (error) return fail(error); reload();
  }));
  $$('[data-deliv]').forEach(s => s.addEventListener('change', async () => {
    const patch = { status: s.value };
    if (s.value === 'issued') patch.issued_at = new Date().toISOString();
    const { error } = await sb.from('project_deliverables').update(patch).eq('id', s.dataset.deliv);
    if (error) return fail(error); reload();
  }));
}

/* ----------------------------------------------------------------- leads --- */
async function viewLeads() {
  $('#view').innerHTML = `<h1 class="page-title">Leads</h1>
    <div class="toolbar">
      <input id="q" type="search" placeholder="Search company, contact or email…" aria-label="Search leads">
      <select id="f-status" aria-label="Filter by status"><option value="">All statuses</option>${opts(LEAD_STAGES)}</select>
      <select id="f-geo" aria-label="Filter by geography"><option value="">India + International</option>
        <option value="in">India only</option><option value="intl">International only</option></select>
    </div>
    <div id="lead-rows" class="table-wrap"><p class="muted">Loading…</p></div>`;
  const run = async () => {
    let q = sb.from('leads').select('id,lead_number,company_name,contact_name,email,country_code,' +
      'is_international,lead_type,status,lead_score,score_band,created_at')
      .order('created_at', { ascending: false }).limit(300);
    const s = val('f-status'), g = val('f-geo'), t = val('q').replace(/[,%()]/g, ' ');
    if (s) q = q.eq('status', s);
    if (g === 'in') q = q.eq('country_code', 'IN');
    if (g === 'intl') q = q.eq('is_international', true);
    if (t) q = q.or(`company_name.ilike.%${t}%,contact_name.ilike.%${t}%,email.ilike.%${t}%`);
    const { data, error } = await q;
    if (error) return fail(error);
    $('#lead-rows').innerHTML = data.length ? `<table class="table"><thead><tr>
      <th>Lead</th><th>Company</th><th>Contact</th><th>Service</th><th>Geo</th><th>Score</th><th>Status</th><th>Received</th>
      </tr></thead><tbody>${data.map(l => `<tr data-href="#/lead/${l.id}" tabindex="0">
        <td class="mono">${esc(l.lead_number)}</td><td>${esc(l.company_name || '—')}</td>
        <td>${esc(l.contact_name || '—')}<br><span class="muted">${esc(l.email || '')}</span></td>
        <td>${label(l.lead_type)}</td>
        <td>${esc(l.country_code || '—')}${l.is_international ? ' <span class="tag">INT</span>' : ''}</td>
        <td><span class="score score--${esc(l.score_band)}">${esc(l.lead_score)}</span></td>
        <td><span class="pill pill--${esc(l.status)}">${label(l.status)}</span></td>
        <td class="muted">${fmtDate(l.created_at)}</td></tr>`).join('')}</tbody></table>`
      : '<p class="muted">No leads match these filters.</p>';
    wireRowLinks();
  };
  ['q', 'f-status', 'f-geo'].forEach(id => $('#' + id).addEventListener(id === 'q' ? 'input' : 'change', debounce(run, 250)));
  run();
}

function wireRowLinks() {
  $$('tr[data-href]').forEach(r => {
    const go = () => location.hash = r.dataset.href;
    r.addEventListener('click', e => { if (!e.target.closest('a,select,button,input')) go(); });
    r.addEventListener('keydown', e => { if (e.key === 'Enter') go(); });
  });
}

async function viewPipeline() {
  const cols = LEAD_STAGES.filter(s => s !== 'lost');
  const { data, error } = await sb.from('leads').select(
    'id,lead_number,company_name,contact_name,lead_type,country_code,status,lead_score,score_band,next_follow_up_at')
    .not('status', 'in', '(spam,duplicate,not_qualified)').order('lead_score', { ascending: false });
  if (error) return fail(error);
  $('#view').innerHTML = `<h1 class="page-title">Lead pipeline</h1>
    <p class="muted">Drag a card to change its stage. Every move is written to the status history.</p>
    <div class="board">${cols.map(st => `<section class="col"><h2>${label(st)}
      <span class="count">${data.filter(l => l.status === st).length}</span></h2>
      <div class="col__drop" data-drop="${st}">${data.filter(l => l.status === st).map(l =>
        `<article class="card" draggable="true" data-id="${l.id}" data-href="#/lead/${l.id}">
          <p class="card__co">${esc(l.company_name || l.contact_name || 'Unnamed')}</p>
          <p class="card__meta">${label(l.lead_type)} · ${esc(l.country_code || '??')}</p>
          <p class="card__foot"><span class="score score--${esc(l.score_band)}">${esc(l.lead_score)}</span>
          <span class="mono muted">${esc(l.lead_number)}</span></p></article>`).join('')}</div></section>`).join('')}</div>`;
  wireBoard('leads', 'status', viewPipeline);
}

function wireBoard(table, field, reload) {
  $$('.card').forEach(c => {
    c.addEventListener('dragstart', e => { e.dataTransfer.setData('text/plain', c.dataset.id); c.classList.add('dragging'); });
    c.addEventListener('dragend', () => c.classList.remove('dragging'));
    c.addEventListener('click', () => location.hash = c.dataset.href);
  });
  $$('.col__drop').forEach(z => {
    z.addEventListener('dragover', e => { e.preventDefault(); z.classList.add('over'); });
    z.addEventListener('dragleave', () => z.classList.remove('over'));
    z.addEventListener('drop', async e => {
      e.preventDefault(); z.classList.remove('over');
      const { error } = await sb.from(table).update({ [field]: z.dataset.drop }).eq('id', e.dataTransfer.getData('text/plain'));
      if (error) return fail(error); reload();
    });
  });
}

async function viewLead(id) {
  const [lead, notes, tasks, acts, hist, score, files] = await Promise.all([
    sb.from('leads').select('*').eq('id', id).maybeSingle(),
    sb.from('lead_notes').select('*').eq('lead_id', id).order('created_at', { ascending: false }),
    sb.from('lead_tasks').select('*').eq('lead_id', id).order('due_at'),
    sb.from('activities').select('*').eq('lead_id', id).order('occurred_at', { ascending: false }).limit(50),
    sb.from('lead_status_history').select('*').eq('lead_id', id).order('changed_at', { ascending: false }),
    sb.from('lead_score_history').select('*').eq('lead_id', id).order('computed_at', { ascending: false }).limit(1),
    sb.from('attachments').select('*').eq('lead_id', id).order('uploaded_at')]);
  if (lead.error) return fail(lead.error);
  const l = lead.data;
  if (!l) { $('#view').innerHTML = '<p class="muted">Lead not found, or your role cannot view it.</p>'; return; }
  const { data: proj } = await sb.from('projects').select('id,project_number').eq('lead_id', id).maybeSingle();
  const rules = score.data?.[0]?.breakdown?.rules || [];
  const row = (k, v) => v ? `<div class="kv"><dt>${esc(k)}</dt><dd>${esc(v)}</dd></div>` : '';
  $('#view').innerHTML = `<a class="back" href="#/leads">← All leads</a>
    <header class="lead-head"><div><h1 class="page-title">${esc(l.company_name || l.contact_name || 'Lead')}</h1>
      <p class="muted mono">${esc(l.lead_number)} · received ${fmtWhen(l.created_at)}</p></div>
      <div class="lead-head__r"><span class="score score--${esc(l.score_band)} score--lg">${esc(l.lead_score)}</span>
      <select id="set-status" aria-label="Lead status">${opts(LEAD_STAGES.concat(['on_hold', 'not_qualified', 'spam', 'duplicate']), l.status)}</select></div></header>
    <div class="grid-2">
      <section class="panel"><h2>Enquiry</h2><dl class="kvs">
        ${row('Contact', l.contact_name)}${row('Email', l.email)}${row('Phone', l.phone)}
        ${row('Country', l.country_code)}${row('Service', String(l.lead_type || '').replace(/_/g, ' '))}
        ${row('Sector', l.industry)}${row('Project type', l.project_type)}${row('Stage', l.project_stage)}
        ${row('Location', l.project_location)}${row('Size', l.project_size)}
        ${row('Disciplines', (l.disciplines || []).join(', '))}</dl>
        ${l.message ? `<h3>Message</h3><p class="msg">${esc(l.message)}</p>` : ''}
        <h3>Files</h3>${(files.data || []).length ? `<ul class="files">${files.data.map(f =>
          `<li><button class="linkbtn" data-file="${esc(f.storage_path)}">${esc(f.file_name)}</button>
           <span class="muted mono">${(f.byte_size / 1048576).toFixed(1)} MB</span></li>`).join('')}</ul>`
          : '<p class="muted">No files attached.</p>'}</section>
      <section class="panel"><h2>Why this score</h2>
        ${rules.length ? `<ul class="rules">${rules.map(r => `<li><span class="pts ${r.points < 0 ? 'neg' : 'pos'}">${r.points > 0 ? '+' : ''}${esc(r.points)}</span> ${esc(r.label)}</li>`).join('')}</ul>` : '<p class="muted">No scoring history.</p>'}
        <h2 style="margin-top:24px">Status history</h2>
        <ul class="timeline">${(hist.data || []).map(h => `<li><span class="muted mono">${fmtWhen(h.changed_at)}</span>
          ${esc(h.from_status || 'created')} → <strong>${esc(h.to_status)}</strong></li>`).join('') || '<li class="muted">No transitions yet.</li>'}</ul></section>
    </div>
    <div class="grid-2">
      <section class="panel"><h2>Notes</h2>
        <form id="note-form"><textarea id="note-body" rows="3" placeholder="Add an internal note…" required></textarea>
          <button class="btn btn--sm" type="submit">Add note</button></form>
        <ul class="notes">${(notes.data || []).map(n => `<li><p>${esc(n.body)}</p><p class="muted mono">${fmtWhen(n.created_at)}</p></li>`).join('') || '<li class="muted">No notes yet.</li>'}</ul></section>
      <section class="panel"><h2>Follow-ups</h2>
        <form id="ftask-form" class="task-form"><input id="ftask-title" placeholder="Follow-up action" required>
          <input id="ftask-due" type="date" required><button class="btn btn--sm" type="submit">Schedule</button></form>
        <ul class="tasks">${(tasks.data || []).map(t => `<li class="${t.status === 'pending' && new Date(t.due_at) < new Date() ? 'overdue' : ''}">
          <label><input type="checkbox" data-ftask="${t.id}" ${t.status === 'completed' ? 'checked' : ''}> ${esc(t.title)}</label>
          <span class="muted mono">${fmtDate(t.due_at)}</span></li>`).join('') || '<li class="muted">Nothing scheduled.</li>'}</ul></section>
    </div>
    <section class="panel"><h2>Activity</h2><ul class="timeline">${(acts.data || []).map(a =>
      `<li><span class="muted mono">${fmtWhen(a.occurred_at)}</span> <strong>${label(a.activity_type)}</strong> — ${esc(a.summary)}</li>`).join('')}</ul></section>
    <div class="actions">${proj ? `<a class="btn btn--primary" href="#/project/${proj.id}">Open project ${esc(proj.project_number)}</a>`
      : `<button class="btn btn--primary" id="convert">Convert to project (marks lead won)</button>`}
      ${canWriteContracts() ? `<a class="btn" href="#/contract/new?lead=${l.id}">Create contract</a>` : ''}</div>`;

  $('#set-status').addEventListener('change', async e => {
    const { error } = await sb.from('leads').update({ status: e.target.value }).eq('id', id);
    if (error) return fail(error); viewLead(id);
  });
  $('#note-form').addEventListener('submit', async e => {
    e.preventDefault();
    const { error } = await sb.from('lead_notes').insert({ lead_id: id, body: val('note-body'), author_id: ME.id });
    if (error) return fail(error); viewLead(id);
  });
  $('#ftask-form').addEventListener('submit', async e => {
    e.preventDefault();
    const due = new Date(val('ftask-due')).toISOString();
    const { error } = await sb.from('lead_tasks').insert({ lead_id: id, title: val('ftask-title'), due_at: due,
      owner_id: ME.id, created_by: ME.id });
    if (error) return fail(error);
    await sb.from('leads').update({ next_follow_up_at: due }).eq('id', id);
    viewLead(id);
  });
  $$('[data-ftask]').forEach(cb => cb.addEventListener('change', async () => {
    const { error } = await sb.from('lead_tasks').update({ status: cb.checked ? 'completed' : 'pending',
      completed_at: cb.checked ? new Date().toISOString() : null }).eq('id', cb.dataset.ftask);
    if (error) fail(error);
  }));
  $$('[data-file]').forEach(b => b.addEventListener('click', async () => {
    const { data, error } = await sb.storage.from('enquiry-files').createSignedUrl(b.dataset.file, 300);
    if (error) return fail(error);
    window.open(data.signedUrl, '_blank', 'noopener');
  }));
  const conv = $('#convert');
  if (conv) conv.addEventListener('click', async () => {
    if (!confirm('Convert this lead to a project and mark it WON?')) return;
    const { data, error } = await sb.rpc('fn_convert_lead_to_project', { p_lead_id: id, p_name: null });
    if (error) return fail(error);
    location.hash = '#/project/' + data;
  });
}

async function viewFollowups() {
  const { data, error } = await sb.from('lead_tasks').select('*, leads(id,company_name,lead_number)')
    .eq('status', 'pending').order('due_at').limit(300);
  if (error) return fail(error);
  const now = new Date();
  $('#view').innerHTML = `<h1 class="page-title">Follow-ups</h1>${data.length ? `<table class="table"><thead><tr>
    <th>Due</th><th>Action</th><th>Lead</th></tr></thead><tbody>${data.map(t =>
    `<tr class="${new Date(t.due_at) < now ? 'overdue' : ''}" data-href="#/lead/${t.lead_id}" tabindex="0">
      <td class="mono">${fmtDate(t.due_at)}</td><td>${esc(t.title)}</td>
      <td>${esc(t.leads?.company_name || '—')} <span class="muted mono">${esc(t.leads?.lead_number || '')}</span></td></tr>`).join('')}
    </tbody></table>` : '<p class="muted">Nothing outstanding.</p>'}`;
  wireRowLinks();
}

/* -------------------------------------------------------------- projects --- */
async function viewProjects() {
  const board = location.hash.includes('board');
  const { data, error } = await sb.from('projects').select(
    'id,project_number,name,status,stage,health,progress,building_type,location,end_date,manager_id,organizations(name)')
    .order('created_at', { ascending: false });
  if (error) return fail(error);
  const head = `<header class="lead-head"><h1 class="page-title">Projects</h1><div class="lead-head__r">
    <a class="btn btn--sm" href="${board ? '#/projects' : '#/projects?board'}">${board ? 'List view' : 'Stage board'}</a>
    ${canManageDelivery() ? '<a class="btn btn--primary btn--sm" href="#/project/new">New project</a>' : ''}</div></header>`;
  if (!data.length) { $('#view').innerHTML = head + '<p class="muted">No projects yet. Convert a won lead or create one.</p>'; return; }
  if (board) {
    const live = data.filter(p => !['completed', 'cancelled'].includes(p.status));
    $('#view').innerHTML = head + `<p class="muted">${canManageDelivery() ? 'Drag a project to move it to another stage.' : 'Projects you can see, by delivery stage.'}</p>
      <div class="board">${PROJECT_STAGES.map(st => `<section class="col"><h2>${label(st)}
        <span class="count">${live.filter(p => p.stage === st).length}</span></h2>
        <div class="col__drop" data-drop="${st}">${live.filter(p => p.stage === st).map(p =>
          `<article class="card" draggable="${canManageDelivery()}" data-id="${p.id}" data-href="#/project/${p.id}">
            <p class="card__co">${esc(p.name)}</p>
            <p class="card__meta">${esc(p.organizations?.name || '—')}</p>
            <p class="card__foot"><span class="health health--${esc(p.health)}">${label(p.health)}</span>
            <span class="mono muted">${esc(p.project_number)}</span></p>
            <div class="progress" aria-label="Progress ${esc(p.progress)}%"><i style="width:${Number(p.progress) || 0}%"></i></div>
          </article>`).join('')}</div></section>`).join('')}</div>`;
    if (canManageDelivery()) wireBoard('projects', 'stage', viewProjects);
    else $$('.card').forEach(c => c.addEventListener('click', () => location.hash = c.dataset.href));
    return;
  }
  $('#view').innerHTML = head + `<table class="table"><thead><tr><th>Project</th><th>Client</th><th>Stage</th>
    <th>Status</th><th>Health</th><th>Progress</th><th>Manager</th><th>Due</th></tr></thead><tbody>
    ${data.map(p => `<tr data-href="#/project/${p.id}" tabindex="0">
      <td><span class="mono muted">${esc(p.project_number)}</span><br>${esc(p.name)}</td>
      <td>${esc(p.organizations?.name || '—')}</td><td>${label(p.stage)}</td><td>${label(p.status)}</td>
      <td><span class="health health--${esc(p.health)}">${label(p.health)}</span></td>
      <td><div class="progress"><i style="width:${Number(p.progress) || 0}%"></i></div></td>
      <td>${esc(userName(p.manager_id))}</td><td class="mono">${fmtDate(p.end_date)}</td></tr>`).join('')}
    </tbody></table>`;
  wireRowLinks();
}

async function projectForm(p) {
  const { data: orgs } = await sb.from('organizations').select('id,name').order('name').limit(500);
  return `<form id="proj-form" class="form-grid">
    <label>Project name<input id="p-name" required maxlength="200" value="${esc(p.name || '')}"></label>
    <label>Client<select id="p-org"><option value="">—</option>${(orgs || []).map(o =>
      `<option value="${o.id}"${o.id === p.organization_id ? ' selected' : ''}>${esc(o.name)}</option>`).join('')}</select></label>
    <label>Building type<input id="p-btype" value="${esc(p.building_type || '')}" placeholder="e.g. Hospital, office tower"></label>
    <label>Location<input id="p-loc" value="${esc(p.location || '')}" placeholder="City, country"></label>
    <label>Service package<select id="p-pkg"><option value="">—</option>${PACKAGES.map(k =>
      `<option${k.slice(0, 6) === p.package_code ? ' selected' : ''} value="${k.slice(0, 6)}">${esc(k)}</option>`).join('')}</select></label>
    <label>Project manager<select id="p-mgr">${userOpts(p.manager_id, u => ['admin', 'project_manager', 'bim_manager'].includes(u.role))}</select></label>
    <label>Status<select id="p-status">${opts(PROJECT_STATUS, p.status || 'planned')}</select></label>
    <label>Stage<select id="p-stage">${opts(PROJECT_STAGES, p.stage || 'kickoff')}</select></label>
    <label>Health<select id="p-health">${opts(HEALTH, p.health || 'on_track')}</select></label>
    <label>Progress %<input id="p-progress" type="number" min="0" max="100" value="${esc(p.progress ?? 0)}"></label>
    <label>Start<input id="p-start" type="date" value="${esc(p.start_date || '')}"></label>
    <label>Finish<input id="p-end" type="date" value="${esc(p.end_date || '')}"></label>
    <label class="span2">Disciplines<input id="p-disc" value="${esc((p.disciplines || []).join(', '))}" placeholder="HVAC, Plumbing, Fire protection, Electrical"></label>
    <label class="span2">Scope summary<textarea id="p-scope" rows="3">${esc(p.scope_summary || '')}</textarea></label>
    <label class="check span2"><input id="p-design" type="checkbox"${p.design_responsibility ? ' checked' : ''}> Engineering design responsibility is in scope (PKG-05)</label>
    <div class="span2"><button class="btn btn--primary" type="submit">Save project</button></div>
  </form>`;
}

function readProjectForm() {
  return {
    name: val('p-name'), organization_id: orNull(val('p-org')), building_type: orNull(val('p-btype')),
    location: orNull(val('p-loc')), package_code: orNull(val('p-pkg')), manager_id: orNull(val('p-mgr')),
    status: val('p-status'), stage: val('p-stage'), health: val('p-health'),
    progress: Math.max(0, Math.min(100, parseInt(val('p-progress') || '0', 10))),
    start_date: orNull(val('p-start')), end_date: orNull(val('p-end')),
    disciplines: val('p-disc') ? val('p-disc').split(',').map(s => s.trim()).filter(Boolean) : null,
    scope_summary: orNull(val('p-scope')), design_responsibility: $('#p-design').checked
  };
}

async function viewNewProject() {
  if (!canManageDelivery()) { $('#view').innerHTML = '<p class="muted">Your role cannot create projects.</p>'; return; }
  $('#view').innerHTML = `<a class="back" href="#/projects">← Projects</a><h1 class="page-title">New project</h1>
    <section class="panel">${await projectForm({})}</section>`;
  $('#proj-form').addEventListener('submit', async e => {
    e.preventDefault();
    const { data, error } = await sb.from('projects').insert(readProjectForm()).select('id').single();
    if (error) return fail(error);
    location.hash = '#/project/' + data.id;
  });
}

async function viewProject(id) {
  const [proj, members, miles, dels, tasks, contracts] = await Promise.all([
    sb.from('projects').select('*, organizations(name)').eq('id', id).maybeSingle(),
    sb.from('project_members').select('*').eq('project_id', id),
    sb.from('project_milestones').select('*').eq('project_id', id).order('sort_order').order('due_date'),
    sb.from('project_deliverables').select('*').eq('project_id', id).order('created_at'),
    sb.from('project_tasks').select('*').eq('project_id', id).order('status').order('due_date', { nullsFirst: false }),
    isCommercial() ? sb.from('contracts').select('id,contract_number,title,status,value,currency').eq('project_id', id)
      : Promise.resolve({ data: [] })]);
  if (proj.error) return fail(proj.error);
  const p = proj.data;
  if (!p) { $('#view').innerHTML = '<p class="muted">Project not found, or you are not on its team.</p>'; return; }
  const mgr = canManageDelivery();
  const memberIds = (members.data || []).map(m => m.user_id);
  const mine = uid => uid === ME.id;
  const now = new Date();

  $('#view').innerHTML = `<a class="back" href="#/projects">← Projects</a>
    <header class="lead-head"><div><h1 class="page-title">${esc(p.name)}</h1>
      <p class="muted mono">${esc(p.project_number)} · ${esc(p.organizations?.name || 'No client')} · ${esc(p.package_code || '')}</p></div>
      <div class="lead-head__r"><span class="health health--${esc(p.health)}">${label(p.health)}</span>
        <span class="pill">${label(p.stage)}</span><span class="pill">${label(p.status)}</span></div></header>
    <div class="progress progress--lg"><i style="width:${Number(p.progress) || 0}%"></i></div>
    <nav class="tabs" role="tablist">${['overview', 'deliverables', 'tasks', 'milestones', 'team'].concat(isCommercial() ? ['contract'] : [])
      .map((t, i) => `<button role="tab" data-tab="${t}" aria-selected="${i === 0}">${label(t)}</button>`).join('')}</nav>

    <section class="panel tab" data-pane="overview">
      ${mgr ? await projectForm(p) : `<dl class="kvs">
        ${[['Client', p.organizations?.name], ['Building type', p.building_type], ['Location', p.location],
           ['Package', p.package_code], ['Manager', userName(p.manager_id)], ['Disciplines', (p.disciplines || []).join(', ')],
           ['Start', fmtDate(p.start_date)], ['Finish', fmtDate(p.end_date)],
           ['Design responsibility', p.design_responsibility ? 'Yes' : 'No']]
          .map(([k, v]) => `<div class="kv"><dt>${esc(k)}</dt><dd>${esc(v || '—')}</dd></div>`).join('')}</dl>
        ${p.scope_summary ? `<h3>Scope</h3><p class="msg">${esc(p.scope_summary)}</p>` : ''}`}
    </section>

    <section class="panel tab" data-pane="deliverables" hidden><h2>Deliverables</h2>
      ${(dels.data || []).length ? `<table class="table"><thead><tr><th>Deliverable</th><th>Type</th><th>Assignee</th>
        <th>Rev</th><th>Due</th><th>Status</th>${mgr ? '<th></th>' : ''}</tr></thead><tbody>${dels.data.map(d =>
        `<tr${d.due_date && new Date(d.due_date) < now && !['issued', 'approved'].includes(d.status) ? ' class="overdue"' : ''}>
          <td>${esc(d.name)}</td><td>${label(d.category)}</td>
          <td>${mgr ? `<select data-assign-deliv="${d.id}" aria-label="Assignee">${userOpts(d.assignee_id, u => memberIds.includes(u.id))}</select>` : esc(userName(d.assignee_id))}</td>
          <td>${mgr || mine(d.assignee_id) ? `<input class="rev" data-rev="${d.id}" value="${esc(d.revision || '')}" aria-label="Revision" size="4">` : esc(d.revision || '—')}</td>
          <td class="mono">${fmtDate(d.due_date)}</td>
          <td>${mgr || mine(d.assignee_id) ? `<select data-deliv="${d.id}" aria-label="Status">${opts(DELIV_STATUS, d.status)}</select>` : label(d.status)}</td>
          ${mgr ? `<td><button class="linkbtn" data-del-deliv="${d.id}" aria-label="Delete deliverable">Remove</button></td>` : ''}</tr>`).join('')}
        </tbody></table>` : '<p class="muted">No deliverables yet.</p>'}
      ${mgr ? `<form id="deliv-form" class="inline-form">
        <input id="d-name" placeholder="Deliverable" required maxlength="200">
        <select id="d-cat" aria-label="Type">${opts(DELIV_CATS, 'drawing_package')}</select>
        <select id="d-assignee" aria-label="Assignee">${userOpts(null, u => memberIds.includes(u.id))}</select>
        <input id="d-due" type="date" aria-label="Due date">
        <button class="btn btn--sm" type="submit">Add</button></form>
        <button class="btn btn--sm" id="add-handover">Add the 10-item handover checklist</button>` : ''}
    </section>

    <section class="panel tab" data-pane="tasks" hidden><h2>Tasks</h2>
      ${(tasks.data || []).length ? `<table class="table"><thead><tr><th>Task</th><th>Assignee</th><th>Priority</th>
        <th>Due</th><th>Status</th></tr></thead><tbody>${tasks.data.map(t =>
        `<tr${t.due_date && new Date(t.due_date) < now && t.status !== 'done' ? ' class="overdue"' : ''}>
          <td>${esc(t.title)}${t.description ? `<br><span class="muted">${esc(t.description)}</span>` : ''}</td>
          <td>${mgr ? `<select data-assign-task="${t.id}" aria-label="Assignee">${userOpts(t.assignee_id, u => memberIds.includes(u.id))}</select>` : esc(userName(t.assignee_id))}</td>
          <td>${label(t.priority)}</td><td class="mono">${fmtDate(t.due_date)}</td>
          <td>${mgr || mine(t.assignee_id) ? `<select data-task="${t.id}" aria-label="Status">${opts(TASK_STATUS, t.status)}</select>` : label(t.status)}</td></tr>`).join('')}
        </tbody></table>` : '<p class="muted">No tasks yet.</p>'}
      ${mgr || memberIds.includes(ME.id) ? `<form id="task-form" class="inline-form">
        <input id="t-title" placeholder="Task" required maxlength="300">
        <select id="t-assignee" aria-label="Assignee">${userOpts(mgr ? null : ME.id, u => memberIds.includes(u.id))}</select>
        <select id="t-priority" aria-label="Priority">${opts(PRIORITY, 'normal')}</select>
        <input id="t-due" type="date" aria-label="Due date">
        <button class="btn btn--sm" type="submit">Add task</button></form>` : ''}
    </section>

    <section class="panel tab" data-pane="milestones" hidden><h2>Milestones</h2>
      ${(miles.data || []).length ? `<table class="table"><thead><tr><th>Milestone</th><th>Due</th><th>Status</th>
        ${isCommercial() ? '<th>Invoice</th>' : ''}</tr></thead><tbody>${miles.data.map(m =>
        `<tr><td>${esc(m.name)}</td><td class="mono">${fmtDate(m.due_date)}</td>
          <td>${mgr ? `<select data-mile="${m.id}" aria-label="Status">${opts(['pending', 'in_progress', 'done'], m.status)}</select>` : label(m.status)}</td>
          ${isCommercial() ? `<td>${money(m.invoice_amount, p.currency)}${m.invoiced ? ' <span class="tag">INVOICED</span>' : ''}</td>` : ''}</tr>`).join('')}
        </tbody></table>` : '<p class="muted">No milestones yet.</p>'}
      ${mgr ? `<form id="mile-form" class="inline-form">
        <input id="m-name" placeholder="Milestone, e.g. Coordinated model issue" required maxlength="200">
        <input id="m-due" type="date" aria-label="Due date">
        <input id="m-amt" type="number" min="0" step="0.01" placeholder="Invoice amount" aria-label="Invoice amount">
        <button class="btn btn--sm" type="submit">Add</button></form>` : ''}
    </section>

    <section class="panel tab" data-pane="team" hidden><h2>Team</h2>
      ${(members.data || []).length ? `<table class="table"><thead><tr><th>Name</th><th>Project role</th>${mgr ? '<th></th>' : ''}</tr></thead><tbody>
        ${members.data.map(m => `<tr><td>${esc(userName(m.user_id))}</td><td>${label(m.project_role)}</td>
          ${mgr ? `<td><button class="linkbtn" data-unmember="${m.user_id}">Remove</button></td>` : ''}</tr>`).join('')}
        </tbody></table>` : '<p class="muted">No team members yet. Engineers only see projects they are added to.</p>'}
      ${mgr ? `<form id="member-form" class="inline-form">
        <select id="mem-user" aria-label="Person" required>${userOpts(null, u => !memberIds.includes(u.id))}</select>
        <select id="mem-role" aria-label="Project role">${opts(MEMBER_ROLES, 'engineer')}</select>
        <button class="btn btn--sm" type="submit">Add to team</button></form>` : ''}
    </section>

    ${isCommercial() ? `<section class="panel tab" data-pane="contract" hidden><h2>Contract</h2>
      ${(contracts.data || []).length ? `<table class="table"><tbody>${contracts.data.map(c =>
        `<tr data-href="#/contract/${c.id}" tabindex="0"><td class="mono">${esc(c.contract_number)}</td><td>${esc(c.title)}</td>
         <td>${label(c.status)}</td><td>${money(c.value, c.currency)}</td></tr>`).join('')}</tbody></table>`
        : '<p class="muted">No contract linked to this project.</p>'}
      ${canWriteContracts() ? `<a class="btn btn--sm" href="#/contract/new?project=${p.id}">Create contract</a>` : ''}
    </section>` : ''}`;

  // tabs
  $$('[data-tab]').forEach(b => b.addEventListener('click', () => {
    $$('[data-tab]').forEach(x => x.setAttribute('aria-selected', x === b));
    $$('.tab').forEach(t => { t.hidden = t.dataset.pane !== b.dataset.tab; });
  }));
  const reload = async () => { const tab = $('[data-tab][aria-selected="true"]')?.dataset.tab; await viewProject(id);
    if (tab) $(`[data-tab="${tab}"]`)?.click(); };
  wireRowLinks();
  wireStatusSelects(reload);

  if (mgr) {
    $('#proj-form').addEventListener('submit', async e => {
      e.preventDefault();
      const { error } = await sb.from('projects').update(readProjectForm()).eq('id', id);
      if (error) return fail(error); await reload(); toast('Project saved.');
    });
    $('#deliv-form').addEventListener('submit', async e => {
      e.preventDefault();
      const { error } = await sb.from('project_deliverables').insert({ project_id: id, name: val('d-name'),
        category: val('d-cat'), assignee_id: orNull(val('d-assignee')), due_date: orNull(val('d-due')) });
      if (error) return fail(error); reload();
    });
    $('#add-handover').addEventListener('click', async () => {
      const existing = new Set((dels.data || []).map(d => d.name));
      const rows = HANDOVER.filter(([n]) => !existing.has(n)).map(([name, category]) => ({ project_id: id, name, category }));
      if (!rows.length) return toast('The handover checklist is already on this project.');
      const { error } = await sb.from('project_deliverables').insert(rows);
      if (error) return fail(error); reload();
    });
    $$('[data-del-deliv]').forEach(b => b.addEventListener('click', async () => {
      if (!confirm('Remove this deliverable?')) return;
      const { error } = await sb.from('project_deliverables').delete().eq('id', b.dataset.delDeliv);
      if (error) return fail(error); reload();
    }));
    $$('[data-assign-deliv]').forEach(s => s.addEventListener('change', async () => {
      const { error } = await sb.from('project_deliverables').update({ assignee_id: orNull(s.value) }).eq('id', s.dataset.assignDeliv);
      if (error) return fail(error);
    }));
    $$('[data-assign-task]').forEach(s => s.addEventListener('change', async () => {
      const { error } = await sb.from('project_tasks').update({ assignee_id: orNull(s.value) }).eq('id', s.dataset.assignTask);
      if (error) return fail(error);
    }));
    $('#mile-form').addEventListener('submit', async e => {
      e.preventDefault();
      const { error } = await sb.from('project_milestones').insert({ project_id: id, name: val('m-name'),
        due_date: orNull(val('m-due')), invoice_amount: val('m-amt') ? Number(val('m-amt')) : null,
        sort_order: (miles.data || []).length });
      if (error) return fail(error); reload();
    });
    $$('[data-mile]').forEach(s => s.addEventListener('change', async () => {
      const { error } = await sb.from('project_milestones').update({ status: s.value }).eq('id', s.dataset.mile);
      if (error) return fail(error);
    }));
    $('#member-form').addEventListener('submit', async e => {
      e.preventDefault();
      if (!val('mem-user')) return;
      const { error } = await sb.from('project_members').insert({ project_id: id, user_id: val('mem-user'), project_role: val('mem-role') });
      if (error) return fail(error); reload();
    });
    $$('[data-unmember]').forEach(b => b.addEventListener('click', async () => {
      const { error } = await sb.from('project_members').delete().eq('project_id', id).eq('user_id', b.dataset.unmember);
      if (error) return fail(error); reload();
    }));
  }
  $$('[data-rev]').forEach(inp => inp.addEventListener('change', async () => {
    const { error } = await sb.from('project_deliverables').update({ revision: orNull(inp.value.trim()) }).eq('id', inp.dataset.rev);
    if (error) fail(error);
  }));
  const tf = $('#task-form');
  if (tf) tf.addEventListener('submit', async e => {
    e.preventDefault();
    const { error } = await sb.from('project_tasks').insert({ project_id: id, title: val('t-title'),
      assignee_id: orNull(val('t-assignee')), priority: val('t-priority'), due_date: orNull(val('t-due')) });
    if (error) return fail(error); reload();
  });
}

/* ------------------------------------------------------------- contracts --- */
async function viewContracts() {
  const { data, error } = await sb.from('contracts')
    .select('id,contract_number,title,status,contract_type,value,currency,signed_date,end_date,organizations(name),projects(id,project_number)')
    .order('created_at', { ascending: false });
  if (error) return fail(error);
  $('#view').innerHTML = `<header class="lead-head"><h1 class="page-title">Contracts</h1>
    ${canWriteContracts() ? '<a class="btn btn--primary btn--sm" href="#/contract/new">New contract</a>' : ''}</header>
    ${data.length ? `<table class="table"><thead><tr><th>Contract</th><th>Client</th><th>Type</th><th>Status</th>
      <th>Value</th><th>Signed</th><th>Project</th></tr></thead><tbody>${data.map(c =>
      `<tr data-href="#/contract/${c.id}" tabindex="0"><td><span class="mono muted">${esc(c.contract_number)}</span><br>${esc(c.title)}</td>
        <td>${esc(c.organizations?.name || '—')}</td><td>${label(c.contract_type)}</td><td>${label(c.status)}</td>
        <td>${money(c.value, c.currency)}</td><td class="mono">${fmtDate(c.signed_date)}</td>
        <td class="mono">${esc(c.projects?.project_number || '—')}</td></tr>`).join('')}</tbody></table>`
      : '<p class="muted">No contracts yet.</p>'}`;
  wireRowLinks();
}

async function viewContract(id) {
  const params = new URLSearchParams(location.hash.split('?')[1] || '');
  const isNew = id.startsWith('new');
  let c = {};
  if (!isNew) {
    const { data, error } = await sb.from('contracts').select('*').eq('id', id).maybeSingle();
    if (error) return fail(error);
    if (!data) { $('#view').innerHTML = '<p class="muted">Contract not found, or your role cannot view it.</p>'; return; }
    c = data;
  } else {
    if (!canWriteContracts()) { $('#view').innerHTML = '<p class="muted">Your role cannot create contracts.</p>'; return; }
    c = { project_id: params.get('project'), lead_id: params.get('lead'), currency: 'INR', status: 'draft', contract_type: 'fixed_fee' };
    if (c.project_id) {
      const { data: p } = await sb.from('projects').select('name,organization_id,lead_id,design_responsibility').eq('id', c.project_id).maybeSingle();
      if (p) Object.assign(c, { title: p.name, organization_id: p.organization_id, lead_id: p.lead_id, design_responsibility: p.design_responsibility });
    } else if (c.lead_id) {
      const { data: l } = await sb.from('leads').select('company_name,organization_id').eq('id', c.lead_id).maybeSingle();
      if (l) Object.assign(c, { title: `Services agreement — ${l.company_name || 'Client'}`, organization_id: l.organization_id });
    }
  }
  const [orgs, projects] = await Promise.all([
    sb.from('organizations').select('id,name').order('name').limit(500),
    sb.from('projects').select('id,project_number,name').order('created_at', { ascending: false }).limit(500)]);
  const ro = !canWriteContracts();
  $('#view').innerHTML = `<a class="back" href="#/contracts">← Contracts</a>
    <h1 class="page-title">${isNew ? 'New contract' : esc(c.contract_number) + ' · ' + esc(c.title)}</h1>
    <section class="panel"><form id="contract-form" class="form-grid">
      <fieldset ${ro ? 'disabled' : ''} class="span2 form-grid" style="border:0;padding:0;margin:0">
      <label class="span2">Title<input id="c-title" required maxlength="200" value="${esc(c.title || '')}"></label>
      <label>Client<select id="c-org"><option value="">—</option>${(orgs.data || []).map(o =>
        `<option value="${o.id}"${o.id === c.organization_id ? ' selected' : ''}>${esc(o.name)}</option>`).join('')}</select></label>
      <label>Project<select id="c-project"><option value="">—</option>${(projects.data || []).map(p =>
        `<option value="${p.id}"${p.id === c.project_id ? ' selected' : ''}>${esc(p.project_number)} ${esc(p.name)}</option>`).join('')}</select></label>
      <label>Type<select id="c-type">${opts(CONTRACT_TYPES, c.contract_type)}</select></label>
      <label>Status<select id="c-status">${opts(CONTRACT_STATUS, c.status)}</select></label>
      <label>Value<input id="c-value" type="number" min="0" step="0.01" value="${esc(c.value ?? '')}"></label>
      <label>Currency<select id="c-cur">${opts(['INR', 'USD', 'GBP', 'EUR', 'AED', 'SAR', 'AUD', 'CAD'], c.currency)}</select></label>
      <label>Signed<input id="c-signed" type="date" value="${esc(c.signed_date || '')}"></label>
      <label>Start<input id="c-start" type="date" value="${esc(c.start_date || '')}"></label>
      <label>End<input id="c-end" type="date" value="${esc(c.end_date || '')}"></label>
      <label class="span2">Scope summary<textarea id="c-scope" rows="3">${esc(c.scope_summary || '')}</textarea></label>
      <label class="span2">Payment terms<textarea id="c-pay" rows="2" placeholder="e.g. 30% advance, 40% on coordinated model issue, 30% on handover">${esc(c.payment_terms || '')}</textarea></label>
      <label class="check span2"><input id="c-design" type="checkbox"${c.design_responsibility ? ' checked' : ''}>
        Engineering design responsibility is part of this contract (PKG-05)</label>
      ${ro ? '' : `<div class="span2"><button class="btn btn--primary" type="submit">${isNew ? 'Create contract' : 'Save contract'}</button></div>`}
      </fieldset></form></section>`;
  if (ro) return;
  $('#contract-form').addEventListener('submit', async e => {
    e.preventDefault();
    const row = { title: val('c-title'), organization_id: orNull(val('c-org')), project_id: orNull(val('c-project')),
      contract_type: val('c-type'), status: val('c-status'), value: val('c-value') ? Number(val('c-value')) : null,
      currency: val('c-cur'), signed_date: orNull(val('c-signed')), start_date: orNull(val('c-start')),
      end_date: orNull(val('c-end')), scope_summary: orNull(val('c-scope')), payment_terms: orNull(val('c-pay')),
      design_responsibility: $('#c-design').checked };
    if (isNew && c.lead_id) row.lead_id = c.lead_id;
    const res = isNew ? await sb.from('contracts').insert(row).select('id').single()
                      : await sb.from('contracts').update(row).eq('id', id).select('id').single();
    if (res.error) return fail(res.error);
    location.hash = '#/contract/' + res.data.id;
    if (!isNew) toast('Contract saved.');
  });
}

/* ------------------------------------------------------------------ team --- */
async function staffCall(body) {
  const { data: { session } } = await sb.auth.getSession();
  const r = await fetch(FN_STAFF, { method: 'POST', headers: { 'content-type': 'application/json',
    Authorization: 'Bearer ' + session.access_token, apikey: CFG.supabaseAnonKey }, body: JSON.stringify(body) });
  const out = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(out.error ? String(out.error).replace(/_/g, ' ') : 'request failed');
  return out;
}

async function viewTeam() {
  if (!has('admin')) { $('#view').innerHTML = '<p class="muted">Admins only.</p>'; return; }
  let users = [];
  try { users = (await staffCall({ action: 'list_users' })).users || []; } catch (e) { return fail(e); }
  $('#view').innerHTML = `<h1 class="page-title">Team</h1>
    <p class="muted">Add staff and engineers. A temporary password is shown once — share it privately; the person
    must change it at first sign-in. Engineers only see projects they are added to.</p>
    <section class="panel"><h2>Add a person</h2><form id="user-form" class="inline-form">
      <input id="u-name" placeholder="Full name" required maxlength="120">
      <input id="u-email" type="email" placeholder="Work email" required>
      <select id="u-role" aria-label="Role">${opts(ROLES, 'engineer')}</select>
      <button class="btn btn--primary btn--sm" type="submit">Create account</button></form>
      <div id="secret" hidden class="secret" role="status"></div></section>
    <section class="panel"><h2>People</h2><table class="table"><thead><tr><th>Name</th><th>Email</th><th>Role</th>
      <th>Status</th><th>Last sign-in</th><th></th></tr></thead><tbody>${users.map(u =>
      `<tr><td>${esc(u.full_name || '—')}</td><td>${esc(u.email)}</td>
        <td>${u.id === ME.id ? label(u.role) : `<select data-role="${u.id}" aria-label="Role">${opts(ROLES, u.role)}</select>`}</td>
        <td>${u.is_active ? 'Active' : '<span class="tag">DEACTIVATED</span>'}</td>
        <td class="mono">${fmtWhen(u.last_sign_in_at)}</td>
        <td>${u.id === ME.id ? '' : `<button class="linkbtn" data-reset="${u.id}">Reset password</button>
          <button class="linkbtn" data-active="${u.id}" data-to="${!u.is_active}">${u.is_active ? 'Deactivate' : 'Reactivate'}</button>`}</td></tr>`).join('')}
    </tbody></table></section>`;
  const showSecret = (who, pw) => {
    const box = $('#secret'); box.hidden = false;
    box.innerHTML = `<p><strong>Temporary password for ${esc(who)}</strong> — shown once, copy it now:</p>
      <p class="mono secret__pw">${esc(pw)}</p><p class="muted">They will be asked to choose their own password at first sign-in.</p>`;
  };
  $('#user-form').addEventListener('submit', async e => {
    e.preventDefault();
    try {
      const r = await staffCall({ action: 'create_user', full_name: val('u-name'), email: val('u-email'), role: val('u-role') });
      const who = val('u-email'); await viewTeam(); await loadUsers(); showSecret(who, r.temporary_password);
    } catch (err) { fail(err); }
  });
  $$('[data-role]').forEach(s => s.addEventListener('change', async () => {
    try { await staffCall({ action: 'set_role', user_id: s.dataset.role, role: s.value }); toast('Role updated.'); await loadUsers(); }
    catch (err) { fail(err); }
  }));
  $$('[data-active]').forEach(b => b.addEventListener('click', async () => {
    if (!confirm(b.dataset.to === 'true' ? 'Reactivate this account?' : 'Deactivate this account? They will be signed out.')) return;
    try { await staffCall({ action: 'set_active', user_id: b.dataset.active, active: b.dataset.to === 'true' }); viewTeam(); }
    catch (err) { fail(err); }
  }));
  $$('[data-reset]').forEach(b => b.addEventListener('click', async () => {
    if (!confirm('Issue a new temporary password for this person?')) return;
    try { const r = await staffCall({ action: 'reset_password', user_id: b.dataset.reset });
      showSecret(USERS.find(u => u.id === b.dataset.reset)?.email || 'user', r.temporary_password); }
    catch (err) { fail(err); }
  }));
}

/* --------------------------------------------------------------- account --- */
function viewAccount() {
  $('#view').innerHTML = `<h1 class="page-title">Account</h1>
    <section class="panel"><dl class="kvs">
      <div class="kv"><dt>Name</dt><dd>${esc(ME.full_name || '—')}</dd></div>
      <div class="kv"><dt>Email</dt><dd>${esc(ME.email)}</dd></div>
      <div class="kv"><dt>Role</dt><dd>${label(ME.role)}</dd></div></dl>
      <h2 style="margin-top:20px">Change password</h2>
      <form id="pw-form" class="inline-form">
        <input id="pw-1" type="password" autocomplete="new-password" minlength="12" placeholder="New password" required>
        <input id="pw-2" type="password" autocomplete="new-password" minlength="12" placeholder="Repeat" required>
        <button class="btn btn--sm" type="submit">Update password</button></form></section>`;
  $('#pw-form').addEventListener('submit', async e => {
    e.preventDefault();
    const a = val('pw-1');
    if (a !== val('pw-2')) return fail({ message: 'The passwords do not match.' });
    if (!(a.length >= 12 && /[A-Za-z]/.test(a) && /\d/.test(a) && /[^A-Za-z0-9]/.test(a)))
      return fail({ message: 'Use 12+ characters with letters, a number and a symbol.' });
    const { error } = await sb.auth.updateUser({ password: a });
    if (error) return fail(error); viewAccount(); toast('Password updated.');
  });
}

/* ---------------------------------------------------------------- router --- */
const ROUTES = [
  [/^#\/?$|^$/, viewDashboard],
  [/^#\/mywork$/, viewMyWork],
  [/^#\/leads$/, viewLeads],
  [/^#\/pipeline$/, viewPipeline],
  [/^#\/followups$/, viewFollowups],
  [/^#\/lead\/([0-9a-f-]{36})$/, viewLead],
  [/^#\/projects(\?board)?$/, viewProjects],
  [/^#\/project\/new$/, viewNewProject],
  [/^#\/project\/([0-9a-f-]{36})$/, viewProject],
  [/^#\/contracts$/, viewContracts],
  [/^#\/contract\/(new(?:\?.*)?|[0-9a-f-]{36})$/, viewContract],
  [/^#\/team$/, viewTeam],
  [/^#\/account$/, viewAccount]
];

async function route() {
  const h = location.hash;
  $$('#nav a').forEach(a => a.setAttribute('aria-current', h.startsWith(a.getAttribute('href')) &&
    (a.getAttribute('href') !== '#/' || h === '#/' || h === '') ? 'page' : 'false'));
  for (const [re, fn] of ROUTES) {
    const m = h.match(re);
    if (m) { $('#view').innerHTML = '<p class="muted">Loading…</p>'; try { await fn(m[1] && !m[1].startsWith('?') ? m[1] : undefined); } catch (e) { fail(e); } return; }
  }
  $('#view').innerHTML = '<p class="muted">Page not found.</p>';
}

let started = false;
async function start() {
  ME = await loadMe();
  if (!ME) { $('#login').hidden = false; $('#app').hidden = true; return; }
  if (ME.must_change) return showSetPassword();
  if (!ME.is_active) { await sb.auth.signOut(); $('#login').hidden = false;
    $('#login-error').textContent = 'This account is deactivated.'; return; }
  await loadUsers();
  $('#login').hidden = true; $('#setpw').hidden = true; $('#app').hidden = false;
  $('#me').textContent = `${ME.full_name || ME.email} · ${String(ME.role).replace(/_/g, ' ')}`;
  buildNav();
  if (!started) { window.addEventListener('hashchange', route); started = true; }
  route();
}

sb.auth.onAuthStateChange(event => { if (event === 'PASSWORD_RECOVERY') showSetPassword(); });
$('#login-form').addEventListener('submit', signIn);
$('#forgot').addEventListener('click', forgot);
$('#setpw-form').addEventListener('submit', savePassword);
$('#signout').addEventListener('click', async () => { await sb.auth.signOut(); location.hash = ''; location.reload(); });
start();

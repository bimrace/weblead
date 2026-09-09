/* ============================================================================
   BIMRACE — site behaviour. Vanilla JS, no dependencies, no build step.

   Every animation on this site explains a system. There is no decorative
   motion: a moving dot is data travelling a route, a sweep is a model being
   read, a log line is a step in a documented workflow. Colour is applied by
   CSS class only, so the whole site re-themes from the token block in
   style.css.

     1. helpers            6. digital twin composition
     2. hero model         7. navigation
     3. data-layer diagram 8. reveal + counters
     4. platform map       9. demonstration console
     5. workflow pipeline 10. forms, misc, boot
   ========================================================================== */
(function () {
  'use strict';

  /* ------------------------------------------------------------ 1. helpers */
  var NS = 'http://www.w3.org/2000/svg';
  var XLINK = 'http://www.w3.org/1999/xlink';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function el(tag, attrs, text) {
    var n = document.createElementNS(NS, tag);
    if (attrs) for (var k in attrs) if (attrs[k] !== null && attrs[k] !== undefined) n.setAttribute(k, attrs[k]);
    if (text != null) n.textContent = text;
    return n;
  }
  function h(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }
  function $(s, c) { return (c || document).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); }

  /* A dot travelling a path is always data moving between two named things. */
  function pulse(pathId, cls, dur, delay, r) {
    var dot = el('circle', { r: r || 3, class: 'm-pulse ' + cls });
    var m = el('animateMotion', { dur: dur + 's', begin: delay + 's', repeatCount: 'indefinite', rotate: 'auto' });
    var mp = el('mpath', { href: '#' + pathId });
    mp.setAttributeNS(XLINK, 'xlink:href', '#' + pathId);
    m.appendChild(mp); dot.appendChild(m);
    return dot;
  }

  /* --------------------------------------------------------- 2. hero model */
  /* An isometric MEP model being read: the sweep is the analysis pass, the
     flagged node is a coordination risk the pass has raised for review. */
  function heroModel() {
    var svg = document.getElementById('hero-svg');
    if (!svg) return;

    var W = 200, CX = 300, CY = 336, LEVELS = [0, 58, 116, 174, 232];
    function iso(x, y, z) { return [CX + (x - y) * 0.866, CY + (x + y) * 0.5 - z]; }
    function d(pts, close) {
      var s = '';
      for (var i = 0; i < pts.length; i++) {
        var p = iso(pts[i][0], pts[i][1], pts[i][2]);
        s += (i ? 'L' : 'M') + p[0].toFixed(1) + ' ' + p[1].toFixed(1);
      }
      return s + (close ? 'Z' : '');
    }

    var g = el('g'), gS = el('g'), gR = el('g'), gN = el('g');

    LEVELS.forEach(function (z, i) {
      gS.appendChild(el('path', {
        d: d([[0, 0, z], [W, 0, z], [W, W, z], [0, W, z]], true),
        class: i === LEVELS.length - 1 ? 'm-plate-top' : 'm-plate'
      }));
      [0.34, 0.68].forEach(function (t) {
        gS.appendChild(el('path', { d: d([[W * t, 0, z], [W * t, W, z]]), class: 'm-brace' }));
        gS.appendChild(el('path', { d: d([[0, W * t, z], [W, W * t, z]]), class: 'm-brace' }));
      });
    });
    [[0, 0], [W, 0], [W, W], [0, W]].forEach(function (c) {
      gS.appendChild(el('path', { d: d([[c[0], c[1], 0], [c[0], c[1], 232]]), class: 'm-col' }));
    });
    [[W * 0.34, W * 0.34], [W * 0.68, W * 0.68]].forEach(function (c) {
      gS.appendChild(el('path', { d: d([[c[0], c[1], 0], [c[0], c[1], 232]]), class: 'm-brace' }));
    });

    var runs = [
      { id: 'run-mech', sys: 'mech', dur: 4.2, pts: [[24, 52, 182], [170, 52, 182], [170, 150, 182], [66, 150, 182]] },
      { id: 'run-elec', sys: 'elec', dur: 5.4, pts: [[28, 158, 66], [28, 60, 66], [148, 60, 66], [148, 124, 66], [188, 124, 66]] },
      { id: 'run-plumb', sys: 'plumb', dur: 6.0, pts: [[152, 34, 12], [152, 34, 224], [78, 34, 224]] },
      { id: 'run-fire', sys: 'struct', dur: 5.0, pts: [[40, 96, 124], [186, 96, 124], [186, 40, 124]] }
    ];
    runs.forEach(function (r) {
      var p = d(r.pts);
      gR.appendChild(el('path', { d: p, class: 'm-glow m-glow--' + r.sys }));
      gR.appendChild(el('path', { d: p, id: r.id, class: 'm-run m-run--' + r.sys }));
    });
    if (!reduce) runs.forEach(function (r) {
      gR.appendChild(pulse(r.id, 'm-pulse--' + r.sys, r.dur, 0, 3.2));
      gR.appendChild(pulse(r.id, 'm-pulse--' + r.sys, r.dur, r.dur / 2, 2.2));
    });

    [{ p: [170, 52, 182], sys: 'mech', t: 'AHU-04 / SUPPLY DUCT', o: [46, -26] },
     { p: [148, 124, 66], sys: 'elec', t: 'CBL-TR-04 / LV DIST', o: [58, 16] },
     { p: [152, 34, 224], sys: 'plumb', t: 'RISER-P2 / DOMESTIC', o: [40, -34] }].forEach(function (n) {
      var p = iso(n.p[0], n.p[1], n.p[2]), lx = p[0] + n.o[0], ly = p[1] + n.o[1];
      gN.appendChild(el('path', {
        d: 'M' + p[0].toFixed(1) + ' ' + p[1].toFixed(1) + 'L' + lx.toFixed(1) + ' ' + ly.toFixed(1) + 'h18',
        class: 'm-leader'
      }));
      gN.appendChild(el('circle', { cx: p[0].toFixed(1), cy: p[1].toFixed(1), r: 4, class: 'm-node m-node--' + n.sys }));
      gN.appendChild(el('text', { x: (lx + 24).toFixed(1), y: (ly + 3.5).toFixed(1), class: 'm-label' }, n.t));
    });

    /* the flagged intersection — an output of the analysis pass, not decoration */
    var fp = iso(186, 96, 124);
    var gF = el('g');
    gF.appendChild(el('rect', { x: fp[0] - 9, y: fp[1] - 9, width: 18, height: 18, rx: 2, class: 'm-flag' }));
    gF.appendChild(el('path', {
      d: 'M' + (fp[0] + 9) + ' ' + (fp[1] - 9) + 'l30 -22h58', class: 'm-leader m-anno'
    }));
    gF.appendChild(el('text', { x: fp[0] + 44, y: fp[1] - 34, class: 'm-flag-t m-anno' }, 'CLR-014  CLEARANCE 42mm'));
    if (!reduce) {
      var fa = el('animate', { attributeName: 'opacity', values: '1;.35;1', dur: '2.6s', repeatCount: 'indefinite' });
      gF.appendChild(fa);
    }

    ['L01  +0.000', 'L02  +3.600', 'L03  +7.200', 'L04  +10.800', 'L05  +14.400'].forEach(function (t, i) {
      var p = iso(0, W, LEVELS[i]);
      gN.appendChild(el('path', { d: 'M' + (p[0] - 10).toFixed(1) + ' ' + p[1].toFixed(1) + 'h-14', class: 'm-leader' }));
      gN.appendChild(el('text', { x: (p[0] - 30).toFixed(1), y: (p[1] + 3.5).toFixed(1), class: 'm-label', 'text-anchor': 'end' }, t));
    });

    if (!reduce) {
      var sweep = el('g', { opacity: '.8' });
      sweep.appendChild(el('path', { d: d([[0, 0, 0], [W, 0, 0], [W, W, 0], [0, W, 0]], true), class: 'm-scan' }));
      sweep.appendChild(el('animateTransform', {
        attributeName: 'transform', type: 'translate', values: '0 8; 0 -236; 0 8',
        dur: '11s', repeatCount: 'indefinite', calcMode: 'spline',
        keyTimes: '0;0.5;1', keySplines: '0.4 0 0.2 1;0.4 0 0.2 1'
      }));
      g.appendChild(sweep);
    }

    g.appendChild(gS); g.appendChild(gR); g.appendChild(gN); g.appendChild(gF);
    svg.appendChild(g);

    /* On phones the annotation type falls below legibility, so the drawing
       crops to the model and the callouts step aside. */
    var mq = window.matchMedia('(max-width: 720px)');
    function fit() {
      var narrow = mq.matches;
      svg.setAttribute('viewBox', narrow ? '104 74 372 486' : '0 0 640 570');
      gN.style.display = narrow ? 'none' : '';
      Array.prototype.forEach.call(gF.querySelectorAll('.m-anno'), function (n) {
        n.style.display = narrow ? 'none' : '';
      });
    }
    fit();
    if (mq.addEventListener) mq.addEventListener('change', fit); else if (mq.addListener) mq.addListener(fit);
    if (reduce && svg.pauseAnimations) svg.pauseAnimations();
  }

  /* -------------------------------------------------- 3. data-layer diagram */
  /* "Your model is an engineering database." The centre is the model; the ring
     is what it actually holds once it is authored information-first. */
  function dataDiagram() {
    var svg = document.getElementById('data-svg');
    if (!svg) return;
    var CX = 450, CY = 305, RX = 328, RY = 222;
    var fields = [
      'Geometry', 'Parameters', 'Systems', 'Equipment',
      'Relationships', 'Quantities', 'Specifications', 'Spatial data'
    ];
    var gE = el('g'), gC = el('g');

    fields.forEach(function (label, i) {
      var a = (Math.PI * 2 * i) / fields.length - Math.PI / 2;
      var x = CX + Math.cos(a) * RX, y = CY + Math.sin(a) * RY;
      var dd = 'M' + (CX + Math.cos(a) * 72).toFixed(1) + ' ' + (CY + Math.sin(a) * 72).toFixed(1) +
              'Q' + (CX + Math.cos(a) * RX * 0.52).toFixed(1) + ' ' + (CY + Math.sin(a) * RY * 0.86).toFixed(1) +
              ' ' + x.toFixed(1) + ' ' + y.toFixed(1);
      var id = 'dedge-' + i;
      gE.appendChild(el('path', { d: dd, class: 'd-link' }));
      gE.appendChild(el('path', { d: dd, id: id, class: 'd-link d-link--live', opacity: '.6' }));
      if (!reduce) gE.appendChild(pulse(id, 'm-pulse--mech', 2.8 + (i % 3) * 0.7, i * 0.3, 2.4));

      var w = Math.max(126, label.length * 8 + 40);
      gC.appendChild(el('rect', { x: x - w / 2, y: y - 19, width: w, height: 38, rx: 3, class: 'd-node' }));
      gC.appendChild(el('rect', { x: x - w / 2, y: y - 19, width: 2.5, height: 38, class: 'd-bar' }));
      gC.appendChild(el('text', { x: x + 8, y: y + 4.5, class: 'd-t', 'text-anchor': 'middle' }, label));
    });

    var gCore = el('g');
    [106, 88].forEach(function (r) { gCore.appendChild(el('circle', { cx: CX, cy: CY, r: r, class: 'd-ring' })); });
    gCore.appendChild(el('circle', { cx: CX, cy: CY, r: 72, class: 'd-hub' }));
    gCore.appendChild(el('text', { x: CX, y: CY - 6, class: 'd-ht', 'text-anchor': 'middle' }, 'BIM MODEL'));
    gCore.appendChild(el('text', { x: CX, y: CY + 16, class: 'd-hs', 'text-anchor': 'middle' }, 'STRUCTURED DATA'));
    if (!reduce) {
      var halo = el('circle', { cx: CX, cy: CY, r: 106, class: 'd-ring', opacity: '.5' });
      halo.appendChild(el('animate', { attributeName: 'r', values: '106;136;106', dur: '5.5s', repeatCount: 'indefinite' }));
      halo.appendChild(el('animate', { attributeName: 'opacity', values: '.5;0;.5', dur: '5.5s', repeatCount: 'indefinite' }));
      gCore.insertBefore(halo, gCore.firstChild);
    }
    svg.appendChild(gE); svg.appendChild(gC); svg.appendChild(gCore);
    if (reduce && svg.pauseAnimations) svg.pauseAnimations();
  }

  /* --------------------------------------------------------- 4. platform map */
  function platformMap() {
    var svg = document.getElementById('platform-svg');
    if (!svg) return;
    var HUB = { x: 450, y: 232, w: 272, h: 84 };
    var nodes = [
      { x: 112, y: 54, t: 'Revit / IFC', s: 'MODEL SOURCE' },
      { x: 322, y: 54, t: 'Engineering rules', s: 'RULE SETS' },
      { x: 578, y: 54, t: 'Calculation', s: 'SIZING / LOADS' },
      { x: 788, y: 54, t: 'Project data', s: 'CDE / TRACKERS' },
      { x: 190, y: 410, t: 'Automation', s: 'EXECUTION' },
      { x: 450, y: 410, t: 'Validation', s: 'ENGINEER REVIEW' },
      { x: 710, y: 410, t: 'Engineering output', s: 'MODEL / REPORT / BOQ' }
    ];
    var gL = el('g'), gN = el('g');
    nodes.forEach(function (n, i) {
      var top = n.y < HUB.y;
      var sy = top ? n.y + 27 : n.y - 27;
      var ey = top ? HUB.y - HUB.h / 2 : HUB.y + HUB.h / 2;
      var my = (sy + ey) / 2;
      var dd = 'M' + n.x + ' ' + sy + 'C' + n.x + ' ' + my + ' ' + HUB.x + ' ' + my + ' ' + HUB.x + ' ' + ey;
      var id = 'plink-' + i;
      gL.appendChild(el('path', { d: dd, class: 'd-link' }));
      gL.appendChild(el('path', { d: dd, id: id, class: 'd-link d-link--live', opacity: '.75' }));
      if (!reduce) gL.appendChild(pulse(id, 'm-pulse--mech', 3 + (i % 4) * 0.55, i * 0.42, 2.6));
      gN.appendChild(el('rect', { x: n.x - 94, y: n.y - 27, width: 188, height: 54, rx: 3, class: 'd-node' }));
      gN.appendChild(el('rect', { x: n.x - 94, y: n.y - 27, width: 3, height: 54, class: 'd-bar' }));
      gN.appendChild(el('text', { x: n.x - 78, y: n.y - 3, class: 'd-t' }, n.t));
      gN.appendChild(el('text', { x: n.x - 78, y: n.y + 15, class: 'd-s' }, n.s));
    });
    var gH = el('g');
    gH.appendChild(el('rect', { x: HUB.x - HUB.w / 2 - 10, y: HUB.y - HUB.h / 2 - 10, width: HUB.w + 20, height: HUB.h + 20, rx: 5, class: 'd-ring' }));
    gH.appendChild(el('rect', { x: HUB.x - HUB.w / 2, y: HUB.y - HUB.h / 2, width: HUB.w, height: HUB.h, rx: 4, class: 'd-hub' }));
    gH.appendChild(el('text', { x: HUB.x, y: HUB.y - 4, class: 'd-ht', 'text-anchor': 'middle' }, 'ORCHESTRATION'));
    gH.appendChild(el('text', { x: HUB.x, y: HUB.y + 18, class: 'd-hs', 'text-anchor': 'middle' }, 'REASON / ROUTE / RECORD'));
    svg.appendChild(gL); svg.appendChild(gN); svg.appendChild(gH);
    if (reduce && svg.pauseAnimations) svg.pauseAnimations();
  }

  /* ----------------------------------------------------- 5. workflow pipeline */
  /* Engineering intent to engineering output, drawn as a single line so the
     hand-off points are visible: the amber node is where a person signs. */
  function workflowPipe() {
    var svg = document.getElementById('pipe-svg');
    if (!svg) return;
    var stages = [
      ['Engineering intent', 'BRIEF / QUERY', 'human'],
      ['Interpretation', 'SCOPE + RULES', 'ai'],
      ['BIM model', 'REVIT / IFC', 'data'],
      ['Calculation', 'SIZING / LOADS', 'data'],
      ['Rule engine', 'STANDARDS', 'data'],
      ['Analysis', 'PATTERN / RISK', 'ai'],
      ['Automation', 'EXECUTE', 'ai'],
      ['QA / QC', 'CHECK', 'data'],
      ['Engineer approval', 'SIGN-OFF', 'human'],
      ['Output', 'MODEL / REPORT', 'data']
    ];
    /* PAD keeps the first and last labels inside the viewBox; they are
       anchored to their outer edge rather than centred for the same reason. */
    var W = 1200, PAD = 92, y = 96, last = stages.length - 1;
    var step = (W - PAD * 2) / (stages.length - 1);
    var gL = el('g'), gN = el('g');

    var dPath = 'M' + PAD + ' ' + y + 'H' + (W - PAD);
    gL.appendChild(el('path', { d: dPath, class: 'd-link' }));
    gL.appendChild(el('path', { d: dPath, id: 'pipe-line', class: 'd-link d-link--live' }));
    if (!reduce) {
      [0, 2.6, 5.2].forEach(function (t) {
        gL.appendChild(pulse('pipe-line', 'm-pulse--mech', 7.8, t, 3));
      });
    }

    stages.forEach(function (s, i) {
      var x = PAD + step * i;
      var isHuman = s[2] === 'human', isAI = s[2] === 'ai';
      gN.appendChild(el('circle', {
        cx: x, cy: y, r: isHuman ? 8 : 6,
        fill: isHuman ? 'var(--elec)' : (isAI ? 'var(--sig)' : 'var(--surface-0)'),
        stroke: isHuman ? 'var(--elec)' : 'var(--sig)', 'stroke-width': 1.4
      }));
      var up = i % 2 === 0;
      var ty = up ? y - 26 : y + 40;
      gN.appendChild(el('path', {
        d: 'M' + x + ' ' + (up ? y - 10 : y + 10) + 'V' + (up ? ty + 12 : ty - 22), class: 'm-leader'
      }));
      var anchor = i === 0 ? 'start' : (i === last ? 'end' : 'middle');
      var tx = i === 0 ? x - 26 : (i === last ? x + 26 : x);
      var t1 = el('text', { x: tx, y: ty, class: 'd-t', 'text-anchor': anchor, 'font-size': '12.5' }, s[0]);
      var t2 = el('text', { x: tx, y: ty + (up ? -15 : 15), class: 'd-s', 'text-anchor': anchor }, s[1]);
      if (isHuman) t2.setAttribute('fill', 'var(--elec)');
      gN.appendChild(t1); gN.appendChild(t2);
    });
    svg.appendChild(gL); svg.appendChild(gN);
    if (reduce && svg.pauseAnimations) svg.pauseAnimations();
  }

  /* ------------------------------------------------ 6. digital twin composite */
  function twinDiagram() {
    var svg = document.getElementById('twin-svg');
    if (!svg) return;
    var inputs = [
      ['BIM model', 'GEOMETRY + DATA', 'live'],
      ['Asset data', 'REGISTER / SPEC', 'live'],
      ['Live telemetry', 'BMS / IOT', 'road'],
      ['Engineering rules', 'DESIGN INTENT', 'dev'],
      ['Analytics', 'PATTERN / TREND', 'road']
    ];
    var X = 150, W = 218, H = 52, GAP = 18, TOP = 40;
    var OX = 616, OY = TOP + (inputs.length * (H + GAP) - GAP) / 2;
    var gL = el('g'), gN = el('g');

    inputs.forEach(function (n, i) {
      var y = TOP + i * (H + GAP) + H / 2;
      var dd = 'M' + (X + W / 2) + ' ' + y + 'C' + (X + W / 2 + 110) + ' ' + y + ' ' + (OX - 186) + ' ' + OY + ' ' + (OX - 106) + ' ' + OY;
      var id = 'tlink-' + i;
      gL.appendChild(el('path', { d: dd, class: 'd-link' }));
      gL.appendChild(el('path', { d: dd, id: id, class: 'd-link d-link--live', opacity: n[2] === 'live' ? '.8' : '.3' }));
      if (!reduce && n[2] === 'live') gL.appendChild(pulse(id, 'm-pulse--mech', 3.4 + i * 0.4, i * 0.5, 2.6));

      gN.appendChild(el('rect', { x: X - W / 2, y: y - H / 2, width: W, height: H, rx: 3, class: 'd-node' }));
      gN.appendChild(el('rect', {
        x: X - W / 2, y: y - H / 2, width: 3, height: H,
        fill: n[2] === 'live' ? 'var(--sig)' : (n[2] === 'dev' ? 'var(--elec)' : 'var(--text-4)')
      }));
      gN.appendChild(el('text', { x: X - W / 2 + 18, y: y - 3, class: 'd-t' }, n[0]));
      gN.appendChild(el('text', { x: X - W / 2 + 18, y: y + 15, class: 'd-s' }, n[1]));
    });

    var gH = el('g');
    gH.appendChild(el('circle', { cx: OX, cy: OY, r: 100, class: 'd-ring' }));
    gH.appendChild(el('circle', { cx: OX, cy: OY, r: 84, class: 'd-hub' }));
    gH.appendChild(el('text', { x: OX, y: OY - 6, class: 'd-ht', 'text-anchor': 'middle' }, 'DIGITAL TWIN'));
    gH.appendChild(el('text', { x: OX, y: OY + 16, class: 'd-hs', 'text-anchor': 'middle' }, 'ROADMAP'));
    svg.appendChild(gL); svg.appendChild(gN); svg.appendChild(gH);
    if (reduce && svg.pauseAnimations) svg.pauseAnimations();
  }

  /* --------------------------------------------------------- 7. navigation */
  function nav() {
    var toggle = document.getElementById('nav-toggle');
    var links = document.getElementById('nav-links');
    if (!toggle || !links) return;

    function setMenu(open) {
      links.classList.toggle('is-open', open);
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      document.body.style.overflow = open ? 'hidden' : '';
    }
    toggle.addEventListener('click', function () {
      setMenu(toggle.getAttribute('aria-expanded') !== 'true');
    });
    links.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
    window.addEventListener('resize', function () {
      if (window.innerWidth > 980 && links.classList.contains('is-open')) setMenu(false);
    });

    $$('.has-menu').forEach(function (item) {
      var btn = $('button', item);
      function open(state) {
        item.setAttribute('data-open', state ? 'true' : 'false');
        btn.setAttribute('aria-expanded', state ? 'true' : 'false');
      }
      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        open(item.getAttribute('data-open') !== 'true');
      });
      if (window.matchMedia('(hover: hover)').matches) {
        item.addEventListener('mouseenter', function () { if (window.innerWidth > 980) open(true); });
        item.addEventListener('mouseleave', function () { if (window.innerWidth > 980) open(false); });
      }
      item.addEventListener('focusout', function (e) {
        if (window.innerWidth > 980 && !item.contains(e.relatedTarget)) open(false);
      });
    });

    document.addEventListener('click', function (e) {
      $$('.has-menu').forEach(function (i) { if (!i.contains(e.target)) i.setAttribute('data-open', 'false'); });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape') return;
      $$('.has-menu').forEach(function (i) {
        i.setAttribute('data-open', 'false');
        var b = $('button', i); if (b) b.setAttribute('aria-expanded', 'false');
      });
      if (links.classList.contains('is-open')) { setMenu(false); toggle.focus(); }
    });
  }

  /* ------------------------------------------------ 8. reveal and counters */
  function reveal() {
    if (reduce || !('IntersectionObserver' in window)) return;
    var items = [];
    ['.sec-head', '.card', '.layer', '.agent', '.flow', '.mat__l', '.ind', '.spec__row',
     '.slot', '.case', '.hero__copy', '.panel', '.dia', '.form', '.phero__in > div',
     '.mcol', '.chain > div', '.badge-legend > div'].forEach(function (s) {
      $$(s).forEach(function (n) { if (items.indexOf(n) === -1) items.push(n); });
    });
    items.forEach(function (n) { n.classList.add('reveal'); });
    var io = new IntersectionObserver(function (es, obs) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        var sib = Array.prototype.slice.call(e.target.parentNode.children);
        e.target.style.setProperty('--d', Math.min(sib.indexOf(e.target), 5) * 55 + 'ms');
        e.target.classList.add('is-in');
        obs.unobserve(e.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
    items.forEach(function (n) { io.observe(n); });
  }

  function counters() {
    var cells = $$('[data-count]');
    if (!cells.length) return;
    function run(n) {
      var target = parseFloat(n.getAttribute('data-count')) || 0;
      var dec = (n.getAttribute('data-dec') | 0);
      var suffix = n.getAttribute('data-suffix') || '';
      function show(v) {
        n.textContent = (dec ? v.toFixed(dec) : Math.round(v).toLocaleString()) + suffix;
      }
      if (reduce) { show(target); return; }
      var t0 = performance.now();
      (function frame(now) {
        var t = Math.min(1, (now - t0) / 1300);
        show(target * (1 - Math.pow(1 - t, 3)));
        if (t < 1) requestAnimationFrame(frame);
      })(t0);
    }
    if (!('IntersectionObserver' in window)) { cells.forEach(run); return; }
    var io = new IntersectionObserver(function (es, obs) {
      es.forEach(function (e) { if (e.isIntersecting) { run(e.target); obs.unobserve(e.target); } });
    }, { threshold: 0.5 });
    cells.forEach(function (c) { io.observe(c); });
  }

  /* Bars inside the console fill to their declared percentage once visible. */
  function bars() {
    var list = $$('.cm__bar i');
    if (!list.length) return;
    function fill(b) { b.style.width = (b.getAttribute('data-pct') || 0) + '%'; }
    if (!('IntersectionObserver' in window) || reduce) { list.forEach(fill); return; }
    var io = new IntersectionObserver(function (es, obs) {
      es.forEach(function (e) { if (e.isIntersecting) { fill(e.target); obs.unobserve(e.target); } });
    }, { threshold: 0.4 });
    list.forEach(function (b) { io.observe(b); });
  }

  /* Hovering or focusing a stack layer highlights it; keyboard users get the
     same affordance through focus. */
  function stackFocus() {
    var layers = $$('.layer');
    if (!layers.length) return;
    layers.forEach(function (l) {
      l.addEventListener('focusin', function () { l.classList.add('is-active'); });
      l.addEventListener('focusout', function () { l.classList.remove('is-active'); });
    });
  }

  /* -------------------------------------------- 9. demonstration console -- */
  /* Three scripted engineering queries. Every figure here is fabricated for
     demonstration and the interface says so in two places: the panel bar and
     the caption. Nothing in this component talks to a real model. */
  var SCENARIOS = {
    chw: {
      label: 'Chilled water system',
      query: 'Check the chilled water system on MEP_COORDINATION_R04.',
      metrics: [
        { k: 'Elements read', v: '4,212', cls: '', pct: 100 },
        { k: 'Pipe segments', v: '1,864', cls: '', pct: 82 },
        { k: 'Rules applied', v: '318', cls: '', pct: 74 },
        { k: 'Findings', v: '7', cls: 'cm--warn', pct: 34 }
      ],
      lines: [
        ['00.04', 'run', 'Loading federated model MEP_COORDINATION_R04'],
        ['00.31', 'ok', 'Model structure validated — 27 systems identified'],
        ['00.58', 'ok', 'Chilled water system resolved: 1,864 segments, 42 terminals'],
        ['01.12', 'run', 'Reading diameters, flow rates and insulation parameters'],
        ['01.44', 'warn', 'DN150 branch CHW-B-07 carries flow sized for DN200 upstream'],
        ['01.51', 'warn', '4 segments missing design flow parameter'],
        ['02.06', 'risk', 'Pump head check fails on index run — review required'],
        ['02.19', 'ok', 'Report drafted: 7 findings, 3 requiring engineer decision'],
        ['02.20', 'run', 'Held for engineering review — no model change written']
      ]
    },
    fire: {
      label: 'Fire protection coordination',
      query: 'Find fire protection coordination issues above the level 3 ceiling.',
      metrics: [
        { k: 'Elements read', v: '18,462', cls: '', pct: 100 },
        { k: 'Sprinkler heads', v: '486', cls: '', pct: 66 },
        { k: 'Clearance rules', v: '112', cls: '', pct: 58 },
        { k: 'High priority', v: '3', cls: 'cm--risk', pct: 22 }
      ],
      lines: [
        ['00.06', 'run', 'Isolating level 3 ceiling void, 2,800mm to 3,400mm SSL'],
        ['00.29', 'ok', 'Fire protection network resolved — 486 heads, 61 branch lines'],
        ['00.47', 'run', 'Testing clearance against duct, tray and structure'],
        ['01.08', 'risk', 'CLR-014 — 42mm clearance to AHU-04 supply duct, 150mm required'],
        ['01.15', 'risk', 'CLR-022 — sprinkler branch conflicts with primary beam web'],
        ['01.24', 'risk', 'CLR-031 — head obstructed by cable tray within 300mm'],
        ['01.38', 'warn', '9 further issues classified low priority'],
        ['01.52', 'ok', 'Issues classified, prioritised and grouped by responsible discipline'],
        ['01.53', 'run', 'Awaiting coordinator triage — nothing issued automatically']
      ]
    },
    qa: {
      label: 'Model QA pass',
      query: 'Run the standards QA pass before the Friday issue.',
      metrics: [
        { k: 'Elements read', v: '18,462', cls: '', pct: 100 },
        { k: 'Checks run', v: '1,284', cls: '', pct: 100 },
        { k: 'Pass rate', v: '96.2%', cls: 'cm--ok', pct: 96 },
        { k: 'Blocking', v: '2', cls: 'cm--risk', pct: 14 }
      ],
      lines: [
        ['00.03', 'run', 'Loading project rule set BR-QA-STD-v4'],
        ['00.22', 'ok', 'Naming convention: 18,204 of 18,462 elements conform'],
        ['00.40', 'warn', '258 elements fail naming — 241 are one family, likely a template fault'],
        ['00.58', 'ok', 'Shared coordinates and levels aligned across all four models'],
        ['01.11', 'warn', '32 elements missing required classification parameter'],
        ['01.26', 'risk', 'Two views issued at wrong status code — blocks issue'],
        ['01.40', 'ok', 'Schedules reconcile against model quantities'],
        ['01.55', 'ok', 'QA report generated with element IDs for every finding'],
        ['01.56', 'run', 'Engineer sign-off required before status change']
      ]
    }
  };

  function console_() {
    var root = document.getElementById('console');
    if (!root) return;
    var grid = $('#console-metrics', root);
    var log = $('#console-log', root);
    var qEl = $('#console-query', root);
    var btns = $$('.console__act button', root);
    var timers = [];

    function clearTimers() { timers.forEach(clearTimeout); timers = []; }

    function render(key) {
      var s = SCENARIOS[key];
      if (!s) return;
      clearTimers();
      btns.forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-scenario') === key ? 'true' : 'false'); });
      if (qEl) qEl.textContent = s.query;

      grid.textContent = '';
      s.metrics.forEach(function (m) {
        var cell = h('div', 'cm ' + m.cls);
        cell.appendChild(h('span', 'cm__k', m.k));
        cell.appendChild(h('span', 'cm__v', m.v));
        var bar = h('div', 'cm__bar'), i = document.createElement('i');
        i.setAttribute('data-pct', m.pct);
        bar.appendChild(i); cell.appendChild(bar);
        grid.appendChild(cell);
        requestAnimationFrame(function () { i.style.width = m.pct + '%'; });
      });

      log.textContent = '';
      s.lines.forEach(function (ln, idx) {
        var row = h('div', 'log__l log__l--' + ln[1]);
        row.appendChild(h('span', 'log__t', ln[0]));
        row.appendChild(h('span', 'log__m', ln[2]));
        log.appendChild(row);
        if (reduce) { row.classList.add('is-in'); return; }
        timers.push(setTimeout(function () { row.classList.add('is-in'); }, 160 + idx * 340));
      });
      var cur = h('div', 'log__l');
      var ci = document.createElement('span'); ci.className = 'log__cursor';
      cur.appendChild(h('span', 'log__t', '')); cur.appendChild(ci);
      log.appendChild(cur);
      if (reduce) cur.classList.add('is-in');
      else timers.push(setTimeout(function () { cur.classList.add('is-in'); }, 160 + s.lines.length * 340));
    }

    btns.forEach(function (b) {
      b.addEventListener('click', function () { render(b.getAttribute('data-scenario')); });
    });

    if ('IntersectionObserver' in window && !reduce) {
      var io = new IntersectionObserver(function (es, obs) {
        es.forEach(function (e) { if (e.isIntersecting) { render('fire'); obs.unobserve(e.target); } });
      }, { threshold: 0.25 });
      io.observe(root);
    } else {
      render('fire');
    }
  }

  /* -------------------------------------------------- 10. forms and misc -- */
  function form() {
    var f = document.getElementById('enquiry-form');
    if (!f) return;

    var RULES = {
      'f-name': [function (v) { return v.trim().length >= 2; }, 'Please enter your name.'],
      'f-company': [function (v) { return v.trim().length >= 2; }, 'Please enter your company.'],
      'f-email': [function (v) { return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()); }, 'Please enter a valid business email address.'],
      'f-msg': [function (v) { return v.trim().length >= 20; }, 'Please describe the scope in a little more detail.']
    };

    function check(id) {
      var input = document.getElementById(id);
      var msg = $('.err[data-for="' + id + '"]');
      if (!input || !RULES[id]) return true;
      var ok = RULES[id][0](input.value);
      input.setAttribute('aria-invalid', ok ? 'false' : 'true');
      if (msg) msg.textContent = ok ? '' : RULES[id][1];
      return ok;
    }

    Object.keys(RULES).forEach(function (id) {
      var input = document.getElementById(id);
      if (!input) return;
      input.addEventListener('blur', function () { check(id); });
      input.addEventListener('input', function () {
        if (input.getAttribute('aria-invalid') === 'true') check(id);
      });
    });

    f.addEventListener('submit', function (e) {
      var bad = Object.keys(RULES).filter(function (id) { return !check(id); });
      if (bad.length) {
        e.preventDefault();
        var first = document.getElementById(bad[0]);
        if (first) { first.focus(); first.scrollIntoView({ block: 'center', behavior: reduce ? 'auto' : 'smooth' }); }
      }
    });
  }

  function portrait() {
    var img = $('.founder__photo');
    if (!img) return;
    var frame = img.closest('.founder__frame');
    function fail() { if (frame) frame.classList.add('is-missing'); img.style.display = 'none'; }
    img.addEventListener('error', fail);
    if (img.complete && img.naturalWidth === 0) fail();
  }

  function legalToc() {
    var toc = document.getElementById('legal-toc');
    if (!toc || !('IntersectionObserver' in window)) return;
    var links = $$('a[href^="#"]', toc);
    var secs = links.map(function (a) { return $(a.getAttribute('href')); }).filter(Boolean);
    if (!secs.length) return;
    var spy = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        links.forEach(function (a) { a.classList.toggle('is-active', a.getAttribute('href') === '#' + e.target.id); });
      });
    }, { rootMargin: '-20% 0px -70% 0px' });
    secs.forEach(function (s) { spy.observe(s); });
  }

  function boot() {
    try {
      heroModel(); dataDiagram(); platformMap(); workflowPipe(); twinDiagram();
      nav(); reveal(); counters(); bars(); stackFocus(); console_();
      portrait(); legalToc(); form();
    } catch (err) {
      if (window.console && window.console.error) window.console.error('[BIMRACE]', err);
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();

/* ============================================================================
   BIMRACE — site behaviour. Vanilla JS, no dependencies, no build step.
     1. Helpers          5. Navigation
     2. Hero model       6. Scroll reveal + counters
     3. AI diagram       7. Enquiry form validation
     4. Platform map     8. Boot
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
  function $(s, c) { return (c || document).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); }

  /* Colour is set by CSS class, never by a hex value here, so the whole site
     can be re-themed from the token block in style.css. */
  function pulse(pathId, cls, dur, delay, r) {
    var dot = el('circle', { r: r || 3, class: 'm-pulse ' + cls });
    var m = el('animateMotion', { dur: dur + 's', begin: delay + 's', repeatCount: 'indefinite', rotate: 'auto' });
    var mp = el('mpath', { href: '#' + pathId });
    mp.setAttributeNS(XLINK, 'xlink:href', '#' + pathId);
    m.appendChild(mp); dot.appendChild(m);
    return dot;
  }

  /* --------------------------------------------------------- 2. hero model */
  function heroModel() {
    var svg = document.getElementById('hero-svg');
    if (!svg) return;

    var W = 200, CX = 292, CY = 332, LEVELS = [0, 58, 116, 174, 232];
    function iso(x, y, z) { return [CX + (x - y) * 0.866, CY + (x + y) * 0.5 - z]; }
    function d(pts, close) {
      var s = '';
      for (var i = 0; i < pts.length; i++) {
        var p = iso(pts[i][0], pts[i][1], pts[i][2]);
        s += (i ? 'L' : 'M') + p[0].toFixed(1) + ' ' + p[1].toFixed(1);
      }
      return s + (close ? 'Z' : '');
    }

    var g = el('g', { id: 'hero-model' }), gS = el('g'), gR = el('g'), gN = el('g');

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
      { id: 'run-plumb', sys: 'plumb', dur: 6.0, pts: [[152, 34, 12], [152, 34, 224], [78, 34, 224]] }
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

    [{ p: [170, 52, 182], sys: 'mech', t: 'DUCT-01 / SUPPLY AIR', o: [46, -26] },
     { p: [148, 124, 66], sys: 'elec', t: 'CBL-TR-04 / LV DIST', o: [58, 16] },
     { p: [152, 34, 224], sys: 'plumb', t: 'RISER-P2 / DOMESTIC', o: [40, -34] }].forEach(function (n) {
      var p = iso(n.p[0], n.p[1], n.p[2]), lx = p[0] + n.o[0], ly = p[1] + n.o[1];
      gN.appendChild(el('path', {
        d: 'M' + p[0].toFixed(1) + ' ' + p[1].toFixed(1) + 'L' + lx.toFixed(1) + ' ' + ly.toFixed(1) + 'h18',
        class: 'm-leader', fill: 'none'
      }));
      gN.appendChild(el('circle', { cx: p[0].toFixed(1), cy: p[1].toFixed(1), r: 4, class: 'm-node m-node--' + n.sys }));
      gN.appendChild(el('text', { x: (lx + 24).toFixed(1), y: (ly + 3.5).toFixed(1), class: 'm-label' }, n.t));
    });

    ['L01  +0.000', 'L02  +3.600', 'L03  +7.200', 'L04  +10.800', 'L05  +14.400'].forEach(function (t, i) {
      var p = iso(0, W, LEVELS[i]);
      gN.appendChild(el('path', { d: 'M' + (p[0] - 10).toFixed(1) + ' ' + p[1].toFixed(1) + 'h-14', class: 'm-leader', fill: 'none' }));
      gN.appendChild(el('text', { x: (p[0] - 30).toFixed(1), y: (p[1] + 3.5).toFixed(1), class: 'm-label', 'text-anchor': 'end' }, t));
    });

    if (!reduce) {
      var sweep = el('g', { opacity: '.7' });
      sweep.appendChild(el('path', { d: d([[0, 0, 0], [W, 0, 0], [W, W, 0], [0, W, 0]], true), class: 'm-scan', fill: 'none' }));
      sweep.appendChild(el('animateTransform', {
        attributeName: 'transform', type: 'translate', values: '0 8; 0 -236; 0 8',
        dur: '11s', repeatCount: 'indefinite', calcMode: 'spline',
        keyTimes: '0;0.5;1', keySplines: '0.4 0 0.2 1;0.4 0 0.2 1'
      }));
      g.appendChild(sweep);
    }

    g.appendChild(gS); g.appendChild(gR); g.appendChild(gN);
    svg.appendChild(g);

    /* On phones the annotation type scales below legibility, so the drawing
       crops to the model and the callouts step aside. */
    var mq = window.matchMedia('(max-width: 720px)');
    function fit() {
      svg.setAttribute('viewBox', mq.matches ? '96 74 372 476' : '0 0 620 560');
      gN.style.display = mq.matches ? 'none' : '';
    }
    fit();
    if (mq.addEventListener) mq.addEventListener('change', fit); else if (mq.addListener) mq.addListener(fit);
    if (reduce && svg.pauseAnimations) svg.pauseAnimations();
  }

  /* --------------------------------------------------------- 3. AI diagram */
  function aiDiagram() {
    var svg = document.getElementById('ai-svg');
    if (!svg) return;
    var CX = 450, CY = 310, RX = 322, RY = 226;
    var labels = ['Architectural Model', 'Structural Model', 'Mechanical', 'Electrical',
                  'Plumbing', 'Equipment', 'Spaces', 'Systems'];
    var gE = el('g'), gC = el('g');

    labels.forEach(function (label, i) {
      var a = (Math.PI * 2 * i) / labels.length - Math.PI / 2;
      var x = CX + Math.cos(a) * RX, y = CY + Math.sin(a) * RY;
      var d = 'M' + (CX + Math.cos(a) * 70).toFixed(1) + ' ' + (CY + Math.sin(a) * 70).toFixed(1) +
              'Q' + (CX + Math.cos(a) * RX * 0.52).toFixed(1) + ' ' + (CY + Math.sin(a) * RY * 0.86).toFixed(1) +
              ' ' + x.toFixed(1) + ' ' + y.toFixed(1);
      var id = 'aedge-' + i;
      gE.appendChild(el('path', { d: d, class: 'd-link' }));
      gE.appendChild(el('path', { d: d, id: id, class: 'd-link d-link--live', opacity: '.6' }));
      if (!reduce) gE.appendChild(pulse(id, 'm-pulse--mech', 2.8 + (i % 3) * 0.7, i * 0.3, 2.4));

      var w = Math.max(120, label.length * 8 + 34);
      gC.appendChild(el('rect', { x: x - w / 2, y: y - 19, width: w, height: 38, rx: 19, class: 'd-node' }));
      gC.appendChild(el('circle', { cx: x - w / 2 + 16, cy: y, r: 3, fill: 'var(--mech)' }));
      gC.appendChild(el('text', { x: x + 8, y: y + 4.5, class: 'd-t', 'text-anchor': 'middle' }, label));
    });

    var gCore = el('g');
    [104, 86].forEach(function (r) { gCore.appendChild(el('circle', { cx: CX, cy: CY, r: r, class: 'd-ring' })); });
    gCore.appendChild(el('circle', { cx: CX, cy: CY, r: 70, class: 'd-hub' }));
    gCore.appendChild(el('text', { x: CX, y: CY - 4, class: 'd-ht', 'text-anchor': 'middle' }, 'BIMRACE'));
    gCore.appendChild(el('text', { x: CX, y: CY + 18, class: 'd-hs', 'text-anchor': 'middle' }, 'MODEL DATA'));
    if (!reduce) {
      var halo = el('circle', { cx: CX, cy: CY, r: 104, class: 'd-ring', opacity: '.5' });
      halo.appendChild(el('animate', { attributeName: 'r', values: '104;132;104', dur: '5.5s', repeatCount: 'indefinite' }));
      halo.appendChild(el('animate', { attributeName: 'opacity', values: '.5;0;.5', dur: '5.5s', repeatCount: 'indefinite' }));
      gCore.insertBefore(halo, gCore.firstChild);
    }
    svg.appendChild(gE); svg.appendChild(gC); svg.appendChild(gCore);
    if (reduce && svg.pauseAnimations) svg.pauseAnimations();
  }

  /* -------------------------------------------------------- 4. platform map */
  function platformMap() {
    var svg = document.getElementById('platform-svg');
    if (!svg) return;
    var HUB = { x: 450, y: 230, w: 250, h: 82 };
    var nodes = [
      { x: 116, y: 54, t: 'BIM Models', s: 'IFC / RVT' },
      { x: 322, y: 54, t: 'MEP Systems', s: 'M / E / P' },
      { x: 578, y: 54, t: 'Engineering Data', s: 'PARAMETERS' },
      { x: 784, y: 54, t: 'Checking Engine', s: 'RULE SETS' },
      { x: 190, y: 406, t: 'Automation', s: 'WORKFLOWS' },
      { x: 450, y: 406, t: 'Coordination', s: 'CLASH / CLEARANCE' },
      { x: 710, y: 406, t: 'Analytics', s: 'INSIGHTS' }
    ];
    var gL = el('g'), gN = el('g');
    nodes.forEach(function (n, i) {
      var top = n.y < HUB.y;
      var sy = top ? n.y + 27 : n.y - 27;
      var ey = top ? HUB.y - HUB.h / 2 : HUB.y + HUB.h / 2;
      var my = (sy + ey) / 2;
      var d = 'M' + n.x + ' ' + sy + 'C' + n.x + ' ' + my + ' ' + HUB.x + ' ' + my + ' ' + HUB.x + ' ' + ey;
      var id = 'plink-' + i;
      gL.appendChild(el('path', { d: d, class: 'd-link' }));
      gL.appendChild(el('path', { d: d, id: id, class: 'd-link d-link--live', opacity: '.75' }));
      if (!reduce) gL.appendChild(pulse(id, 'm-pulse--mech', 3 + (i % 4) * 0.55, i * 0.42, 2.6));
      gN.appendChild(el('rect', { x: n.x - 92, y: n.y - 27, width: 184, height: 54, rx: 3, class: 'd-node' }));
      gN.appendChild(el('rect', { x: n.x - 92, y: n.y - 27, width: 3, height: 54, class: 'd-bar' }));
      gN.appendChild(el('text', { x: n.x - 76, y: n.y - 3, class: 'd-t' }, n.t));
      gN.appendChild(el('text', { x: n.x - 76, y: n.y + 15, class: 'd-s' }, n.s));
    });
    var gH = el('g');
    gH.appendChild(el('rect', { x: HUB.x - HUB.w / 2 - 10, y: HUB.y - HUB.h / 2 - 10, width: HUB.w + 20, height: HUB.h + 20, rx: 5, class: 'd-ring' }));
    gH.appendChild(el('rect', { x: HUB.x - HUB.w / 2, y: HUB.y - HUB.h / 2, width: HUB.w, height: HUB.h, rx: 4, class: 'd-hub' }));
    gH.appendChild(el('text', { x: HUB.x, y: HUB.y - 4, class: 'd-ht', 'text-anchor': 'middle' }, 'BIMRACE'));
    gH.appendChild(el('text', { x: HUB.x, y: HUB.y + 18, class: 'd-hs', 'text-anchor': 'middle' }, 'INTELLIGENCE LAYER'));
    svg.appendChild(gL); svg.appendChild(gN); svg.appendChild(gH);
    if (reduce && svg.pauseAnimations) svg.pauseAnimations();
  }

  /* --------------------------------------------------------- 5. navigation */
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

    /* Capability dropdown: click on touch/mobile, hover on pointer devices. */
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

  /* ------------------------------------------------ 6. reveal and counters */
  function reveal() {
    if (reduce || !('IntersectionObserver' in window)) return;
    var items = [];
    ['.sec-head', '.pillar', '.std', '.ind', '.spec__row', '.pcard', '.slot',
     '.hero__copy', '.viz', '.pstep', '.dia', '.form', '.phero__in > div'].forEach(function (s) {
      $$(s).forEach(function (n) { if (items.indexOf(n) === -1) items.push(n); });
    });
    items.forEach(function (n) { n.classList.add('reveal'); });
    var io = new IntersectionObserver(function (es, obs) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        var sib = Array.prototype.slice.call(e.target.parentNode.children);
        e.target.style.setProperty('--d', Math.min(sib.indexOf(e.target), 5) * 60 + 'ms');
        e.target.classList.add('is-in');
        obs.unobserve(e.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });
    items.forEach(function (n) { io.observe(n); });

    var proc = document.getElementById('process');
    if (proc) {
      new IntersectionObserver(function (es, obs) {
        es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-drawn'); obs.unobserve(e.target); } });
      }, { threshold: 0.2 }).observe(proc);
    }
  }

  function counters() {
    var cells = $$('[data-count]');
    if (!cells.length) return;
    function run(n) {
      var target = parseInt(n.getAttribute('data-count'), 10) || 0;
      if (reduce) { n.textContent = target.toLocaleString(); return; }
      var t0 = performance.now();
      (function frame(now) {
        var t = Math.min(1, (now - t0) / 1400);
        n.textContent = Math.round(target * (1 - Math.pow(1 - t, 3))).toLocaleString();
        if (t < 1) requestAnimationFrame(frame);
      })(t0);
    }
    if (!('IntersectionObserver' in window)) { cells.forEach(run); return; }
    var io = new IntersectionObserver(function (es, obs) {
      es.forEach(function (e) { if (e.isIntersecting) { run(e.target); obs.unobserve(e.target); } });
    }, { threshold: 0.5 });
    cells.forEach(function (c) { io.observe(c); });
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

  /* -------------------------------------------------- 7. enquiry validation */
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

  /* ------------------------------------------------------------- 8. boot -- */
  function boot() {
    try {
      heroModel(); aiDiagram(); platformMap();
      nav(); reveal(); counters(); portrait(); legalToc(); form();
    } catch (err) {
      if (window.console && console.error) console.error('[BIMRACE]', err);
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();

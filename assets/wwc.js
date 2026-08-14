/* =================================================================
   WEIRD WITH CODE — light interaction layer
   Same filename as before so every page picks it up unchanged.

   Systems:
     preloader   counter 00->100, veil lifts   (add id="uv-veil" markup
                 or let the script inject it on pages with .uv-head)
     trail       mouse-trail images inside [data-trail] using images
                 listed in its data-trail-srcs attribute (JSON array)
     reveals     [data-rise] fade-in on scroll (kept from old system,
                 so all patched project pages keep working)
     drift       [data-drift] gentle scroll parallax on feed media
     peek        [data-peek] hover media following the pointer
     overlay     [data-overlay-open] / [data-overlay-close] toggle
                 the #uv-overlay contact layer
     fadeout     internal links fade the page before navigating

   Legacy attributes from the dark system (data-mag, data-say,
   data-lines) are tolerated: data-lines still splits, the other two
   are inert, so previously patched pages need no edits.
   ================================================================= */

(function () {
  'use strict';

  var RM = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var FINE = window.matchMedia('(pointer: fine)').matches;
  var lerp = function (a, b, n) { return a + (b - a) * n; };

  /* ---------------------------------------------------------------
     Preloader
     Runs only on pages that opt in with <body data-veil>. Counter
     eases to 100 over ~1.1s, veil slides up, then reveals fire.
     --------------------------------------------------------------- */
  function preloader() {
    if (!document.body.hasAttribute('data-veil') || RM) {
      document.documentElement.classList.add('uv-open');
      return;
    }
    // Skip the ceremony on repeat views this session.
    var seen = false;
    try { seen = sessionStorage.getItem('uvSeen') === '1'; } catch (e) {}
    if (seen) { document.documentElement.classList.add('uv-open'); return; }

    var veil = document.createElement('div'); veil.id = 'uv-veil';
    var num = document.createElement('span'); num.id = 'uv-count';
    num.textContent = '00';
    veil.appendChild(num);
    document.body.appendChild(veil);
    document.documentElement.classList.add('uv-loading');

    var t0 = performance.now(), DUR = 1100;
    (function tick(t) {
      var p = Math.min(1, (t - t0) / DUR);
      var eased = 1 - Math.pow(1 - p, 3);
      num.textContent = String(Math.round(eased * 100)).padStart(2, '0');
      if (p < 1) { requestAnimationFrame(tick); return; }
      veil.classList.add('up');
      document.documentElement.classList.remove('uv-loading');
      document.documentElement.classList.add('uv-open');
      try { sessionStorage.setItem('uvSeen', '1'); } catch (e) {}
      setTimeout(function () { veil.remove(); }, 1000);
    })(t0);
  }

  /* ---------------------------------------------------------------
     Mouse-trail images
     Every TRAVEL px of pointer movement inside [data-trail], the
     next image in the cycle appears at the pointer, holds, fades.
     --------------------------------------------------------------- */
  function trail() {
    if (!FINE || RM) return;
    var zone = document.querySelector('[data-trail]');
    if (!zone) return;

    var srcs;
    try { srcs = JSON.parse(zone.getAttribute('data-trail-srcs') || '[]'); }
    catch (e) { srcs = []; }
    if (!srcs.length) return;

    // Warm the first few so the trail never shows a loading blank.
    srcs.slice(0, 6).forEach(function (s) { var i = new Image(); i.src = s; });

    var TRAVEL = 130, MAX = 7;
    var lx = null, ly = null, idx = 0, live = [];

    zone.addEventListener('mousemove', function (e) {
      if (lx === null) { lx = e.clientX; ly = e.clientY; return; }
      var d = Math.hypot(e.clientX - lx, e.clientY - ly);
      if (d < TRAVEL) return;
      lx = e.clientX; ly = e.clientY;

      var img = document.createElement('img');
      img.className = 'uv-trail-img';
      img.alt = '';
      img.src = srcs[idx % srcs.length];
      idx++;
      img.style.left = e.clientX + 'px';
      img.style.top = e.clientY + 'px';
      document.body.appendChild(img);
      live.push(img);

      requestAnimationFrame(function () { img.classList.add('live'); });
      setTimeout(function () { img.classList.add('gone'); }, 650);
      setTimeout(function () {
        img.remove(); live = live.filter(function (n) { return n !== img; });
      }, 1450);

      if (live.length > MAX) {
        var old = live.shift();
        old.classList.add('gone');
        setTimeout(function () { old.remove(); }, 700);
      }
      // Warm the next one in the cycle.
      var pre = new Image(); pre.src = srcs[idx % srcs.length];
    }, { passive: true });

    zone.addEventListener('mouseleave', function () { lx = ly = null; });
  }

  /* ---------------------------------------------------------------
     Reveals (unchanged API: data-rise, data-rise-group, data-lines)
     --------------------------------------------------------------- */
  function reveals() {
    document.querySelectorAll('[data-lines]').forEach(function (el) {
      var parts = el.innerHTML.split(/<br\s*\/?>/i);
      el.classList.add('wc-lines');
      el.innerHTML = parts.map(function (p, i) {
        return '<span class="wc-line"><i style="--d:' + (i * 95) + 'ms">' + p.trim() + '</i></span>';
      }).join('');
    });

    document.querySelectorAll('[data-rise-group]').forEach(function (g) {
      var step = parseInt(g.getAttribute('data-rise-group'), 10) || 80;
      Array.prototype.forEach.call(g.children, function (c, i) {
        if (!c.hasAttribute('data-rise')) c.setAttribute('data-rise', '');
        c.style.setProperty('--d', (i * step) + 'ms');
      });
    });

    var targets = document.querySelectorAll('[data-rise],[data-lines]');
    if (RM || !('IntersectionObserver' in window)) {
      targets.forEach(function (el) { el.classList.add('wc-in'); });
      return;
    }
    var io = new IntersectionObserver(function (rows) {
      rows.forEach(function (r) {
        if (!r.isIntersecting) return;
        r.target.classList.add('wc-in');
        io.unobserve(r.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.1 });
    targets.forEach(function (el) { io.observe(el); });
  }

  /* ---------------------------------------------------------------
     Scroll drift — media inside [data-drift] slides slightly against
     scroll direction. rAF-throttled, no work when nothing moved.
     --------------------------------------------------------------- */
  function drift() {
    if (RM) return;
    var items = Array.prototype.slice.call(document.querySelectorAll('[data-drift] img'));
    if (!items.length) return;

    var ticking = false;
    function apply() {
      ticking = false;
      var vh = window.innerHeight;
      items.forEach(function (img) {
        var r = img.parentElement.getBoundingClientRect();
        if (r.bottom < 0 || r.top > vh) return;
        var p = (r.top + r.height / 2 - vh / 2) / vh; // -0.5 .. 0.5
        img.style.transform = 'translate3d(0,' + (p * -5).toFixed(2) + '%,0)';
      });
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(apply); }
    }, { passive: true });
    apply();
  }

  /* ---------------------------------------------------------------
     Hover peek (works index)
     --------------------------------------------------------------- */
  function peek() {
    if (!FINE || RM) return;
    if (!document.querySelector('[data-peek]')) return;

    var box = document.createElement('div'); box.id = 'wc-peek';
    var img = document.createElement('img'); img.alt = ''; img.decoding = 'async';
    box.appendChild(img);
    document.body.appendChild(box);

    var mx = 0, my = 0, cx = 0, cy = 0;
    addEventListener('mousemove', function (e) { mx = e.clientX; my = e.clientY; }, { passive: true });

    (function tick() {
      cx = lerp(cx, mx, 0.12); cy = lerp(cy, my, 0.12);
      box.style.transform = 'translate3d(' + (cx + 22).toFixed(1) + 'px,' +
        (cy - box.offsetHeight / 2).toFixed(1) + 'px,0)';
      requestAnimationFrame(tick);
    })();

    // Delegated, so rows created after boot (e.g. filter re-renders)
    // work without any rebinding.
    document.addEventListener('mouseover', function (e) {
      var row = e.target.closest && e.target.closest('[data-peek]');
      if (!row) return;
      img.src = row.getAttribute('data-peek');
      box.classList.add('on');
    });
    document.addEventListener('mouseout', function (e) {
      var row = e.target.closest && e.target.closest('[data-peek]');
      if (!row) return;
      if (e.relatedTarget && e.relatedTarget.closest &&
          e.relatedTarget.closest('[data-peek]') === row) return;
      box.classList.remove('on');
    });

    // Pre-warm sources present at boot.
    document.querySelectorAll('[data-peek]').forEach(function (row) {
      var warm = new Image(); warm.src = row.getAttribute('data-peek');
    });
  }

  /* ---------------------------------------------------------------
     Contact overlay
     --------------------------------------------------------------- */
  function overlay() {
    var ov = document.getElementById('uv-overlay');
    if (!ov) return;
    var lastFocus = null;

    function open() {
      lastFocus = document.activeElement;
      ov.classList.add('open');
      document.body.classList.add('uv-contact');
      ov.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
      var c = ov.querySelector('.uv-ov-close');
      if (c) c.focus();
    }
    function close() {
      ov.classList.remove('open');
      document.body.classList.remove('uv-contact');
      ov.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    }

    document.addEventListener('click', function (e) {
      if (e.target.closest('[data-overlay-open]')) { e.preventDefault(); open(); }
      if (e.target.closest('[data-overlay-close]')) { e.preventDefault(); close(); }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && ov.classList.contains('open')) close();
    });
  }

  /* ---------------------------------------------------------------
     Page fade transitions on internal navigation
     --------------------------------------------------------------- */
  function fadeout() {
    if (RM) return;
    document.body.style.transition = 'opacity .45s ease';
    document.addEventListener('click', function (e) {
      var a = e.target.closest('a[href]');
      if (!a) return;
      var href = a.getAttribute('href');
      if (!href || href.charAt(0) === '#' ||
          a.target === '_blank' ||
          /^(https?:|mailto:|tel:)/.test(href) ||
          a.hasAttribute('data-overlay-open')) return;
      e.preventDefault();
      document.body.style.opacity = '0';
      setTimeout(function () { location.href = href; }, 380);
    });
    // Restore when arriving via back/forward cache.
    window.addEventListener('pageshow', function () {
      document.body.style.opacity = '1';
    });
  }

  /* --------------------------------------------------------------- */
  function boot() {
    preloader(); trail(); reveals(); drift(); peek(); overlay(); fadeout();
    document.documentElement.classList.add('wc-ready');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else { boot(); }
})();

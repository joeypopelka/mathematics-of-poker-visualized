/* Shared site navigation + theme switch — injected on every page.
   Meisterhaus structure: one compact header row (title left, tabs right)
   over a strong rule, plus a fixed left rail carrying the family shapes
   as wayfinding. No bands, no ornament.
   Sets html[data-theme] (persisted) and html[data-family] (section color). */
(function () {
  'use strict';

  var script = document.currentScript;
  var root = script.src.replace(/nav\.js(\?.*)?$/, '');

  // first path segment under the repo root → which tab / family is active
  var SECTION_TAB = {
    'zero-one': 'zo',
    'akq': 'akq',
    'jam-or-fold': 'more',
    'multi-street': 'more',
    'risk': 'more',
    'tournaments': 'more',
    'multiway': 'more'
  };

  function activeKey() {
    var rel = location.href.indexOf(root) === 0 ? location.href.slice(root.length) : '';
    var seg = rel.split(/[\/?#]/)[0];
    if (SECTION_TAB[seg]) return SECTION_TAB[seg];
    return location.hash === '#about' ? 'about' : 'home';
  }

  /* ---- theme ---- */
  function storedTheme() { try { return localStorage.getItem('mop-theme'); } catch (e) { return null; } }
  function osDark() { return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches; }
  function currentDark() {
    var t = document.documentElement.getAttribute('data-theme');
    if (t) return t === 'dark';
    return osDark();
  }
  var saved = storedTheme();
  if (saved === 'dark' || saved === 'light') {
    document.documentElement.setAttribute('data-theme', saved);
  }

  var css = [
    '.mnav-header{display:block;margin:0;padding:0;border:0;max-width:none;width:auto;text-align:left;',
      'background:var(--bg);border-bottom:1px solid var(--strong);',
      'font-family:var(--sans);line-height:1.5}',
    '.mnav-header *{box-sizing:border-box}',
    '.mnav-bar{max-width:1100px;margin:0 auto;padding:0 1.4rem;display:flex;align-items:center;gap:1.2rem;min-height:3.1rem;flex-wrap:wrap}',
    '.mnav-title{font-size:.78rem;font-weight:700;letter-spacing:.3em;text-transform:uppercase;color:var(--ink);text-decoration:none;white-space:nowrap}',
    '.mnav-title:hover{text-decoration:none;color:var(--ink)}',
    '.mnav-tabs{display:flex;flex-wrap:wrap;gap:.1rem;align-items:center;margin-left:auto}',
    '.mnav-tab{position:relative}',
    '.mnav-tab>button,.mnav-tab>a{display:block;margin:0;background:none;border:none;border-radius:0;box-shadow:none;cursor:pointer;',
      'font-family:var(--sans);font-size:.6rem;font-weight:500;letter-spacing:.26em;text-transform:uppercase;',
      'color:var(--dim);padding:1.05rem .7rem .95rem;border-bottom:2px solid transparent;text-decoration:none}',
    '.mnav-tab>button:hover,.mnav-tab>a:hover{color:var(--ink);text-decoration:none}',
    '.mnav-tab.mnav-active>a,.mnav-tab.mnav-active>button{color:var(--ink);border-bottom-color:var(--fam)}',
    '.mnav-tab>button .mnav-caret{font-size:.8em;color:var(--faint);margin-left:.3em}',
    '.mnav-tab.mnav-open>button{color:var(--ink)}',
    '.mnav-menu{display:none;position:absolute;right:0;top:100%;z-index:1000;min-width:17rem;',
      'background:var(--panel);border:1px solid var(--strong);padding:.3rem 0;text-align:left}',
    '.mnav-tab.mnav-open .mnav-menu{display:block}',
    '.mnav-menu a{display:block;padding:.5rem 1rem;color:var(--ink);font-size:.78rem;font-weight:500;',
      'letter-spacing:.06em;text-decoration:none}',
    '.mnav-menu a:hover{background:var(--panel2);color:var(--ink);text-decoration:none}',
    '.mnav-menu a .mnav-sub{display:block;font-family:var(--mono);font-size:.62rem;font-weight:400;',
      'letter-spacing:.04em;color:var(--dim);margin-top:.1rem}',
    '.mnav-mode{display:flex;align-items:center;gap:.45rem;background:none;border:1px solid var(--strong);',
      'cursor:pointer;color:var(--ink);font-family:var(--sans);font-size:.54rem;font-weight:700;',
      'letter-spacing:.24em;text-transform:uppercase;padding:.4rem .65rem;border-radius:0;margin-left:.6rem}',
    '.mnav-mode:hover{background:var(--panel2)}',
    '.mnav-mode:focus-visible{outline:2px solid var(--blue);outline-offset:2px}',
    '.mnav-mode i{display:block;width:.55rem;height:.55rem;background:var(--ink)}',
    'html[data-theme="dark"] .mnav-mode i{border-radius:50%}',
    '@media (prefers-color-scheme: dark){html:not([data-theme="light"]) .mnav-mode i{border-radius:50%}}',
    /* the wayfinding rail: family shapes down the left edge */
    '.mnav-rail{position:fixed;left:0;top:0;bottom:0;width:2.2rem;z-index:900;',
      'background:var(--bg);border-right:1px solid var(--hair);',
      'display:flex;flex-direction:column;align-items:center;padding-top:1rem;gap:.85rem}',
    '.mnav-rail i{display:block;width:1rem;height:1rem;border-radius:50%;',
      'background:radial-gradient(circle at 50% 50%, var(--c) 0 52%, transparent 53% 86%, var(--c) 87%),',
      'repeating-conic-gradient(from -6deg, #fff 0 12deg, transparent 12deg 45deg),',
      'var(--c)}',
    '.mnav-rail .mnav-gs{--c:var(--blue)}',
    '.mnav-rail .mnav-gc{--c:var(--red)}',
    '.mnav-rail .mnav-gt{--c:var(--yellow)}',
    '@media (max-width:1259px){.mnav-rail{display:none}}'
  ].join('\n');

  function item(href, label, sub) {
    return '<a href="' + root + href + '">' + label +
           ' <span class="mnav-sub">' + sub + '</span></a>';
  }

  var html =
    '<div class="mnav-bar">' +
      '<a class="mnav-title" href="' + root + '">MoP · Visualized</a>' +
      '<nav class="mnav-tabs" aria-label="Site">' +
        '<div class="mnav-tab" data-key="home"><a href="' + root + '#home">Home</a></div>' +
        '<div class="mnav-tab" data-key="zo"><button type="button" aria-haspopup="true" aria-expanded="false">[0,1] Games <span class="mnav-caret">▾</span></button><div class="mnav-menu">' +
          item('zero-one/', 'Overview', 'the [0,1] family, ch. 11 &amp; 16–18') +
          item('zero-one/game2.html', 'Game #2', "von Neumann's half-street game") +
          item('zero-one/game9.html', 'Game #9', 'live Figure 17.1') +
          item('zero-one/game10.html', 'Game #10', 'live Figure 17.2') +
          item('zero-one/game11.html', 'Game #11', 'the check-raise game') +
          item('zero-one/game12.html', 'Game #12', 'the infinite raising ladder') +
        '</div></div>' +
        '<div class="mnav-tab" data-key="akq"><button type="button" aria-haspopup="true" aria-expanded="false">AKQ Games <span class="mnav-caret">▾</span></button><div class="mnav-menu">' +
          item('akq/limit/', 'Limit', 'ch. 13 — the gateway game') +
          item('akq/nl/', 'No-Limit', 'ch. 15 + appendix') +
        '</div></div>' +
        '<div class="mnav-tab" data-key="more"><button type="button" aria-haspopup="true" aria-expanded="false">Additional Topics <span class="mnav-caret">▾</span></button><div class="mnav-menu">' +
          item('jam-or-fold/', 'Jam-or-Fold', 'ch. 12 — preflop NLHE, solved exactly') +
          item('multi-street/', 'Multi-Street Games', 'ch. 14 + 19 — geometric growth of pot') +
          item('risk/', 'Risk', 'ch. 22–25 — ruin, Kelly, backing') +
          item('tournaments/', 'Tournaments', 'ch. 26–28 — ICM, bubble factors') +
          item('multiway/', 'Multiplayer Games', 'ch. 29 — alliances and equilibria') +
        '</div></div>' +
        '<div class="mnav-tab" data-key="about"><a href="' + root + '#about">About</a></div>' +
        '<button type="button" class="mnav-mode" aria-label="Switch color theme"><i></i><span class="mnav-mode-label"></span></button>' +
      '</nav>' +
    '</div>';

  var RAIL_SHAPES = {
    zo: '<i class="mnav-gs"></i>',
    akq: '<i class="mnav-gc"></i>',
    more: '<i class="mnav-gt"></i>'
  };

  function build() {
    var style = document.createElement('style');
    style.textContent = css;
    document.head.appendChild(style);

    var header = document.createElement('div');
    header.className = 'mnav-header';
    header.innerHTML = html;
    document.body.insertBefore(header, document.body.firstChild);

    var rail = document.createElement('div');
    rail.className = 'mnav-rail';
    rail.setAttribute('aria-hidden', 'true');
    document.body.appendChild(rail);

    var tabs = Array.prototype.slice.call(header.querySelectorAll('.mnav-tab'));

    function closeMenus(except) {
      tabs.forEach(function (t) {
        var btn = t.querySelector('button');
        if (btn && t !== except) {
          t.classList.remove('mnav-open');
          btn.setAttribute('aria-expanded', 'false');
        }
      });
    }

    tabs.forEach(function (t) {
      var btn = t.querySelector('button');
      if (btn) {
        btn.addEventListener('click', function (e) {
          e.stopPropagation();
          var open = t.classList.toggle('mnav-open');
          btn.setAttribute('aria-expanded', String(open));
          closeMenus(t);
        });
      }
    });

    document.addEventListener('click', function () { closeMenus(null); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeMenus(null);
    });

    function markActive() {
      var key = activeKey();
      tabs.forEach(function (t) {
        t.classList.toggle('mnav-active', t.getAttribute('data-key') === key);
      });
      if (RAIL_SHAPES[key]) {
        document.documentElement.setAttribute('data-family', key);
        rail.innerHTML = RAIL_SHAPES[key];
      } else {
        document.documentElement.removeAttribute('data-family');
        rail.innerHTML = RAIL_SHAPES.zo + RAIL_SHAPES.akq + RAIL_SHAPES.more;
      }
    }
    window.addEventListener('hashchange', markActive);
    markActive();

    /* theme switch */
    var modeBtn = header.querySelector('.mnav-mode');
    var modeLabel = header.querySelector('.mnav-mode-label');
    function syncLabel() { modeLabel.textContent = currentDark() ? 'Light' : 'Dark'; }
    modeBtn.addEventListener('click', function () {
      var next = currentDark() ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      try { localStorage.setItem('mop-theme', next); } catch (e) {}
      syncLabel();
      window.dispatchEvent(new CustomEvent('mop-theme-change', { detail: { theme: next } }));
    });
    syncLabel();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', build);
  } else {
    build();
  }
})();

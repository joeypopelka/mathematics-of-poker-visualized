/* Shared site navigation — injected on every page.
   Include with: <script defer src="PATH/TO/nav.js"></script>
   The repo root is inferred from this script's own src, so it works at any
   depth, locally and on GitHub Pages. */
(function () {
  'use strict';

  var script = document.currentScript;
  var root = script.src.replace(/nav\.js(\?.*)?$/, '');

  // first path segment under the repo root → which tab is active
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

  /* Every rule is explicit (margins, padding, fonts) so page CSS for bare
     elements (header, button, a, nav) can't leak into the injected bar. */
  var css = [
    '.mnav-header{display:block;margin:0;padding:0;border:0;border-bottom:1px solid #232B3A;max-width:none;width:auto;background:#10141D;font-family:Charter,Georgia,"Times New Roman",serif;line-height:1.55;text-align:left}',
    '.mnav-header *{box-sizing:border-box}',
    '.mnav-mast{max-width:1100px;margin:0 auto;padding:1.1rem 1.4rem .6rem}',
    '.mnav-mast a:hover{text-decoration:none;color:#E8E4DC}',
    '.mnav-mast a{font-size:1.25rem;font-weight:600;letter-spacing:-.01em;color:#E8E4DC;text-decoration:none}',
    '.mnav-mast a i{color:#F0A44E}',
    '.mnav-tabs{max-width:1100px;margin:0 auto;padding:0 1.4rem;display:flex;flex-wrap:wrap;gap:.2rem}',
    '.mnav-tab{position:relative}',
    '.mnav-tab>button,.mnav-tab>a{display:block;margin:0;background:none;border:none;border-radius:0;box-shadow:none;text-transform:none;letter-spacing:normal;cursor:pointer;font:600 .95rem Charter,Georgia,serif;color:#8B93A3;padding:.6rem .9rem;border-bottom:2px solid transparent;text-decoration:none}',
    '.mnav-tab>button:hover,.mnav-tab>a:hover{color:#E8E4DC;text-decoration:none}',
    '.mnav-tab.mnav-active>a,.mnav-tab.mnav-active>button{color:#F0A44E;border-bottom-color:#F0A44E}',
    '.mnav-tab>button .mnav-caret{font-size:.7em;color:#5A6274;margin-left:.3em}',
    '.mnav-tab.mnav-open>button{color:#E8E4DC}',
    '.mnav-menu{display:none;position:absolute;left:0;top:100%;z-index:1000;min-width:16rem;background:#151B27;border:1px solid #232B3A;border-radius:0 0 10px 10px;padding:.35rem 0;box-shadow:0 10px 24px rgba(0,0,0,.45)}',
    '.mnav-tab.mnav-open .mnav-menu{display:block}',
    '.mnav-menu a{display:block;padding:.45rem .95rem;color:#E8E4DC;font-size:.92rem;text-decoration:none}',
    '.mnav-menu a:hover{background:#10141D;color:#F0A44E}',
    '.mnav-menu a .mnav-sub{display:block;font-size:.78rem;color:#5A6274}'
  ].join('\n');

  function item(href, label, sub) {
    return '<a href="' + root + href + '">' + label +
           ' <span class="mnav-sub">' + sub + '</span></a>';
  }

  var html =
    '<div class="mnav-mast"><a href="' + root + '">Mathematics of Poker, <i>Visualized</i></a></div>' +
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
    '</nav>';

  function build() {
    var style = document.createElement('style');
    style.textContent = css;
    document.head.appendChild(style);

    var header = document.createElement('div');
    header.className = 'mnav-header';
    header.innerHTML = html;
    document.body.insertBefore(header, document.body.firstChild);

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
    }
    window.addEventListener('hashchange', markActive);
    markActive();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', build);
  } else {
    build();
  }
})();

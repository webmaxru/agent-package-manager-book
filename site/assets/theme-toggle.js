/* Shared light/dark theme toggle.
 *
 * Contract (kept identical across every page + the anti-FOUC head snippet):
 *   - Preference is stored in localStorage under "apm-theme" as "light"|"dark".
 *   - An explicit choice is reflected as data-theme on <html>; with no stored
 *     choice the attribute is absent and CSS falls back to the OS preference
 *     via @media (prefers-color-scheme: dark).
 *   - Any <button data-theme-toggle> on the page flips and persists the choice.
 */
(function () {
  var STORAGE_KEY = 'apm-theme';
  var COLORS = { light: '#F6F7FB', dark: '#10141F' };
  var root = document.documentElement;
  var mql = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;

  function storedChoice() {
    try {
      var value = localStorage.getItem(STORAGE_KEY);
      return value === 'light' || value === 'dark' ? value : null;
    } catch (_error) {
      return null;
    }
  }

  function systemTheme() {
    return mql && mql.matches ? 'dark' : 'light';
  }

  function effectiveTheme() {
    return storedChoice() || systemTheme();
  }

  function apply(choice) {
    // Only set the attribute for an explicit choice; removing it hands control
    // back to the system-preference media query.
    if (choice === 'light' || choice === 'dark') {
      root.setAttribute('data-theme', choice);
    } else {
      root.removeAttribute('data-theme');
    }
  }

  function syncThemeColorMeta(active) {
    // A media-less theme-color meta always matches, so it overrides the two
    // media-scoped tags in markup and tracks a forced theme in the browser UI.
    var meta = document.querySelector('meta[name="theme-color"]:not([media])');
    if (!meta) {
      meta = document.createElement('meta');
      meta.setAttribute('name', 'theme-color');
      document.head.appendChild(meta);
    }
    meta.setAttribute('content', COLORS[active] || COLORS.light);
  }

  function sync() {
    var active = effectiveTheme();
    var next = active === 'dark' ? 'light' : 'dark';
    var label = 'Switch to ' + next + ' theme';
    var buttons = document.querySelectorAll('[data-theme-toggle]');
    for (var i = 0; i < buttons.length; i++) {
      var button = buttons[i];
      button.dataset.active = active;
      button.setAttribute('aria-pressed', String(active === 'dark'));
      button.setAttribute('aria-label', label);
      button.setAttribute('title', label);
    }
    syncThemeColorMeta(active);
  }

  // Re-assert any stored choice (covers pages without the inline head snippet)
  // and paint the initial button state.
  apply(storedChoice());
  sync();

  var toggles = document.querySelectorAll('[data-theme-toggle]');
  for (var j = 0; j < toggles.length; j++) {
    toggles[j].addEventListener('click', function () {
      var next = effectiveTheme() === 'dark' ? 'light' : 'dark';
      try {
        localStorage.setItem(STORAGE_KEY, next);
      } catch (_error) {
        /* storage may be unavailable (private mode); still apply for this view */
      }
      apply(next);
      sync();
    });
  }

  if (mql) {
    var onSystemChange = function () {
      // Only follow the OS while the visitor has made no explicit choice.
      if (!storedChoice()) sync();
    };
    if (mql.addEventListener) mql.addEventListener('change', onSystemChange);
    else if (mql.addListener) mql.addListener(onSystemChange);
  }
})();

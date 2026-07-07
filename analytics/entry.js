/**
 * Cookieless Application Insights RUM for the APM book — beacon transport.
 *
 * Source for the committed bundle `site/assets/analytics.js`. Rebuild after
 * editing with:  npm run build:analytics  (esbuild → IIFE).
 *
 * Loaded on every page *after* `site/assets/analytics-config.js`, which
 * `site/generate.py` writes at build time with the Application Insights
 * connection string (a public, write-only client key) and the `enabled` kill
 * switch. Cookieless by construction: the beacon sets no cookies and no
 * local/session storage and keeps only an in-memory, per-page-load session id —
 * so no cookie/GDPR consent banner is required.
 */
import { init, trackEvent, trackChangeDebounced } from '@webmaxru/cookieless-insights';

// Build-time config injected by generate.py (safe empty object if absent).
const cfg = (typeof window !== 'undefined' && window.__APM_ANALYTICS__) || {};

// One in-memory client per page load. The beacon posts via navigator.sendBeacon
// and auto-flushes on pagehide/visibilitychange, so navigation events survive
// unload. `enabled` is the master kill switch: build-time via the one-line
// ANALYTICS_ENABLED flag in site/generate.py, or at runtime via
// `getClient()?.setEnabled(false)`. A missing connection string is a safe no-op.
const analytics = init({
  connectionString: cfg.connectionString,
  enabled: cfg.enabled !== false,
  cloudRole: 'apm-book',
  autoPageView: true, // sends the page view on init
});

if (analytics.enabled) {
  wireInteractions();
}

/** Stable, human-readable page label used as an event property. */
function pageId() {
  const path = location.pathname.replace(/\/+$/, '');
  const file = path.split('/').pop() || 'index.html';
  if (path.includes('/chapters/')) return 'chapter:' + file.replace(/\.html$/, '');
  if (file === '' || file === 'index.html') return 'home';
  return file.replace(/\.html$/, '');
}

/** Highlight.js language of a <code> block, if any (e.g. "yaml", "bash"). */
function langOf(codeEl) {
  if (!codeEl) return '';
  const match = /(?:language|lang)-([\w-]+)/.exec(codeEl.className || '');
  return match ? match[1] : '';
}

function wireInteractions() {
  const page = pageId();

  // "Opened via a shared/deep link" — landed on a section anchor, or arrived
  // from another site. Fires once per load, alongside the automatic page view.
  let externalReferrer = false;
  try {
    externalReferrer = !!document.referrer && new URL(document.referrer).host !== location.host;
  } catch (_e) {
    externalReferrer = false;
  }
  if (location.hash || externalReferrer) {
    trackEvent('Opened Via Shared Link', {
      page,
      anchor: location.hash || '',
      external_referrer: externalReferrer,
    });
  }

  // A single delegated click handler covers every current and future control on
  // the statically-rendered chapters, the home page, and the orchestration page.
  // Bubble phase: element-level handlers in app.js run first, so aria-expanded is
  // already toggled when we read it; the event is still enqueued before the
  // browser's default navigation, and pagehide flushes the beacon on unload.
  document.addEventListener('click', (event) => {
    const target = event.target;
    if (!(target instanceof Element)) return;

    // Copy-code button (created dynamically by app.js).
    const copyBtn = target.closest('.copy-code');
    if (copyBtn) {
      const codeBlock = copyBtn.closest('.code-block');
      const code = codeBlock ? codeBlock.querySelector('pre > code') : null;
      trackEvent('Code Copied', { page, language: langOf(code) });
      return;
    }

    // Mobile chapter-sidebar toggle.
    const toggle = target.closest('.sidebar-toggle');
    if (toggle) {
      trackEvent('Sidebar Toggled', { page, open: toggle.getAttribute('aria-expanded') === 'true' });
      return;
    }

    // Orchestration wireframe controls.
    if (target.closest('#run')) {
      trackEvent('Orchestration Run', { page });
      return;
    }
    if (target.closest('#reset')) {
      trackEvent('Orchestration Reset', { page });
      return;
    }

    // Links: in-page anchor, outbound (external host), or internal navigation.
    const link = target.closest('a[href]');
    if (link) {
      const href = link.getAttribute('href') || '';
      if (href.startsWith('#')) {
        trackEvent('Anchor Navigated', { page, to: href });
        return;
      }
      let url;
      try {
        url = new URL(link.href, location.href);
      } catch (_e) {
        return;
      }
      if (url.host !== location.host) {
        trackEvent('Outbound Click', { page, host: url.host, href: url.href });
      } else if (url.pathname !== location.pathname) {
        trackEvent('Internal Nav', { page, to: url.pathname });
      }
    }
  });

  // Sliders, text inputs, selects, contenteditable — collapse a burst of changes
  // (drags/typing) into one event once activity settles (700ms default).
  document.addEventListener('input', (event) => {
    const el = event.target;
    if (!(el instanceof Element)) return;
    if (!el.matches('input, textarea, select, [role="slider"], [contenteditable]')) return;
    const key =
      el.id || el.getAttribute('name') || el.getAttribute('aria-label') || el.tagName.toLowerCase();
    trackChangeDebounced('Input Changed', String(key));
  });
}

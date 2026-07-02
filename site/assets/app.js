(function () {
  const sidebar = document.querySelector('#chapter-sidebar');
  const toggle = document.querySelector('.sidebar-toggle');

  if (sidebar && toggle) {
    toggle.addEventListener('click', () => {
      const isOpen = sidebar.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', String(isOpen));
    });

    sidebar.addEventListener('click', (event) => {
      if (event.target.closest('a') && sidebar.classList.contains('is-open')) {
        sidebar.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  document.querySelectorAll('pre > code').forEach((codeBlock) => {
    const pre = codeBlock.parentElement;
    if (!pre || pre.parentElement.classList.contains('code-block')) return;
    if (pre.closest('.manifest-artifact')) return;

    const wrapper = document.createElement('div');
    wrapper.className = 'code-block';
    pre.parentNode.insertBefore(wrapper, pre);
    wrapper.appendChild(pre);

    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'copy-code';
    button.textContent = 'Copy';
    button.setAttribute('aria-label', 'Copy code block');
    wrapper.appendChild(button);

    button.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(codeBlock.textContent);
        button.textContent = 'Copied';
        window.setTimeout(() => { button.textContent = 'Copy'; }, 1600);
      } catch (_error) {
        button.textContent = 'Copy failed';
        window.setTimeout(() => { button.textContent = 'Copy'; }, 1600);
      }
    });
  });

  document.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener('click', (event) => {
      const id = link.getAttribute('href').slice(1);
      if (!id) return;
      const target = document.getElementById(decodeURIComponent(id));
      if (!target) return;
      event.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      history.pushState(null, '', `#${id}`);
      target.setAttribute('tabindex', '-1');
      target.focus({ preventScroll: true });
    });
  });

  if (window.hljs) {
    window.hljs.configure({ languages: ['yaml', 'bash', 'shell', 'json', 'text', 'plaintext', 'python'] });
    window.hljs.highlightAll();
  }

  // Index hero: reveal the manifest artifact's lines as if "resolving".
  // The hidden/animated state lives behind @media (prefers-reduced-motion:
  // no-preference) in CSS; adding the class only when motion is welcome keeps
  // reduced-motion users (and no-JS) on the fully visible default.
  const artifact = document.querySelector('.manifest-artifact');
  if (
    artifact &&
    window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: no-preference)').matches
  ) {
    artifact.classList.add('reveal-on');
  }
})();

// The Cite panel: switch between BibTeX, RIS, CSL-JSON and EndNote, and copy the one
// on screen. Every record is plain <pre> text in the page, so without this script the
// panel still shows BibTeX and can be selected by hand.
// dataset['fmt'], never dataset.fmt: the group site compiles this with Closure at
// -O ADVANCED, which renames a dotted custom property. It renamed fmt to g, so every
// read came back undefined, every tab matched and nothing hid. citations.js uses
// dataset['doi'] for the same reason.
(() => {
  for (const panel of document.querySelectorAll('details.cite .cite-body')) {
    const tabs = [...panel.querySelectorAll('.cite-tab')];
    const texts = [...panel.querySelectorAll('.cite-text')];
    if (!tabs.length || !texts.length) continue;

    const show = (fmt) => {
      for (const t of tabs) t.classList.toggle('is-on', t.dataset['fmt'] === fmt);
      for (const p of texts) p.hidden = p.dataset['fmt'] !== fmt;
    };
    // The tabs are a radio group: one format is always the visible one. Clicking the
    // format that is ALREADY showing closes the panel instead, so a second click on
    // the same button undoes the first, which is what it looks like it should do.
    for (const tab of tabs) {
      tab.addEventListener('click', () => {
        const details = panel.closest('details');
        if (tab.classList.contains('is-on') && details) {
          details.open = false;
          return;
        }
        show(tab.dataset['fmt']);
      });
    }

    if (!navigator.clipboard) continue;
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'cite-copy';
    button.textContent = 'Copy';
    button.addEventListener('click', () => {
      const shown = texts.find((p) => !p.hidden);
      if (!shown) return;
      navigator.clipboard.writeText(shown.textContent).then(() => {
        button.textContent = 'Copied';
        setTimeout(() => { button.textContent = 'Copy'; }, 1500);
      }).catch(() => {});
    });
    panel.querySelector('.cite-tabs').appendChild(button);
  }
})();

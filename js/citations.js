// Citation counts from OpenAlex, filled in after the page loads and shown
// only when a count comes back. Nothing is displayed while the request is
// in flight or if it fails, so the page never depends on the service.
// Same logic as citations.js on entropy4energy.ai.
(() => {
  const spans = [...document.querySelectorAll('.cites[data-doi]')];
  if (!spans.length || !window.fetch) return;
  const byDoi = new Map(spans.map((el) => [el.dataset.doi.toLowerCase(), el]));
  const dois = [...byDoi.keys()];
  // OpenAlex sometimes holds two records for one DOI (a preprint duplicate);
  // keep the larger count.
  const best = new Map();
  const show = (doi, count) => {
    const el = byDoi.get(doi);
    if (!el || !(count > 0) || (best.get(doi) || 0) >= count) return;
    best.set(doi, count);
    el.textContent = count === 1 ? '1 citation' : `${count.toLocaleString()} citations`;
    el.title = 'Citation count from OpenAlex';
    el.hidden = false;
  };
  const batch = 40;
  for (let i = 0; i < dois.length; i += batch) {
    const chunk = dois.slice(i, i + batch);
    const url = 'https://api.openalex.org/works?per-page=' + chunk.length
      + '&select=doi,cited_by_count&filter=doi:' + chunk.map(encodeURIComponent).join('|');
    // Give up after 8 s: a slow or unreachable service must never hold anything up.
    const ctl = ('AbortController' in window) ? new AbortController() : null;
    if (ctl) setTimeout(() => ctl.abort(), 8000);
    fetch(url, ctl ? { signal: ctl.signal } : {}).then((r) => (r.ok ? r.json() : null)).then((data) => {
      if (!data || !data.results) return;
      for (const work of data.results) {
        if (!work.doi) continue;
        show(work.doi.replace(/^https?:\/\/doi\.org\//i, '').toLowerCase(), work.cited_by_count);
      }
    }).catch(() => {});
  }
})();

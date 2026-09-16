/* coreyoses.com: the CV sections are <details>; the long ones ship closed.
   This keeps the page behaving like a flat document anyway: deep links and the
   section nav open the section they point at, the nav carries an expand-all
   toggle, and printing opens everything first. Current Chrome and Safari also
   open a closed section by themselves when find-in-page hits text inside it. */
(function () {
  "use strict";

  var SECTIONS = "details.cv-section";

  function all() {
    return Array.prototype.slice.call(document.querySelectorAll(SECTIONS));
  }

  /* ids hold a colon (sec:journal-publications), which querySelector reads as a
     pseudo-class, so the lookup goes through getElementById */
  function targetOf(hash) {
    if (!hash || hash.charAt(0) !== "#") return null;
    var id = decodeURIComponent(hash.slice(1));
    return document.getElementById(id);
  }

  function reveal(hash, scroll) {
    var el = targetOf(hash);
    if (!el) return false;
    var box = el.closest("details");
    while (box) {
      box.open = true;
      box = box.parentElement ? box.parentElement.closest("details") : null;
    }
    if (scroll) el.scrollIntoView();
    syncToggle();
    return true;
  }

  /* The section bar is sticky and wraps to two or three rows on narrow screens,
     so headings need a scroll margin that follows its real height. It is watched
     rather than measured once: the bar grows a row when the web font swaps in. */
  function watchNav() {
    var nav = document.querySelector(".secnav");
    if (!nav) return;
    var measure = function () {
      document.documentElement.style.setProperty(
        "--secnav-h", Math.round(nav.getBoundingClientRect().height) + "px");
    };
    measure();
    if (window.ResizeObserver) {
      new ResizeObserver(measure).observe(nav);
    } else {
      window.addEventListener("resize", measure);
      window.addEventListener("load", measure);
    }
  }

  var toggle = null;

  function syncToggle() {
    if (!toggle) return;
    var closed = all().filter(function (d) { return !d.open; }).length;
    toggle.textContent = closed ? "Expand all" : "Collapse all";
    toggle.setAttribute("aria-expanded", closed ? "false" : "true");
  }

  function init() {
    watchNav();
    if (!all().length) return;

    toggle = document.getElementById("cv-expand-all");
    if (toggle) {
      toggle.hidden = false;
      toggle.addEventListener("click", function () {
        var open = all().some(function (d) { return !d.open; });
        all().forEach(function (d) { d.open = open; });
        syncToggle();
      });
      syncToggle();
    }

    /* a nav link to a section already in view fires no hashchange, so the click
       is handled directly as well */
    document.addEventListener("click", function (e) {
      var a = e.target.closest ? e.target.closest('a[href^="#"]') : null;
      if (!a) return;
      if (reveal(a.getAttribute("href"), false)) syncToggle();
    });

    window.addEventListener("hashchange", function () {
      reveal(location.hash, true);
    });

    all().forEach(function (d) {
      d.addEventListener("toggle", syncToggle);
    });

    /* a section closed at load time has no height yet, so the browser cannot
       land on a deep link on its own; the second pass is for the font swap,
       which moves everything below the sticky bar */
    if (location.hash) {
      reveal(location.hash, true);
      window.addEventListener("load", function () { reveal(location.hash, true); });
      if (document.fonts && document.fonts.ready) {
        document.fonts.ready.then(function () { reveal(location.hash, true); });
      }
    }
  }

  /* print and PDF export get the whole CV, whatever is open on screen */
  window.addEventListener("beforeprint", function () {
    all().forEach(function (d) {
      if (!d.open) { d.dataset.wasClosed = "1"; d.open = true; }
    });
  });
  window.addEventListener("afterprint", function () {
    all().forEach(function (d) {
      if (d.dataset.wasClosed) { d.open = false; delete d.dataset.wasClosed; }
    });
    syncToggle();
  });

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();

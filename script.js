// Scroll-reveal with hard guarantees: content can never stay hidden.
// - Elements already in the viewport are revealed immediately on load.
// - IntersectionObserver animates the rest in as you scroll.
// - Failsafes re-check on load/pageshow/resize, and a final timer reveals
//   anything still pending in the viewport.
(function () {
  // Always load at the top (scrollRestoration is set to "manual" inline in <head>).
  // The 2px nudge forces the compositor to repaint — some embedded browsers
  // otherwise hold a stale blank frame after reload.
  window.scrollTo(0, 0);
  const resetScroll = () => {
    requestAnimationFrame(() => {
      window.scrollTo(0, 2);
      requestAnimationFrame(() => window.scrollTo(0, 0));
    });
  };
  window.addEventListener("load", resetScroll);
  window.addEventListener("pageshow", resetScroll);

  // Self-heal for embedded previews that restore scroll from OUTSIDE the page
  // after load (which can leave a stale, blank compositor frame): if a scroll
  // arrives early with no preceding user input, nudge 1px to force a repaint.
  let userInput = false;
  ["wheel", "touchstart", "keydown", "pointerdown"].forEach((t) =>
    window.addEventListener(t, () => { userInput = true; }, { passive: true, capture: true })
  );
  const healDeadline = performance.now() + 2500;
  window.addEventListener("scroll", () => {
    if (userInput || performance.now() > healDeadline) return;
    requestAnimationFrame(() => { window.scrollBy(0, 1); window.scrollBy(0, -1); });
  }, { passive: true });

  const els = Array.from(document.querySelectorAll(".reveal"));
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const showAll = () => els.forEach((el) => el.classList.add("in"));

  if (reduced || !("IntersectionObserver" in window)) {
    showAll();
    return;
  }

  const inViewport = (el) => {
    const r = el.getBoundingClientRect();
    return r.top < window.innerHeight && r.bottom > 0;
  };

  // Reveal whatever is on screen right now (handles reload mid-page,
  // scroll restoration, anchor jumps).
  const sweep = () => els.forEach((el) => { if (inViewport(el)) el.classList.add("in"); });

  const io = new IntersectionObserver(
    (entries) => {
      for (const e of entries) {
        if (e.isIntersecting) {
          e.target.classList.add("in");
          io.unobserve(e.target);
        }
      }
    },
    { threshold: 0.05 }
  );
  els.forEach((el) => io.observe(el));

  sweep();
  window.addEventListener("load", sweep);
  window.addEventListener("pageshow", sweep);
  window.addEventListener("resize", sweep, { passive: true });
  window.addEventListener("scroll", sweep, { passive: true, once: true });
  setTimeout(sweep, 500);
  setTimeout(sweep, 1500);

  // Smooth scrolling for in-page anchors only (CSS scroll-behavior:smooth is
  // deliberately not used — it breaks scroll restoration on reload).
  document.querySelectorAll('a[href^="#"]').forEach((a) => {
    a.addEventListener("click", (ev) => {
      const target = document.querySelector(a.getAttribute("href"));
      if (!target) return;
      ev.preventDefault();
      target.scrollIntoView({ behavior: reduced ? "auto" : "smooth", block: "start" });
      history.pushState(null, "", a.getAttribute("href"));
    });
  });
})();

// Hero: word-by-word headline entrance + pointer parallax on floating artifacts.
(function () {
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const h1 = document.querySelector(".hero h1");
  if (h1 && !reduced) {
    const parts = [];
    Array.from(h1.childNodes).forEach((n) => {
      if (n.nodeType === Node.TEXT_NODE) {
        n.textContent.split(/(\s+)/).forEach((t) => {
          if (!t) return;
          if (/^\s+$/.test(t)) { parts.push(document.createTextNode(t)); return; }
          const s = document.createElement("span"); s.className = "w"; s.textContent = t; parts.push(s);
        });
      } else { n.classList.add("w"); parts.push(n); }
    });
    h1.textContent = "";
    parts.forEach((p) => h1.appendChild(p));
    h1.querySelectorAll(".w").forEach((w, i) => { w.style.transitionDelay = (0.055 * i) + "s"; });
    requestAnimationFrame(() => requestAnimationFrame(() => h1.classList.add("h1-in")));
  } else if (h1) { h1.classList.add("h1-in"); }

  const hero = document.querySelector(".hero");
  const art = document.querySelector(".hero-art");
  if (!hero || !art || reduced || window.matchMedia("(pointer: coarse)").matches) return;
  const layers = art.querySelectorAll("[data-depth]");
  let tx = 0, ty = 0, cx = 0, cy = 0, raf = null;
  hero.addEventListener("mousemove", (e) => {
    const r = hero.getBoundingClientRect();
    tx = (e.clientX - r.left) / r.width - 0.5;
    ty = (e.clientY - r.top) / r.height - 0.5;
    if (!raf) loop();
  });
  function loop() {
    raf = requestAnimationFrame(loop);
    cx += (tx - cx) * 0.06; cy += (ty - cy) * 0.06;
    layers.forEach((l) => {
      const d = parseFloat(l.dataset.depth || "0.5");
      l.style.transform = "translate3d(" + (-cx * 38 * d).toFixed(2) + "px, " + (-cy * 28 * d).toFixed(2) + "px, 0)";
    });
    if (Math.abs(tx - cx) < 0.001 && Math.abs(ty - cy) < 0.001) { cancelAnimationFrame(raf); raf = null; }
  }
})();

// Nav scrollspy: mark the link whose section is in view. Only same-page
// anchors participate (case pages link back to index.html#… and are skipped).
(function () {
  const links = Array.from(document.querySelectorAll('.nav-links a[href^="#"]:not(.btn)'));
  const pairs = links
    .map((a) => [document.querySelector(a.getAttribute("href")), a])
    .filter(([sec]) => sec);
  if (!pairs.length || !("IntersectionObserver" in window)) return;
  const bySection = new Map(pairs);
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      const link = bySection.get(e.target);
      if (e.isIntersecting) {
        links.forEach((a) => a.classList.remove("active"));
        link.classList.add("active");
      } else if (link.classList.contains("active") && e.boundingClientRect.top > 0) {
        link.classList.remove("active"); // scrolled back above the section
      }
    });
  }, { rootMargin: "-20% 0px -55% 0px" });
  pairs.forEach(([sec]) => io.observe(sec));
})();

// AI panel: its orb/aurora animations are ambient and infinite — pause them
// whenever the panel is offscreen so they cost nothing while out of view.
(function () {
  const panel = document.querySelector(".ai-panel");
  if (!panel || !("IntersectionObserver" in window)) return;
  // Set the initial state synchronously — IO's first callback can be delayed
  // (or throttled entirely in embedded webviews), and the panel is usually
  // below the fold on load.
  const r = panel.getBoundingClientRect();
  panel.classList.toggle("paused", r.bottom < -100 || r.top > window.innerHeight + 100);
  const io = new IntersectionObserver((entries) => {
    const e = entries[entries.length - 1];
    panel.classList.toggle("paused", !e.isIntersecting);
  }, { rootMargin: "100px 0px" });
  io.observe(panel);
})();

// Touch carousels: on coarse-pointer devices the CSS transform-marquees can't be
// swiped and their :hover pause sticks on a tap. So on touch we turn the tracks
// into native horizontal scrollers (see styles.css) and drive a gentle auto-
// advance here that PAUSES while a finger is down and, ~1.5s after release, EASES
// back into motion (ramps the speed up) — mirroring the desktop hover behaviour.
// Testimonials also collapse from two rows to one ordered row on mobile.
(function () {
  if (!window.matchMedia("(hover: none) and (pointer: coarse)").matches) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  // Rebuild the two testimonial rows into a single row in a deliberate order:
  // lead with a photo, then two cards, then the other photo, then the rest.
  function reflowTestimonialsToOneRow() {
    const m = document.querySelector(".t-marquee");
    if (!m) return null;
    const orig = {};
    m.querySelectorAll(".t-card:not([aria-hidden])").forEach((c) => { orig[c.dataset.p] = c; });
    const order = ["andres", "ilya", "jamell", "rebecca", "jayne", "viktor", "enoch", "more"];
    const row = document.createElement("div");
    row.className = "t-row";
    order.forEach((k) => { if (orig[k]) row.appendChild(orig[k]); });          // move the originals
    order.forEach((k) => {                                                     // + a hidden clone set for the loop
      if (!orig[k]) return;
      const d = orig[k].cloneNode(true);
      d.setAttribute("aria-hidden", "true");
      if (d.tagName === "A") d.setAttribute("tabindex", "-1");
      row.appendChild(d);
    });
    m.innerHTML = "";
    m.appendChild(row);
    return row;
  }

  function drive(el, durationSec, periods) {
    if (!el) return;
    let paused = false, resumeAt = 0, rampStart = 0, last = null, visible = true;
    let loopW = el.scrollWidth / periods;      // width of one repeated set
    let speed = loopW / durationSec;           // px per second
    // Position lives in a float accumulator, NOT in el.scrollLeft: mobile Safari
    // stores scrollLeft as an integer, so per-frame increments under 1px
    // (scrollLeft += 0.4) truncate back to the old value and the carousel never
    // moves. We advance `pos` and assign it; sub-pixel progress survives here.
    let pos = el.scrollLeft;
    const recalc = () => { loopW = el.scrollWidth / periods; speed = loopW / durationSec; };
    window.addEventListener("resize", recalc, { passive: true });
    window.addEventListener("load", recalc);

    const wrap = () => {
      if (pos >= loopW) pos -= loopW;
      else if (pos < 0) pos += loopW;
    };
    // touch events are reliable on touch devices (pointer events get canceled once
    // native scrolling takes over): finger down pauses, lift schedules the resume.
    el.addEventListener("touchstart", () => { paused = true; resumeAt = Infinity; }, { passive: true });
    const resumeSoon = () => { if (resumeAt !== 0) resumeAt = performance.now() + 1500; };
    el.addEventListener("touchend", resumeSoon, { passive: true });
    el.addEventListener("touchcancel", resumeSoon, { passive: true });

    // Scrolls we didn't write (finger drags, momentum after release) become the
    // new position, so the auto-advance resumes exactly where the user left off.
    // Momentum also keeps pushing the resume deadline back — motion restarts
    // ~1.5s after the carousel actually comes to rest, not after the finger lifts.
    el.addEventListener("scroll", () => {
      const sl = el.scrollLeft;
      if (Math.abs(sl - pos) > 1.5) {
        pos = sl;
        if (paused && resumeAt !== Infinity) resumeAt = performance.now() + 1500;
      }
      if (pos >= loopW || pos < 0) { wrap(); el.scrollLeft = pos; } // seamless manual loop
    }, { passive: true });

    // don't spend cycles auto-advancing while the carousel is offscreen
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(
        (es) => { visible = es[es.length - 1].isIntersecting; },
        { rootMargin: "60px 0px" }
      ).observe(el);
    }

    requestAnimationFrame(function frame(t) {
      if (last == null) last = t;
      const dt = Math.min(0.05, (t - last) / 1000); last = t;
      if (paused && performance.now() >= resumeAt) { paused = false; rampStart = performance.now(); }
      if (visible && !paused) {
        const ramp = Math.min(1, (performance.now() - rampStart) / 900); // ease speed back in
        pos += speed * ramp * dt;
        wrap();
        el.scrollLeft = pos;
      }
      requestAnimationFrame(frame);
    });
  }

  const oneRow = reflowTestimonialsToOneRow();
  drive(oneRow, 120, 2);                              // testimonials (8 cards, gentle)
  drive(document.querySelector(".work-track"), 38, 2); // projects
})();

// Mobile nav: the hamburger toggles the dropdown menu (≤760px). It closes when
// a link is tapped, on Escape, on an outside click, or when the viewport grows
// back to the desktop layout.
(function () {
  const nav = document.querySelector(".nav");
  const toggle = document.querySelector(".nav-toggle");
  const links = document.querySelector(".nav-links");
  if (!nav || !toggle || !links) return;

  const setOpen = (open) => {
    nav.classList.toggle("nav-open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
  };

  toggle.addEventListener("click", () => setOpen(!nav.classList.contains("nav-open")));
  links.addEventListener("click", (e) => { if (e.target.closest("a")) setOpen(false); });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && nav.classList.contains("nav-open")) { setOpen(false); toggle.focus(); }
  });
  document.addEventListener("click", (e) => {
    if (nav.classList.contains("nav-open") && !nav.contains(e.target)) setOpen(false);
  });
  window.addEventListener("resize", () => { if (window.innerWidth > 760) setOpen(false); }, { passive: true });
})();

/* ---------- hero reel: Ken-Burns showreel over project screens ---------- */
// A framed "showreel": each shot's img runs a slow zoom/pan (pure CSS, see the
// m-* classes); this module runs the cut list — dissolve to the next shot and
// update the lower-third tag + progress dots. Pauses on hover and offscreen;
// never starts under prefers-reduced-motion (the first frame just sits still).
(() => {
  const art = document.querySelector(".hero-art");
  const reel = document.querySelector(".hreel");
  if (!art || !reel) return;
  const shots = Array.from(reel.querySelectorAll(".hreel-shot"));
  const tag = reel.querySelector(".hreel-tag");
  const dots = Array.from(reel.querySelectorAll(".hreel-dots i"));
  if (shots.length < 2) return;
  let i = 0;

  const cut = (n) => {
    const cur = shots[i], next = shots[n];
    cur.classList.add("out");          // outgoing dissolves above…
    next.classList.add("on");          // …the incoming, already moving
    setTimeout(() => cur.classList.remove("on", "out"), 1050);
    if (tag) {
      tag.textContent = next.dataset.name || "";
      tag.classList.remove("bump"); void tag.offsetWidth; tag.classList.add("bump");
    }
    dots.forEach((d, k) => d.classList.toggle("on", k === n));
    i = n;
  };

  shots[0].classList.add("on");
  if (tag) tag.textContent = shots[0].dataset.name || "";
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  const SHOT_MS = 5600;
  let timer = setInterval(() => cut((i + 1) % shots.length), SHOT_MS);
  const stop = () => { if (timer) { clearInterval(timer); timer = null; } };
  const start = () => { if (!timer) timer = setInterval(() => cut((i + 1) % shots.length), SHOT_MS); };
  art.addEventListener("mouseenter", stop);
  art.addEventListener("mouseleave", start);
  // don't churn while the hero is scrolled away
  if ("IntersectionObserver" in window) {
    new IntersectionObserver((es) => {
      if (es[es.length - 1].isIntersecting) start(); else stop();
    }).observe(reel);
  }
})();

/* ---------- hero v2: curtain cleanup + cursor-weight intro ---------- */
// The intro line is split into chars; each char's variable-font weight rises
// as the cursor approaches (Plus Jakarta Sans is loaded as a variable font).
// Screen readers get the sentence via aria-label on the h1.
(() => {
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const curtain = document.querySelector(".curtain");
  if (curtain) {
    if (reduced) curtain.remove(); // CSS hides it; drop the node too
    else curtain.addEventListener("animationend", () => curtain.remove());
  }

  const intro = document.querySelector(".hero2-intro");
  if (!intro) return;

  const text = intro.textContent.trim().replace(/\s+/g, " ");
  intro.setAttribute("aria-label", text);

  // split into word spans (keep wrapping word-level) holding char spans
  const chars = [];
  const frag = document.createDocumentFragment();
  text.split(" ").forEach((word, i) => {
    if (i) frag.appendChild(document.createTextNode(" "));
    const w = document.createElement("span");
    w.className = "w2";
    w.setAttribute("aria-hidden", "true");
    for (const ch of word) {
      const c = document.createElement("span");
      c.textContent = ch;
      w.appendChild(c);
      chars.push(c);
    }
    frag.appendChild(w);
  });
  intro.textContent = "";
  intro.appendChild(frag);

  if (reduced || !window.matchMedia("(pointer: fine)").matches) return;

  const BASE = 500, MAX = 800, SIGMA = 58, CUTOFF = 240;
  const n = chars.length;
  const cur = new Float32Array(n).fill(BASE);
  const shown = new Int16Array(n).fill(BASE);
  let cx = new Float32Array(n), cy = new Float32Array(n); // char centers, page coords
  let mx = -1e4, my = -1e4, raf = null;

  const measure = () => {
    chars.forEach((c, i) => {
      const r = c.getBoundingClientRect();
      cx[i] = r.left + r.width / 2 + window.scrollX;
      cy[i] = r.top + r.height / 2 + window.scrollY;
    });
  };
  // measure once entrance animation + fonts settle; keep fresh on resize
  const settle = () => setTimeout(measure, 1600);
  (document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(settle);
  window.addEventListener("resize", () => setTimeout(measure, 120), { passive: true });

  const loop = () => {
    raf = requestAnimationFrame(loop);
    let busy = false;
    for (let i = 0; i < n; i++) {
      const dx = cx[i] - mx, dy = cy[i] - my;
      const d = Math.sqrt(dx * dx + dy * dy);
      const target = d > CUTOFF ? BASE : BASE + (MAX - BASE) * Math.exp(-(d * d) / (2 * SIGMA * SIGMA));
      cur[i] += (target - cur[i]) * 0.16;
      if (Math.abs(target - cur[i]) > 0.4) busy = true;
      const rounded = Math.round(cur[i]);
      if (rounded !== shown[i]) {
        shown[i] = rounded;
        chars[i].style.fontVariationSettings = '"wght" ' + rounded;
      }
    }
    if (!busy) { cancelAnimationFrame(raf); raf = null; }
  };
  window.addEventListener("mousemove", (e) => {
    mx = e.clientX + window.scrollX;
    my = e.clientY + window.scrollY;
    if (!raf) loop();
  }, { passive: true });
})();

/* ---------- hero v2: project cards drifting along an arc ---------- */
// matmac-style strip: each card rides a CSS offset-path arc; a rAF loop
// advances a shared offset so the whole set drifts, fading at both ends.
// offset-rotate:auto (the default) tilts cards to follow the curve.
(() => {
  const arc = document.querySelector(".hero2-arc");
  if (!arc) return;
  if (!CSS.supports("offset-distance", "0%")) { arc.remove(); return; } // no pile-ups on old engines

  const cards = Array.from(arc.querySelectorAll(".hero2-card"));
  const n = cards.length;
  if (!n) return;

  const PATH = 'path("M 1 127 C 1 127 359 1 865 1 C 1371 1 1729 127 1729 127")';
  cards.forEach((c) => { c.style.offsetPath = PATH; });

  const SPACING = 10;                 // % of path between cards
  const CYCLE = n * SPACING;          // full loop length (>100 so cards wrap offstage)
  const BUF = (CYCLE - 100) / 2;      // offstage margin at each end
  const FADE = 9;                     // % of path over which cards fade in/out
  const CRUISE = 1.1, HOVER = 0.25;   // %/s — brisk drift, eases off while inspecting a card

  let base = 0, speed = CRUISE, targetSpeed = CRUISE;
  arc.addEventListener("pointerover", (e) => { if (e.target.closest(".hero2-card")) targetSpeed = HOVER; });
  arc.addEventListener("pointerout", (e) => { if (e.target.closest(".hero2-card")) targetSpeed = CRUISE; });
  const place = () => {
    for (let i = 0; i < n; i++) {
      const pos = ((base + i * SPACING) % CYCLE) - BUF;
      const card = cards[i];
      if (pos < 0 || pos > 100) { card.style.opacity = "0"; continue; }
      card.style.offsetDistance = pos.toFixed(3) + "%";
      card.style.opacity = Math.min(pos / FADE, (100 - pos) / FADE, 1).toFixed(3);
    }
  };
  place();

  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return; // static arc

  let last = null, raf = null;
  const tick = (now) => {
    raf = requestAnimationFrame(tick);
    speed += (targetSpeed - speed) * 0.06; // glide between cruise and hover pace
    if (last !== null) base = (base + speed * ((now - last) / 1000)) % CYCLE;
    last = now;
    place();
  };
  const start = () => { if (!raf) { last = null; raf = requestAnimationFrame(tick); } };
  const stop = () => { if (raf) { cancelAnimationFrame(raf); raf = null; } };
  start();
  // don't churn while the hero is scrolled away
  if ("IntersectionObserver" in window) {
    new IntersectionObserver((es) => {
      if (es[es.length - 1].isIntersecting) start(); else stop();
    }).observe(arc);
  }
})();

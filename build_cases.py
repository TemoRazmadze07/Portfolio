#!/usr/bin/env python3
"""Generate the four case-study pages (tbc/golance/novocure/rogers .html)
from one data structure. Content source of truth: ../CASE_STUDIES.md.
Regenerate: python3 build_cases.py
"""
V = "38"  # cache-bust version, keep in sync with index.html

CASES = [
 dict(
  slug="tbc", tint="tint-blue", ph="ph-tbc",
  kicker="TBC Bank · Banking",
  title="Business Internet Bank redesign — winner of Global Finance's “Best Online Portal” 2021",
  meta=[("Role","Senior Product Designer / Information Architect"),
        ("Company","TBC Bank — Georgia's leading bank"),
        ("When","Jun 2016 – Jan 2022 (UX Designer → Senior)"),
        ("Scope","End-to-end redesign of the corporate internet-banking platform")],
  tiles=[("2021","Global Finance “Best Online Portal”"),("55→64","Business Mobile Bank NPS"),("−7%","website drop-off")],
  problem="TBC's Business Internet Bank carried the full set of operations a company needs to run its finances, but years of feature growth had buried them under navigation that no longer matched how businesses actually worked. Usage data and known pain points showed users struggling to find core operations and spending too long on routine tasks. The brief wasn't a facelift — it was to prove, with evidence, whether a full redesign was justified, then deliver it.",
  role="I led the redesign end-to-end with product, business, and engineering — from the evidence-gathering that justified it to the shipped platform. I'd started at TBC as a UX Designer, where I built the design-system foundation this redesign later extended.",
  moments=[
   ("Diagnose before redesigning","I ran tree testing against the existing navigation to isolate exactly where the information architecture broke down — so the rebuild stood on evidence, not internal assumptions about where features “should” live.","a"),
   ("An IA organized by how businesses operate","I rearchitected the information architecture and core flows around real task paths, trading the legacy menu for a structure that cut time-on-task on the highest-frequency operations.","b"),
   ("A platform, not a screen set","New features and enhanced flows were built on shared, reusable patterns — extending the design-system foundation so the experience stayed consistent as the product grew.","a"),
  ],
  also=["Started from quantitative data, business goals, and the documented problem set — arguing a structural redesign, not incremental patching, was the right investment.",
        "Established a repeatable research-based design process, tracked with Google's HEART framework against NPS, time-on-task, and conversion."],
  outcome="The redesigned platform earned TBC the “Best Online Portal” category in Global Finance's World's Best Corporate/Institutional Digital Banks Awards 2021 — recognition leadership tied directly to the business internet bank. The same research-led approach carried across TBC's digital estate: Business Mobile Bank NPS from 55 to 64, a corporate intranet redesign (+20% engagement), a website IA change (−7% drop-off), and loan/savings calculators (+12% lead conversion).",
  skills="Information architecture · tree testing · UX research · measurement (HEART) · design systems · interaction design · stakeholder alignment",
  reflection="With more time I'd have instrumented navigation analytics from day one — tree testing found the breakages, but continuous funnel data would have caught them sooner.",
 ),
 dict(
  slug="golance", tint="tint-green", ph="ph-golance",
  kicker="goLance · AI marketplace",
  title="Matching trust — designing the UX for goLance's AI cultural-fit engine",
  meta=[("Role","Senior User Experience Designer"),
        ("Company","goLance — global freelance marketplace (1M+ freelancers)"),
        ("When","Apr 2025 – Apr 2026 · remote (Wrocław)"),
        ("Scope","End-to-end design: freelancer portal, client side, payments, AI features")],
  tiles=[("+25%","project engagement"),("−22%","checkout drop-off"),("−40%","support load")],
  problem="At marketplace scale, matching on skills alone still produced mismatched, short-lived engagements — the real gap was cultural and working-style fit, which is hard to assess and easy to fake. The company was betting on AI to close it, but AI matching and automated assessment only create value if hiring users trust and act on what the model surfaces. My job was to make opaque, probabilistic outputs legible and credible inside real hiring decisions.",
  role="End-to-end design owner across the freelancer portal, client/recruiter side, payments, and the platform's AI features — working directly with the AI/data and product teams. I designed the UX of the AI features; the models were built by the AI/data team.",
  moments=[
   ("An assessment that builds a real profile","I designed the Cultural Fit Assessment end-to-end — an LLM-supported, scenario-based evaluation where AI-generated adaptive questions build an individual cultural profile. I designed how questions branch and how answers resolve into a profile.","a"),
   ("Scores as confidence, not verdicts","Because matching is a learning model rather than static scoring, I designed compatibility scores and “Best Match” indicators to read as confidence signals — placed at the decision point in the hiring flow, informing the hire without overclaiming certainty the model couldn't back.","b"),
   ("Designing for imperfect AI","On Mango AI, the contractor-management assistant, I shaped how AI-generated summaries, performance insights, and flagged issues are presented — prioritizing what a client needs to verify, and making each flag's reasoning inspectable so people trust it enough to act.","a"),
  ],
  also=["Rebuilt payment and checkout by mapping drop-off, cutting steps, and clarifying cost and confirmation states.",
        "Designed the core work-verification workflows — dashboards, scheduling, time tracking, in-hours session monitoring — balancing employer verification against freelancer transparency.",
        "Drove marketplace-wide usability through IA and interface consistency; contributed to the marketing website."],
  outcome="The Cultural Fit Assessment and matching experience raised project engagement by 25%. The checkout redesign cut drop-off by 22% and support load by 40%, and broader usability work reduced task-completion time by 30%. The harder result: hiring users had a reason to trust automated matching, and acted on model outputs they would otherwise have ignored.",
  skills="UX research · information architecture · interaction design · AI/LLM UX · design systems · WCAG accessibility · cross-functional work with AI/data · Figma",
  reflection="Next I'd push explainability further — surfacing why a match scored the way it did, not just how confident the model is.",
 ),
 dict(
  slug="novocure", tint="tint-sand", ph="ph-novocure",
  kicker="Novocure · Healthcare, via EPAM",
  title="Restarting an oncology HCP portal from zero — three markets, WCAG AA, +21% sales",
  meta=[("Role","Senior Experience Designer (design lead from mid-project)"),
        ("Client","Novocure — global oncology (Optune), via EPAM Systems"),
        ("When","Jul 2024 – Apr 2025"),
        ("Scope","HCP portal: orders, renewals, device tracking · US / DE / FR")],
  tiles=[("+21%","sales, Q4 2024"),("87/100","SUS score"),("3","markets at WCAG AA")],
  problem="A previous vendor had abandoned the build, leaving Novocure without a working way for HCPs and their staff to place orders, manage renewals, and coordinate patient device usage — while sales depended on that workflow being frictionless. The portal had to serve three markets with different personas, clinical practices, date formats, and legal constraints — not one design translated three ways. And given the treatment context, accessibility wasn't optional: every screen had to meet WCAG Level AA.",
  role="Senior Experience Designer on the EPAM engagement; took over design leadership mid-project after the lead designer left — owning design processes, demos, stakeholder communication, and delivery alongside the design work itself.",
  moments=[
   ("Three markets, three design problems","350+ requirements became 400+ prototype screens across the US, German, and French markets — treating each market's personas, medical-domain practices, and legal constraints as distinct design problems, not localization.","a"),
   ("Accessibility from the first component","Contrast, focus order, semantic structure, and assistive-tech support were built into components from the start rather than retrofitted — so WCAG AA held even as requirements changed near-daily.","b"),
   ("A design library as the single source of truth","One library across all three markets — the trade-off that made it possible to ship at volume, on deadline, while protecting consistency and future maintenance.","a"),
  ],
  also=["Built the IA and core task flows — orders, renewals, task management, team coordination — around how HCP staff actually work.",
        "Stepped into design leadership mid-project: set up missing processes, ran design demos, kept delivery on track through churn.",
        "Ran on-site stakeholder workshops in Lucerne with CH and DE stakeholders — driving same-day/next-day approvals and lifting team velocity by 30%."],
  outcome="Delivered every MVP alpha and beta requirement on time. The redesign contributed to +21% sales in Q4 2024, and the portal scored 87/100 on the System Usability Scale — turning a stalled, vendor-abandoned project into a maintainable foundation across three markets.",
  skills="UX/UI design · information architecture · WCAG AA accessibility · multi-market design · design systems/libraries · prototyping · stakeholder workshops · design leadership · Figma",
  reflection="I'd formalize accessibility annotations into the design library from day one — we retrofitted documentation that should have been born with the components.",
 ),
 dict(
  slug="rogers", tint="tint-rose", ph="ph-rogers",
  kicker="Rogers Communications · Telecom, via EPAM",
  title="OneView: cutting the sales rep's cognitive load — −25% time-on-task, −80% errors",
  meta=[("Role","Experience Designer"),
        ("Client","Rogers Communications — Canadian telecom, 10M+ customers, via EPAM"),
        ("When","Jan 2022 – Jul 2024"),
        ("Scope","Rep-facing sales & support platform · multi-line device buy flow")],
  tiles=[("−25%","time-on-task"),("−80%","user error rate"),("3wk→1wk","agent onboarding")],
  problem="Care reps lost time and made costly mistakes in OneView's multi-line device buy flow: too many clicks, too much on-screen complexity, and payment logic that forced them back and forth or into a second system mid-conversation. Every customer interaction ran slower, error rates climbed, and new agents took weeks to get up to speed.",
  role="Experience Designer on the EPAM engagement — owning the redesign of the buy flow across research, IA, interaction design, and accessibility, working with product, engineering, and Rogers stakeholders.",
  moments=[
   ("Layout grounded in how reps actually work","Research showed reps didn't rely on a large product photo — so I shrank the device image to a compact visual anchor and gave that space back to the information reps act on, cutting scanning effort instead of decorating the page.","a"),
   ("One legible payment decision","I merged scattered payment options into a single view with an automatic total-savings calculation — ending the back-and-forth (and the second system) that carried the highest cognitive load.","b"),
   ("Depth on demand","A full-screen device-spec modal, a compare-up-to-3-devices feature, and stock availability split by delivery vs in-store pickup — so reps could answer detailed questions without ever leaving the buy flow.","a"),
  ],
  also=["Preselected the lowest-price storage option (reps always open the conversation at the lowest price point) with a dynamic SKU header updating live as options change.",
        "Simplified the IA and minimized clicks so the flow matched the real sequence of a sales conversation.",
        "Ran accessibility audits and implemented WCAG fixes — removing a large share of the old flow's interaction errors."],
  outcome="25% less time-on-task on the buy flow, an 80% drop in user error rate, and new-agent onboarding cut from 3 weeks to 1. The work earned the “Customer Centered” badge twice and a 3.9/4 stakeholder rating — reps could hold the customer conversation inside one coherent flow instead of working around the tool.",
  skills="UX research · information architecture · interaction & responsive design · design systems · UX writing · competitive analysis · WCAG accessibility audits · prototyping",
  reflection="Given another cycle, I'd extend the same cognitive-load lens to the post-sale service flows reps rely on every day.",
 ),
]

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Temuri Razmadze</title>
<meta name="description" content="Case study: {kicker}. {tiles_line}">
<link rel="canonical" href="https://temorazmadze07.github.io/Portfolio/{slug}.html">

<!-- Open Graph / social share preview -->
<meta property="og:type" content="article">
<meta property="og:site_name" content="Temuri Razmadze">
<meta property="og:title" content="{title} — Temuri Razmadze">
<meta property="og:description" content="Case study · {kicker}. {tiles_line}">
<meta property="og:url" content="https://temorazmadze07.github.io/Portfolio/{slug}.html">
<meta property="og:image" content="https://temorazmadze07.github.io/Portfolio/assets/og-image.png">
<meta property="og:image:type" content="image/png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title} — Temuri Razmadze">
<meta name="twitter:description" content="Case study · {kicker}. {tiles_line}">
<meta name="twitter:image" content="https://temorazmadze07.github.io/Portfolio/assets/og-image.png">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css?v={v}">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="assets/favicon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="assets/favicon-16.png" sizes="16x16" type="image/png">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<link rel="shortcut icon" href="assets/favicon.ico">
<script>if ("scrollRestoration" in history) history.scrollRestoration = "manual";</script>
</head>
<body>

<header class="nav">
  <div class="nav-inner">
    <a class="nav-name" href="index.html">Temuri&nbsp;Razmadze</a>
    <nav class="nav-links" aria-label="Main">
      <a href="index.html#work" aria-label="Work"><svg class="nav-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/></svg><span class="nav-label">Work</span></a>
      <a href="index.html#ai" aria-label="How I work"><svg class="nav-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3.5 L14 9.5 L20 11.5 L14 13.5 L12 19.5 L10 13.5 L4 11.5 L10 9.5 Z"/><path d="M18.5 3.5 v4 M16.5 5.5 h4"/></svg><span class="nav-label">How I work</span></a>
      <a href="index.html#words" aria-label="Recommendations"><svg class="nav-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.38 8.38 0 0 1-8.4 8.4 8.5 8.5 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.4 8.4 0 0 1 8.4-8.4h.5a8.48 8.48 0 0 1 8.1 8.1z"/></svg><span class="nav-label">Recommendations</span></a>
      <a href="index.html#contact" aria-label="Contact"><svg class="nav-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2.5" y="5" width="19" height="14" rx="2.5"/><path d="m3.5 7 8.5 6 8.5-6"/></svg><span class="nav-label">Contact</span></a>
      <a class="btn btn-small" href="assets/CV_Temuri_Razmadze.pdf" download aria-label="Download CV (PDF)"><span class="cv-long">Download CV</span><span class="cv-short" aria-hidden="true">CV</span></a>
    </nav>
  </div>
</header>
"""

def tiles_html(tiles):
    cells = "".join(f'<div class="m-tile"><span class="m-num">{n}</span><span class="m-label">{l}</span></div>' for n,l in tiles)
    return cells

def moments_html(c):
    out = []
    for i,(h,p,variant) in enumerate(c["moments"]):
        flip = " flip" if i % 2 == 1 else ""
        out.append(f'''
      <div class="moment{flip} reveal">
        <figure class="m-fig"><img src="assets/{c['ph']}-{variant}.svg" alt="" loading="lazy"><figcaption>placeholder — real screens coming</figcaption></figure>
        <div class="m-txt"><h3>{h}</h3><p>{p}</p></div>
      </div>''')
    return "".join(out)

def page(c, nxt):
    meta = "".join(f'<div><b>{k}</b><span>{v}</span></div>' for k,v in c["meta"])
    also = "".join(f"<li>{x}</li>" for x in c["also"])
    tiles_line = " · ".join(f"{n} {l}" for n,l in c["tiles"])
    return HEAD.format(title=c["title"], kicker=c["kicker"], tiles_line=tiles_line, v=V, slug=c["slug"]) + f"""
<main>
  <section class="case-hero">
    <div class="wrap">
      <a class="case-back reveal" href="index.html#work">← All work</a>
      <p class="kicker reveal"><span class="kbar"></span>{c["kicker"]}</p>
      <h1 class="reveal d1">{c["title"]}</h1>
      <div class="case-meta reveal d2">{meta}</div>
    </div>
  </section>

  <div class="wrap">
    <figure class="case-cover reveal"><img src="assets/{c['ph']}.svg" alt="" ><figcaption>placeholder — real screens coming</figcaption></figure>
    <div class="m-band {c['tint']} reveal">{tiles_html(c["tiles"])}</div>
  </div>

  <section class="case-sec">
    <div class="wrap">
      <p class="kicker reveal"><span class="kbar"></span>The problem</p>
      <p class="sec-text reveal">{c["problem"]}</p>
    </div>
  </section>

  <section class="case-sec">
    <div class="wrap">
      <p class="kicker reveal"><span class="kbar"></span>My role</p>
      <p class="sec-text reveal">{c["role"]}</p>
    </div>
  </section>

  <section class="case-sec">
    <div class="wrap">
      <p class="kicker reveal"><span class="kbar"></span>The work — decisions that mattered</p>
      {moments_html(c)}
      <div class="also reveal">
        <p class="also-label">Also part of the work</p>
        <ul>{also}</ul>
      </div>
    </div>
  </section>

  <section class="case-sec">
    <div class="wrap">
      <p class="kicker reveal"><span class="kbar"></span>Outcome</p>
      <p class="sec-text reveal">{c["outcome"]}</p>
      <p class="case-skills reveal">{c["skills"]}</p>
    </div>
  </section>

  <section class="case-sec">
    <div class="wrap">
      <p class="kicker reveal"><span class="kbar"></span>Looking back</p>
      <p class="reflection-text reveal">{c["reflection"]}</p>
    </div>
  </section>

  <div class="wrap">
    <a class="case-next {nxt['tint']} reveal" href="{nxt['slug']}.html">
      <span><p class="card-kicker">Next case study</p><h2>{nxt["title"]}</h2></span>
      <span class="case-next-arrow">→</span>
    </a>
  </div>

  <section class="case-cta">
    <div class="wrap">
      <h2 class="contact-title reveal">Let's <span class="accent">talk</span></h2>
      <p class="contact-sub reveal d1">Open to senior product-design roles across Poland — hybrid or remote, B2B or employment contract.</p>
      <div class="hero-cta reveal d2">
        <a class="btn" href="mailto:temorazmadze01@gmail.com">temorazmadze01@gmail.com <span class="btn-arrow">→</span></a>
        <a class="btn btn-ghost" href="https://www.linkedin.com/in/temuri-razmadze" target="_blank" rel="noopener">LinkedIn</a>
      </div>
    </div>
  </section>
</main>

<footer class="footer">
  <div class="wrap footer-inner">
    <span>© 2026 Temuri Razmadze · Wrocław, Poland</span>
    <span class="footer-note">Designed &amp; built in an AI-augmented workflow — with Claude Code ✳</span>
  </div>
</footer>

<script src="script.js?v={V}"></script>
</body>
</html>
"""

for i,c in enumerate(CASES):
    nxt = CASES[(i+1) % len(CASES)]
    with open(f"{c['slug']}.html","w") as f:
        f.write(page(c, nxt))
    print("wrote", c["slug"] + ".html")

---
name: deck-chassis
description: Build a live HTML technical demo or narrated-rehearsal deck on the deck-chassis player — when to use it, the build_deck call, the standard slide types, the render-check gate, and the house style rules (co-brand footer, no accent boxes, teleprompter notes, narration respelling, presenter layout, countdown thresholds). PPTX export is a separate concern, not covered here.
---

# deck-chassis

Use this skill any time you're building or editing a **live HTML technical demo deck or a narrated rehearsal deck**. If the deliverable is a PPTX for a customer or a conference, this skill still applies to the HTML source-of-truth step (HTML is authored first, PPTX/PDF are exports) but PPTX-specific formatting is a separate, dedicated skill — out of scope here.

Library: `github.com/JimDemos/deck-chassis`. Clone or reference it, import `chassis.build_deck`.

## When to reach for this

- A new live demo deck (customer, conference, internal) that needs slide nav, presenter sync, or a terminal/demo panel
- A narrated rehearsal pass on an existing deck
- Fixing a chassis bug (nav, presenter sync, terminal panel, narration lock) — fix it in `deck-chassis`, not in a per-deck copy. If a deck still has its own forked chassis code, that's tech debt; point back here instead of patching the fork

## The build call

```python
from chassis import build_deck

build_deck(
    SLIDES,                      # list of (slide_type, fields, notes) tuples
    title="...",
    footer_text="...",           # right of the co-brand mark, lower-left
    logo_html="<div class=\"logo\">...</div>",
    fonts_css="",                 # @font-face block, embed brand fonts
    render_notes=render_notes,    # your say/[do]/{cue} -> HTML renderer, see below
    out_deck_path="present-x.html",
    out_presenter_path="present-x-presenter.html",
    terminal={"demo_hosts": {"see": {"url": "demos/see-it.html", "label": "..."}}},  # or None
    narration={"audio_manifest": [...], "audio_dir": "...", "rate": 1.10, "lock_key": "..."},  # or None
    presenter_budget_min=30,
)
```

Standard slide types (`chassis/slides.py`): `title`, `thesis`, `timeline`, `twocol`, `stat`, `grid`, `layers`, `model`, `demo`, `hack`, `recap`, `teach`, `tie`, `wall`, `trend`, `close`. Need a new shape — add a renderer there once; don't invent a one-off `<div>` soup in the deck's own build script.

Turn `terminal` and `narration` on or off per deck — a live meeting walkthrough wants the terminal panel and no narration; a stage rehearsal recording wants narration and may skip the terminal panel. Same chassis either way.

## Mandatory gate: render-check before shipping

Never hand Jim or show an unrendered deck. Playwright and chromium are already installed (`~/.cache/ms-playwright/`). Screenshot every slide, read the PNGs yourself (don't just check for zero errors), and check overflow:

```python
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1920, "height": 1080})
    pg.goto(URL)
    for i in range(total_slides):
        pg.evaluate(f"show({i}, true)")
        pg.wait_for_timeout(300)
        pg.screenshot(path=f"/tmp/check/slide{i+1}.png")
    b.close()
```

`overflow > 2px` on any slide means it breaks on a projector. Look at the actual PNGs — the numbers catch overflow, a look catches collisions and bad grid placement.

## House style rules (don't relitigate these)

- **Co-brand mark lower-left, level with the footer line.** No separate Red Hat logo top-right — one mark per slide. Same mark, same position on the title slide. Root font scales with viewport (`html{font-size:calc(100vw / 120)}`) so proportions hold on any monitor, projector, or thumbnail.
- **No accent-bordered callout boxes.** No `border-left`/`border-top` colored rail + rounded tinted background on any panel — Jim calls it an immediate AI tell ("boxes with eyelashes"). Emphasis = bold lead-in, a heading, or a plain thin `hr`. The flat full-width Red Hat red progress bar is brand, not decoration, and is fine.
- **Teleprompter notes markup:** script text is plain (renders white, flush-left — the `say` class), `[stage directions]` in brackets (renders amber, block-indented — the `do` class), `{facts and sources}` in braces (renders grey, block-indented — the `cue` class). `render_notes()` parses this with a regex over `[...]` / `{...}` / plain runs — see `examples/build_example.py` for the reference parser.
- **Narration respelling (TTS):** RHEL → `Rell`; SAP → `S-A-P` (hyphenated, not periods); SELinux → `essy Linux`; SUSE → `Soozay`; HIPAA → `hippah`; ePHI → `ee-fee`; RHEL versions spoken without "point" ("rell ten one"). First mention of any Red Hat initialism in a non-Red-Hat room: say it in full once, then abbreviate. Apply a respell map (`RESPELL` list of `(from, to)` tuples) before handing script text to TTS — see the S1 build's `notes_s1_draft5.py` for the working pattern.
- **Presenter view layout:** notes panel left at `3fr`, current+next slide thumbnails right at `1fr`, 16:9, not stretched (`object-fit`/transform-scale from the real 1920x1080 render, never CSS-stretched to fit the panel).
- **Countdown thresholds:** amber at 80% of budget elapsed, red at 92%. Budget is set per deck (`presenter_budget_min`), not hardcoded.

## Out of scope

- PPTX/PDF export — separate skill, separate concern. This skill covers the HTML authoring/live-presentation surface only, per the standing architecture decision: HTML is primary, PPTX/PDF are export targets, Google Slides is not the editing interface.
- Lab credentials, sandbox specifics, Red Hat/organiser-internal templates — never belong in this repo or any deck built on it if the deck is meant to be public.

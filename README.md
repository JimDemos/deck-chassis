# deck-chassis

A browser-based slide player and standard presenter control suite for live technical demos, factored out of a year of one-off Python deck builders (kpatch-demo, openscap-demo, ABB, CBC, SAP4U, and the ASUG Tech Connect 2026 "Securing the Enterprise" session).

## Why this exists

Every deck used to re-implement its own slide-show chassis from scratch: nav, presenter sync, the terminal/demo panel, narration. Fixes to one deck never carried forward to the others. This repo is the fix: one chassis, imported by every deck, with features a given presentation turns on or off instead of forking the code.

## Architecture

- **HTML is the primary authoring and live-presentation surface.** You write Python, you get a deck you walk through on stage. See `examples/build_example.py`.
- **PPTX and PDF are export targets**, generated from the same slide content for customer and conference deliverables where that's the expected format. This repo ships the player; PPTX/PDF export lives in each deck's own build script today (see `acme-demo-platform` modules) and will move here if/when it's genuinely shared code rather than deck-specific template wrangling.
- **Google Slides is not the editing interface.** It was considered and rejected: HTML stays authoritative, PPTX/PDF are exports alongside it.

## The standard control suite (v1 — always on)

- Keyboard/touch slide navigation (arrows, space, swipe, Home/End)
- Presenter-window sync over `BroadcastChannel` (deck + presenter stay in lockstep, including remote slide jumps)
- Teleprompter notes overlay (`N` key): `say` / `[do]` / `{cue}` markup
- Progress bar + slide counter
- Co-brand footer on every slide

## Optional, per-deck features (config, not forks)

| Feature | Toggle | What it adds |
|---|---|---|
| Terminal / demo panel | `terminal={"demo_hosts": {...}}` | `T` key slides in a 50vw iframe panel, one entry per demo host |
| Narration | `narration={"audio_manifest": [...], ...}` | Per-slide MP3 playback, single-narrator lock across open tabs (`M` mute, `A` auto-advance) |
| Presenter timer budget | `presenter_budget_min=N` | Countdown in the presenter view, amber at 80%, red at 92% |

A meeting walkthrough turns the terminal panel on and narration off. A rehearsal-record pass turns narration on. Same chassis either way — see `examples/build_example.py` for the minimal end-to-end case (no customer data), verified with a Playwright render check (nav, terminal toggle, notes toggle).

## Standard slide-type library

`chassis/slides.py` ships renderers for: `title`, `thesis`, `timeline`, `twocol`, `stat`, `grid`, `layers`, `model`, `demo`, `hack`, `recap`, `teach`, `tie`, `wall`, `trend`, `close`. New slide shapes get added here once; every deck picks them up.

## Usage

```python
from chassis import build_deck

build_deck(
    SLIDES,                      # list of (slide_type, fields, notes) tuples
    title="...",
    footer_text="...",
    logo_html="<div class=\"logo\">...</div>",
    fonts_css="",                 # embed brand fonts as @font-face here
    render_notes=render_notes,    # your say/[do]/{cue} -> HTML renderer
    out_deck_path="present-x.html",
    out_presenter_path="present-x-presenter.html",
    terminal={"demo_hosts": {"see": {"url": "demos/see-it.html", "label": "..."}}},
    narration=None,
    presenter_budget_min=30,
)
```

## Not published here

Lab credentials, sandbox specifics, and any Red Hat/organiser-internal template files stay out. Deck *content* that's OSINT-backed and conference-public is fine to publish per the standing "public talks: OSINT-backed names only" rule — that's a per-deck call, not a chassis one.

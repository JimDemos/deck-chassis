"""Orchestrator: slides + a feature config -> (deck_html, presenter_html).

This is the deterministic entry point. A new presentation is a slide list
(see slides.py for the standard types) plus a config that turns chassis
features on or off -- nothing about the chassis itself should need to change
per deck. If a deck needs a slide type or a control the chassis doesn't have,
add it here once and every deck gets it.
"""

from .css import CHASSIS_CSS
from .player_js import build_player_js
from .presenter import build_presenter_html
from .slides import render


def build_deck(
    slides,
    *,
    title,
    footer_text,
    logo_html,
    fonts_css,
    render_notes,
    out_deck_path,
    out_presenter_path=None,
    sync_channel="chassis-deck-sync",
    terminal=None,       # None, or {"demo_hosts": {key: {"url":..., "label":...}}}
    narration=None,      # None, or {"audio_manifest": [...], "audio_dir":..., "rate":1.0, "lock_key":...}
    presenter_budget_min=30,
):
    """slides: list of (slide_type, fields, notes) tuples.
    render_notes(raw_notes, index) -> HTML string for that slide's notes.
    Returns (deck_html, presenter_html_or_None).
    """
    n = len(slides)
    body_parts = []
    for i, (slide_type, fields, notes) in enumerate(slides, 1):
        term_key = fields.get("term") if terminal else None
        term_attr = f' data-term="{term_key}"' if term_key else ""
        active = " active" if i == 1 else ""
        body_parts.append(
            f'<div class="slide s-{slide_type}{active}"{term_attr} data-footer="{footer_text}">'
            f'{logo_html}{render(slide_type, fields)}'
            f'<div class="notes">{render_notes(notes, i - 1)}</div></div>'
        )

    features = {}
    if terminal:
        features["terminal"] = terminal
    if narration:
        features["narration"] = narration
    js = build_player_js(features, sync_channel=sync_channel)

    term_panel_html = ""
    if terminal:
        term_panel_html = (
            '<div id="term-panel"><div class="term-header">'
            '<span class="term-tag" id="term-tag">terminal</span>'
            '<span class="term-host" id="term-host"></span>'
            '<button class="term-close" onclick="closeTerm()">&#10005; close &middot; T</button></div>'
            '<iframe id="term-frame" src="about:blank"></iframe></div>'
        )

    deck_html = (
        f'<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>{title}</title>'
        f'<style>{fonts_css}{CHASSIS_CSS}</style></head><body>'
        f'<div id="progress"></div>{"".join(body_parts)}{term_panel_html}'
        f'<div id="nav"><button onclick="show(current-1)">&#8592;</button>'
        f'<span id="counter">1 / {n}</span><button onclick="show(current+1)">&#8594;</button></div>'
        f'<script>{js}</script></body></html>'
    )

    with open(out_deck_path, "w") as f:
        f.write(deck_html)

    presenter_html = None
    if out_presenter_path:
        deckname = out_deck_path.split("/")[-1]
        notes_html_list = [render_notes(notes, i) for i, (_, _, notes) in enumerate(slides)]
        presenter_html = build_presenter_html(
            title=title, deckname=deckname, notes_html_list=notes_html_list,
            budget_min=presenter_budget_min, sync_channel=sync_channel, fonts_css=fonts_css,
        )
        with open(out_presenter_path, "w") as f:
            f.write(presenter_html)

    return deck_html, presenter_html

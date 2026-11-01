#!/usr/bin/env python3
"""Minimal end-to-end example: no customer data, demonstrates the standard
control suite with the terminal panel ON and narration OFF. Run:

    python3 examples/build_example.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chassis import build_deck

NOTES = {
    "title": "[Open on the room] «SCRIPT»",
    "thesis": "«SCRIPT»",
    "demo": "{Recorded, not live} «SCRIPT»",
    "close": "[Stop talking. Let it sit.]",
}


def render_notes(raw, index):
    import re
    import html as H
    out = []
    for m in re.finditer(r'\[([^\]]+)\]|\{([^}]+)\}|«SCRIPT»|([^\[{«]+)', raw):
        if m.group(1):
            out.append(f'<div class="do">{H.escape(m.group(1).strip())}</div>')
        elif m.group(2):
            out.append(f'<div class="cue">{H.escape(m.group(2).strip())}</div>')
        elif m.group(0) == '«SCRIPT»':
            out.append(f'<div class="say">{SCRIPT[index]}</div>')
        elif m.group(3) and m.group(3).strip():
            out.append(f'<div class="say">{H.escape(m.group(3).strip())}</div>')
    return ''.join(out)


SCRIPT = [
    "Good afternoon. Thanks for being here.",
    "Here's the thesis for today's talk.",
    "Let's look at the capability live.",
    "That's the talk. Questions.",
]

SLIDES = [
    ("title", dict(eyebrow="Example Track · Example Venue · 2026",
                   title="A Deck Built on the Chassis",
                   sub="Same controls, every deck.",
                   people=[("Presenter Name", "Role, Organization")]), "title"),
    ("thesis", dict(kicker="The thesis", head="State it plainly.<br>Then show the <em>evidence</em>.",
                    pts=["One claim per deck.", "Evidence before argument.", "A demo beats a slide."]), "thesis"),
    ("demo", dict(badge="Live demo", name="Terminal panel", term="demo1",
                  what="Press T to open the terminal panel for this slide.",
                  chk=["about 1 minute", "press T", "press T again to close"]), "demo"),
    ("close", dict(head="That's the chassis.<br>One source, every control.",
                   punch="Press T. Press N. Press M.", foot="chassis v1"), "close"),
]

LOGO_HTML = '<div class="logo">EXAMPLE</div>'

if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    build_deck(
        SLIDES,
        title="Chassis Example Deck",
        footer_text="Example Org · Example Track 2026",
        logo_html=LOGO_HTML,
        fonts_css="",  # use system fonts for the example; real decks embed brand fonts here
        render_notes=render_notes,
        out_deck_path=os.path.join(out_dir, "present-example.html"),
        out_presenter_path=os.path.join(out_dir, "present-example-presenter.html"),
        sync_channel="chassis-example-sync",
        terminal={"demo_hosts": {"demo1": {"url": "about:blank", "label": "example terminal target"}}},
        presenter_budget_min=5,
    )
    print("wrote present-example.html and present-example-presenter.html")

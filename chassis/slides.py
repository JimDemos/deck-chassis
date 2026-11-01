"""Standard slide-type library.

Each slide is a (type, fields, notes) tuple. `render(slide_type, fields)` returns
the inner HTML for that slide's <div class="slide s-{type}">...</div>. Adding a
new slide type means adding one function here and one CSS block in css.py --
content never touches the chassis.
"""


def title(f):
    people = ''.join(
        f'<div><div class="pname">{p}</div><div class="prole">{r}</div></div>'
        for p, r in f.get("people", [])
    )
    return (
        f'<div class="eyebrow">{f["eyebrow"]}</div><h1>{f["title"]}</h1>'
        f'<div class="sub">{f["sub"]}</div><div class="people">{people}</div>'
    )


def thesis(f):
    pts = ''.join(f'<li>{p}</li>' for p in f["pts"])
    return f'<div class="kicker">{f["kicker"]}</div><h2>{f["head"]}</h2><ul class="pts">{pts}</ul>'


def timeline(f):
    rows = ''.join(f'<div class="d">{d}</div><div class="t">{t}</div>' for d, t in f["rows"])
    return f'<div class="kicker">{f["kicker"]}</div><h2>{f["head"]}</h2><div class="tl">{rows}</div>'


def twocol(f):
    l, r = f["left"], f["right"]
    return (
        f'<div class="kicker">{f["kicker"]}</div><h2>{f["head"]}</h2>'
        f'<div class="cols"><div class="col"><h3>{l[0]}</h3><p>{l[1]}</p></div>'
        f'<div class="col"><h3>{r[0]}</h3><p>{r[1]}</p></div></div>'
    )


def stat(f):
    stats = ''.join(f'<div class="stat"><div class="n">{a}</div><div class="l">{l}</div></div>' for a, l in f["stats"])
    return f'<div class="kicker">{f["kicker"]}</div><h2>{f["head"]}</h2><div class="stats">{stats}</div><div class="foot">{f["foot"]}</div>'


def grid(f):
    cells = ''.join(f'<div class="cell"><h3>{a}</h3><p>{t}</p></div>' for a, t in f["cells"])
    return f'<div class="kicker">{f["kicker"]}</div><h2>{f["head"]}</h2><div class="grid">{cells}</div>'


def layers(f):
    rows = ''.join(f'<div class="layer"><div class="n">{a}</div><div class="t">{t}</div></div>' for a, t in f["layers"])
    return f'<div class="kicker">{f["kicker"]}</div><h2>{f["head"]}</h2><div class="layers">{rows}</div>'


def model(f):
    cols = ''.join(f'<div class="col"><div class="tag">{a}</div><h3>{h}</h3><p>{t}</p></div>' for a, h, t in f["cols"])
    return f'<div class="kicker">{f["kicker"]}</div><h2>{f["head"]}</h2><div class="cols">{cols}</div>'


def demo(f):
    chks = ''.join(f'<div class="chk">{c}</div>' for c in f["chk"])
    return (
        f'<div class="badge">{f["badge"]}</div><div class="dname">{f["name"]}</div>'
        f'<div class="dwhat">{f["what"]}</div><div class="chks">{chks}</div>'
    )


def hack(f):
    nums = ''.join(f'<div class="hn"><div class="n">{a}</div><div class="l">{l}</div></div>' for a, l in f["nums"])
    html = (
        f'<div class="kicker">{f["layer"]} · {f["where"]}</div><h2>{f["name"]}</h2>'
        f'<div class="hk"><div class="hkl"><div class="hkt">How they got in</div><p>{f["vector"]}</p>'
        f'<div class="hkt">What failed</div><p>{f["failed"]}</p></div><div class="hkr">{nums}</div></div>'
    )
    if f.get("tl"):
        html += '<div class="htl">' + ''.join(
            f'<div class="hn2"><div class="dot"></div><div class="d">{d}</div><div class="t">{t}</div></div>'
            for d, t in f["tl"]
        ) + '</div>'
    return html


def recap(f):
    pts = ''.join(f'<li>{p}</li>' for p in f["pts"])
    return f'<div class="kicker">{f["verb"]}</div><h2>{f["head"]}</h2><ul class="pts">{pts}</ul>'


def teach(f):
    rows = ''.join(f'<div class="layer"><div class="n">{a}</div><div class="t">{t}</div></div>' for a, t in f["rows"])
    return (
        f'<div class="kicker">{f["kicker"]}</div><h2>{f["head"]}</h2>'
        f'<p class="lede">{f["lede"]}</p><div class="layers">{rows}</div>'
    )


def tie(f):
    l, r = f["left"], f["right"]
    return (
        f'<div class="kicker">{f["kicker"]}</div><h2>{f["head"]}</h2>'
        f'<div class="cols"><div class="col"><h3>{l[0]}</h3><p>{l[1]}</p></div>'
        f'<div class="col"><h3>{r[0]}</h3><p>{r[1]}</p></div></div>'
        f'<div class="foot" style="margin-top:1.6rem">{f["line"]}</div>'
    )


def wall(f):
    tiles = ''.join(
        f'<div class="tile{" lt" if lt else ""}">{logo_html}</div>'
        for logo_html, lt in f["tiles"]
    )
    return f'<div class="kicker">{f["kicker"]}</div><h2>{f["head"]}</h2><div class="wall">{tiles}</div><div class="wfoot">{f["foot"]}</div>'


def trend(f):
    hdr = ''.join(f'<div class="th">{c}</div>' for c in [""] + f["cols"])
    rows = ''.join(
        f'<div class="rl">{r[0]}</div>' + ''.join(f'<div class="rc">{c}</div>' for c in r[1:])
        for r in f["rows"]
    )
    return f'<div class="kicker">{f["kicker"]}</div><h2>{f["head"]}</h2><div class="trend">{hdr}{rows}</div>'


def close(f):
    return f'<div class="bar"></div><div class="q">{f["head"]}</div><div class="punch">{f["punch"]}</div><div class="foot">{f.get("foot","")}</div>'


RENDERERS = {
    "title": title, "thesis": thesis, "timeline": timeline, "twocol": twocol,
    "stat": stat, "grid": grid, "layers": layers, "model": model, "demo": demo,
    "hack": hack, "recap": recap, "teach": teach, "tie": tie, "wall": wall,
    "trend": trend, "close": close,
}


def render(slide_type, fields):
    fn = RENDERERS.get(slide_type)
    if fn is None:
        raise ValueError(f"unknown slide type: {slide_type!r} (known: {sorted(RENDERERS)})")
    return fn(fields)

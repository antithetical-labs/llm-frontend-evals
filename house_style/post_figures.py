"""Charts for the post.

Every panel here is faceted rather than colour-coded. The brand has exactly one
accent, so four models cannot honestly get four hues; each panel owns its data
in coral and carries the rest ghosted behind it for scale. Where a chart needs
ordered categories it uses the validated ramp from style.py, never invented hues.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .style import ACCENT, BG, HAIR, MONO, MUTED, PALETTES, RAMP, TEXT, use_brand

ROOT = Path(__file__).resolve().parent.parent
# Writes into the blog repo when POST_IMAGES_DIR points there, and into this
# repo otherwise, so a clone with no blog checked out still renders every figure.
OUT_DARK = Path(os.environ.get("POST_IMAGES_DIR", ROOT / "figures" / "post"))
# The light set never appears on the blog, which is dark only. It exists because
# the same PNG gets republished on a white page, where a figure saved with a
# near-black background arrives as a dark slab, so it stays in this repo.
OUT_LIGHT = Path(os.environ.get("POST_IMAGES_LIGHT_DIR",
                                ROOT / "figures" / "post-light"))
OUT = OUT_DARK

MODELS = ["claude", "gpt", "kimi", "gemini"]
BRIEF_LABEL = {"streamforge": "dev tool", "backlot": "back-office tool"}

# Read from the stylesheet source, because these are CSS features: either the
# declaration is there or it is not, and the rendered pixel cannot tell you
# whether a flat fill was authored as a gradient.
# The dingbat and emoji rows are deliberately separate. Lumping them under one
# "emoji" pattern put the rate at 49% of pages, and 90% of those matches were a
# checkmark: the interesting, common thing is ✓ and ✦, while an actual
# pictograph is rare. One row would have reported the tick's frequency under the
# rocket's name.
SOURCE_TELLS = {
    "gradient": r"linear-gradient|radial-gradient|conic-gradient",
    "frosted glass": r"backdrop-filter\s*:\s*[^;]*blur",
    "pill button": r"border-radius\s*:\s*(9999|999|100)px|border-radius\s*:\s*50rem",
    "glow shadow": r"box-shadow[^;]*0\s+0\s+\d+",
    "dingbat (✓ ✦)": r"[☀-➿]",
    "emoji": r"[\U0001F300-\U0001FAFF]",
}


def load() -> list[dict]:
    rows = []
    src = {p.stem: p.read_text() for p in (ROOT / "pages").glob("*.html")}
    for line in (ROOT / "styles.jsonl").read_text().splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        r["model"], r["brief"], r["cond"], r["run"] = r["name"].split("__")
        text = src.get(r["name"], "")
        for name, pattern in SOURCE_TELLS.items():
            r[name] = bool(re.search(pattern, text))
        r["eyebrow label"] = r["eyebrows"] > 0
        r["numbered markers"] = r["numbered_markers"] > 0
        # Both public checklists name a blue/indigo/purple accent specifically,
        # so it gets measured as its own claim rather than folded into "colour".
        h = r.get("accent_H")
        r["blue / purple accent"] = h is not None and 240 <= h < 330
        rows.append(r)
    return rows


def rate(pool: list[dict], key: str) -> float:
    return sum(1 for r in pool if r[key]) / len(pool) if pool else float("nan")


def use_theme(mode: str) -> None:
    """Point every chart function at the `mode` palette and output directory.

    The functions read the tokens as module globals rather than taking a theme
    argument, so the switch is a rebind here. The alternative is threading one
    parameter through sixteen call sites for a value that is constant across a
    whole render pass.
    """
    global ACCENT, BG, HAIR, MUTED, RAMP, TEXT, OUT
    p = PALETTES[mode]
    ACCENT, BG, HAIR, MUTED, RAMP, TEXT = (
        p["ACCENT"], p["BG"], p["HAIR"], p["MUTED"], p["RAMP"], p["TEXT"])
    OUT = OUT_DARK if mode == "dark" else OUT_LIGHT
    use_brand(mode)


def _finish(fig, out: Path) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor=BG, bbox_inches="tight")
    plt.close(fig)
    return out


# --------------------------------------------------------------------------
def fig_genre(rows: list[dict]) -> Path:
    """Background lightness per page, split by product type.

    A strip rather than a bar: the claim is about how tightly twenty
    independent runs cluster, and a mean would hide exactly that.
    """
    bare = [r for r in rows if r["cond"] == "bare"]
    fig, axes = plt.subplots(2, 1, figsize=(9, 3.4), sharex=True)

    for ax, brief in zip(axes, ["streamforge", "backlot"]):
        ax.set_facecolor(BG)
        for mi, model in enumerate(MODELS):
            pts = [r["bg_L"] for r in bare
                   if r["brief"] == brief and r["model"] == model]
            ax.plot(pts, [mi] * len(pts), "o", color=ACCENT, markersize=7,
                    markeredgecolor=BG, markeredgewidth=1.2, alpha=0.85)
        ax.set_yticks(range(len(MODELS)))
        ax.set_yticklabels(MODELS, color=TEXT, fontsize=9)
        ax.set_ylim(-0.7, len(MODELS) - 0.3)
        ax.invert_yaxis()
        ax.set_title(BRIEF_LABEL[brief], color=TEXT, fontsize=10, loc="left", pad=6)
        ax.grid(True, axis="x", color=HAIR, lw=0.4)
        ax.set_axisbelow(True)
        for s in ax.spines.values():
            s.set_color(HAIR)

    axes[-1].set_xlim(0, 1)
    axes[-1].set_xlabel("background lightness   (0 = black, 1 = white)",
                        color=MUTED, fontsize=8)
    axes[-1].set_xticks([0, 0.25, 0.5, 0.75, 1])
    for ax in axes:
        for lbl in ax.get_xticklabels():
            lbl.set(**MONO)
    fig.suptitle("Every page, no design instruction given",
                 color=TEXT, fontsize=12, x=0.125, ha="left", y=1.02)
    return _finish(fig, OUT / "chart-genre.png")


# --------------------------------------------------------------------------
def fig_fingerprint(rows: list[dict]) -> Path:
    """Per-model rate for each pattern, against the four-model average.

    Faceted because the accent cannot be split four ways. The ghost bar behind
    each panel is the same in every panel, so a short coral bar against a long
    ghost reads as "this model does not do that" without a second hue.
    """
    bare = [r for r in rows if r["cond"] == "bare"]
    patterns = ["gradient", "pill button", "frosted glass", "glow shadow",
                "dingbat (✓ ✦)", "emoji", "eyebrow label", "numbered markers"]
    overall = {p: rate(bare, p) for p in patterns}
    y = np.arange(len(patterns))

    fig, axes = plt.subplots(1, 4, figsize=(10, 3.1), sharey=True)
    for ax, model in zip(axes, MODELS):
        g = [r for r in bare if r["model"] == model]
        ax.set_facecolor(BG)
        ax.barh(y, [overall[p] for p in patterns], height=0.62,
                color=HAIR, zorder=1)
        ax.barh(y, [rate(g, p) for p in patterns], height=0.34,
                color=ACCENT, zorder=2)
        ax.set_title(f"{model}   n={len(g)}", color=TEXT, fontsize=9,
                     loc="left", pad=6)
        ax.set_xlim(0, 1)
        ax.set_xticks([0, 0.5, 1])
        ax.set_xticklabels(["0", "50", "100%"], **MONO)
        ax.tick_params(colors=MUTED, labelsize=7)
        ax.grid(True, axis="x", color=HAIR, lw=0.4)
        ax.set_axisbelow(True)
        for s in ax.spines.values():
            s.set_color(HAIR)

    axes[0].set_yticks(y)
    axes[0].set_yticklabels(patterns, color=TEXT, fontsize=9)
    axes[0].invert_yaxis()

    handles = [plt.Rectangle((0, 0), 1, 1, color=ACCENT),
               plt.Rectangle((0, 0), 1, 1, color=HAIR)]
    fig.legend(handles, ["this model", "all four models"], loc="lower center",
               ncol=2, frameon=False, labelcolor=TEXT, fontsize=8,
               bbox_to_anchor=(0.5, -0.09))
    fig.suptitle("Which patterns each model reaches for on its own",
                 color=TEXT, fontsize=12, x=0.02, ha="left", y=1.04)
    return _finish(fig, OUT / "chart-fingerprint.png")


# --------------------------------------------------------------------------
def fig_tells(rows: list[dict]) -> Path:
    """The published slop checklists, scored against what the pages do.

    "Named" means the pattern appears on one of the two public lists this is
    checked against (pbakaus/impeccable and the MindStudio design-system post),
    not that it is generally talked about. Anything measured here that they do
    not name is the interesting half.
    """
    bare = [r for r in rows if r["cond"] == "bare"]
    measured = [
        ("gradient", rate(bare, "gradient"), True),
        ("pill / rounded-full", rate(bare, "pill button"), True),
        ("glassmorphism", rate(bare, "frosted glass"), True),
        ("shadow / glow", rate(bare, "glow shadow"), True),
        ("blue or purple accent", rate(bare, "blue / purple accent"), True),
        ("eyebrow label", rate(bare, "eyebrow label"), False),
        ("dingbat (✓ ✦)", rate(bare, "dingbat (✓ ✦)"), False),
        ("numbered markers", rate(bare, "numbered markers"), False),
        ("emoji", rate(bare, "emoji"), False),
        ("serif headline", sum(1 for r in bare
                               if r["heading_font"] == "serif") / len(bare), False),
    ]
    measured.sort(key=lambda t: t[1])
    labels = [m[0] for m in measured]
    values = [m[1] for m in measured]
    named = [m[2] for m in measured]
    y = np.arange(len(labels))

    fig, ax = plt.subplots(figsize=(9, 3.6))
    ax.set_facecolor(BG)
    # Two ordered groups, so two steps of the validated ramp rather than two
    # invented hues. The checklist group is the darker step.
    colors = [RAMP[0] if flag else ACCENT for flag in named]
    ax.barh(y, values, height=0.6, color=colors)
    for yi, v in zip(y, values):
        ax.text(v + 0.015, yi, f"{v:.0%}", va="center", color=TEXT,
                fontsize=9, **MONO)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, color=TEXT, fontsize=9)
    ax.set_xlim(0, 1.08)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1])
    ax.set_xticklabels(["0", "25", "50", "75", "100%"], **MONO)
    ax.tick_params(colors=MUTED, labelsize=8)
    ax.grid(True, axis="x", color=HAIR, lw=0.4)
    ax.set_axisbelow(True)
    for s in ax.spines.values():
        s.set_color(HAIR)

    handles = [plt.Rectangle((0, 0), 1, 1, color=RAMP[0]),
               plt.Rectangle((0, 0), 1, 1, color=ACCENT)]
    ax.legend(handles, ["on the published checklists", "on neither"],
              loc="lower right", frameon=False, labelcolor=TEXT, fontsize=8)
    ax.set_title("The slop checklists, scored against 40 untouched pages",
                 color=TEXT, fontsize=12, loc="left", pad=10)
    return _finish(fig, OUT / "chart-tells.png")


# --------------------------------------------------------------------------
def fig_nudge(rows: list[dict]) -> Path:
    """What one line of 'avoid generic AI aesthetics' moves, and what it does not."""
    bare = [r for r in rows if r["cond"] == "bare"]
    nudge = [r for r in rows if r["cond"] == "nudge"]
    metrics = ["pill button", "frosted glass", "dingbat (✓ ✦)", "glow shadow",
               "gradient", "eyebrow label", "numbered markers"]
    pairs = [(m, rate(bare, m), rate(nudge, m)) for m in metrics]
    pairs.sort(key=lambda t: t[2] - t[1])
    y = np.arange(len(pairs))

    fig, (ax, ax2) = plt.subplots(
        1, 2, figsize=(10.5, 3.4),
        gridspec_kw={"width_ratios": [2.1, 1], "wspace": 0.34})

    ax.set_facecolor(BG)
    for yi, (_, b, n) in zip(y, pairs):
        ax.plot([b, n], [yi, yi], "-", color=HAIR, lw=1.4, zorder=1)
        ax.plot(b, yi, "o", color=MUTED, markersize=7, zorder=2,
                markeredgecolor=BG, markeredgewidth=1.2)
        ax.plot(n, yi, "o", color=ACCENT, markersize=7, zorder=3,
                markeredgecolor=BG, markeredgewidth=1.2)
        # The delta sits in a reserved gutter past the 100% tick rather than
        # beside its own dot, so the column reads down as its own list.
        ax.text(1.06, yi, f"{n - b:+.0%}", va="center", color=MUTED,
                fontsize=8, **MONO)
    ax.set_yticks(y)
    ax.set_yticklabels([p[0] for p in pairs], color=TEXT, fontsize=9)
    ax.invert_yaxis()
    ax.set_xlim(0, 1.28)
    ax.set_xticks([0, 0.5, 1])
    ax.set_xticklabels(["0", "50", "100%"], **MONO)
    ax.tick_params(colors=MUTED, labelsize=8)
    ax.grid(True, axis="x", color=HAIR, lw=0.4)
    ax.set_axisbelow(True)
    handles = [plt.Rectangle((0, 0), 1, 1, color=MUTED),
               plt.Rectangle((0, 0), 1, 1, color=ACCENT)]
    ax.legend(handles, ["untouched", "after the nudge"], loc="lower left",
              frameon=False, labelcolor=TEXT, fontsize=8)
    ax.set_title("The surface treatment comes off", color=TEXT, fontsize=10,
                 loc="left", pad=8)
    for s in ax.spines.values():
        s.set_color(HAIR)

    # The counter-panel: the looks themselves are still the same three.
    ATT = ["1-cream-serif-terracotta", "2-near-black-bright-accent",
           "3-broadsheet-hairline", "other"]
    SHORT = ["cream / serif", "dark / neon", "broadsheet", "none of the three"]
    steps = [RAMP[4], RAMP[3], RAMP[1], HAIR]
    ax2.set_facecolor(BG)
    for xi, (label, pool) in enumerate([("untouched", bare), ("nudged", nudge)]):
        bottom = 0
        for a, colour in zip(ATT, steps):
            n = sum(1 for r in pool if r["attractor"] == a)
            if not n:
                continue
            ax2.bar(xi, n, width=0.52, bottom=bottom, color=colour,
                    edgecolor=BG, linewidth=1.4)
            bottom += n
    ax2.set_xticks([0, 1])
    ax2.set_xticklabels(["untouched", "nudged"], color=TEXT, fontsize=9)
    ax2.set_ylabel("pages", color=MUTED, fontsize=8)
    ax2.tick_params(colors=MUTED, labelsize=8)
    ax2.set_title("but the mix just shuffles", color=TEXT, fontsize=10,
                  loc="left", pad=8)
    for s in ax2.spines.values():
        s.set_color(HAIR)
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in steps]
    ax2.legend(handles, SHORT, loc="upper center", bbox_to_anchor=(0.5, -0.14),
               ncol=2, frameon=False, labelcolor=TEXT, fontsize=7.5)

    fig.suptitle('"Avoid generic AI aesthetics. Make it distinctive."',
                 color=TEXT, fontsize=12, x=0.02, ha="left", y=1.03)
    return _finish(fig, OUT / "chart-nudge.png")


# --------------------------------------------------------------------------
# Two figures are screenshots rather than charts, because the claim is about
# what the page looks like and no measurement substitutes for showing it.

def _plate(cells: list[tuple[str, Path]], title: str, out: Path,
           cell_w: int, cell_h: int) -> Path:
    """Screenshots laid out in one row, at a size worth actually looking at."""
    from PIL import Image, ImageDraw, ImageFont

    from .sheets import FONT_DIR

    pad, label_h = 16, 26

    def font(size: int, mono: bool = True):
        name = "jetbrainsmono-400.ttf" if mono else "archivo-500.ttf"
        try:
            return ImageFont.truetype(str(FONT_DIR / name), size)
        except OSError:
            return ImageFont.load_default()

    width = len(cells) * cell_w + (len(cells) + 1) * pad
    height = cell_h + label_h + 2 * pad + 40
    canvas = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(canvas)
    draw.text((pad, 12), title, fill=TEXT, font=font(19, mono=False))

    for i, (label, path) in enumerate(cells):
        x = pad + i * (cell_w + pad)
        y = 40 + pad
        draw.text((x, y), label, fill=MUTED, font=font(12))
        box = (x, y + label_h, x + cell_w, y + label_h + cell_h)
        im = Image.open(path).convert("RGB")
        crop = im.crop((0, 0, im.width, min(im.height,
                                            int(im.width * cell_h / cell_w))))
        canvas.paste(crop.resize((cell_w, cell_h), Image.LANCZOS), box[:2])
        draw.rectangle(box, outline=HAIR, width=1)

    OUT.mkdir(parents=True, exist_ok=True)
    # Screenshot plates are the only figures big enough to matter: truecolour
    # they run past the 400 KB per-image budget the blog holds itself to. These
    # are flat UI captures, so an adaptive 256-colour palette is visually free
    # and cuts them by roughly two thirds. The charts are already tiny and are
    # left alone.
    canvas.quantize(colors=256, method=Image.MEDIANCUT,
                    dither=Image.FLOYDSTEINBERG).save(out, optimize=True)
    return out


def fig_banned_vs_not(rows: list[dict]) -> Path:
    """Every measured pattern, before and after four of them are banned.

    Answers: does banning a pattern remove it, and what happens to the ones you
    did not name? The split by whether a pattern was named is the whole
    argument, so that split carries the colour, and it is repeated in the row
    label so the chart survives greyscale and colour-vision deficiency.
    """
    bare = [r for r in rows if r["cond"] == "bare"]
    forb = [r for r in rows if r["cond"] == "forbid"]

    # The prohibition names exactly these four. Everything else is untouched by
    # the instruction and free to do whatever it was going to do anyway.
    BANNED = {"gradient", "frosted glass", "pill button", "dark background"}

    def pair(name):
        if name == "dark background":
            f = lambda pool: sum(1 for r in pool if r["bg_L"] < 0.30) / len(pool)
            return f(bare), f(forb)
        return rate(bare, name), rate(forb, name)

    names = ["gradient", "pill button", "frosted glass", "dark background",
             "glow shadow", "dingbat (✓ ✦)", "emoji", "eyebrow label",
             "numbered markers"]
    data = []
    for n in names:
        b, f = pair(n)
        data.append((n, b, f, n in BANNED))
    data.sort(key=lambda t: t[2] - t[1])

    y = np.arange(len(data))
    fig, ax = plt.subplots(figsize=(9, 4.0))
    ax.set_facecolor(BG)
    for i, (n, b, f, banned) in enumerate(data):
        colour = RAMP[0] if banned else ACCENT
        ax.plot([b, f], [i, i], "-", color=HAIR, lw=1.5, zorder=1)
        ax.plot(b, i, "o", color=MUTED, markersize=7, zorder=2,
                markeredgecolor=BG, markeredgewidth=1.2)
        ax.plot(f, i, "o", color=colour, markersize=8, zorder=3,
                markeredgecolor=BG, markeredgewidth=1.2)
        ax.text(1.05, i, f"{(f - b) * 100:+.0f}", va="center", color=MUTED,
                fontsize=8, **MONO)

    ax.set_yticks(y)
    ax.set_yticklabels([f"{n}  ·  BANNED" if bn else n
                        for n, _, _, bn in data], color=TEXT, fontsize=9)
    ax.invert_yaxis()
    ax.set_xlim(0, 1.22)
    ax.set_xticks([0, 0.5, 1])
    ax.set_xticklabels(["0", "50", "100%"], **MONO)
    ax.set_xlabel("share of pages carrying the pattern", color=MUTED,
                  fontsize=8, labelpad=8)
    ax.tick_params(colors=MUTED, labelsize=8)
    ax.grid(True, axis="x", color=HAIR, lw=0.4)
    ax.set_axisbelow(True)
    for s in ax.spines.values():
        s.set_color(HAIR)
    handles = [plt.Rectangle((0, 0), 1, 1, color=MUTED),
               plt.Rectangle((0, 0), 1, 1, color=RAMP[0]),
               plt.Rectangle((0, 0), 1, 1, color=ACCENT)]
    ax.legend(handles,
              ["untouched", "after the ban, named", "after the ban, not named"],
              loc="upper center", bbox_to_anchor=(0.5, -0.18), ncol=3,
              frameon=False, labelcolor=TEXT, fontsize=8)
    ax.set_title("Only what you name goes to zero",
                 color=TEXT, fontsize=12, loc="left", pad=10)
    fig.text(0.125, -0.22,
             "40 untouched pages, 39 forbidden  ·  change in percentage "
             "points  ·  llm-frontend-evals", color=MUTED, fontsize=7.5,
             **MONO)
    return _finish(fig, OUT / "chart-banned-vs-not.png")


def fig_clusters(rows: list[dict]) -> Path:
    """Whether patterns arrive independently or in bundles.

    Answers: is a design attractor one feature or a package? Phi over the
    untouched pages, with each brief's own value shown beside the pooled one,
    because the obvious objection is that any co-occurrence is really the
    product category showing through. It is not: the within-brief values are as
    strong or stronger.
    """
    bare = [r for r in rows if r["cond"] == "bare"]
    for r in bare:
        r["dark bg"] = r["bg_L"] < 0.30
    feats = ["gradient", "frosted glass", "pill button", "glow shadow",
             "dingbat (✓ ✦)", "emoji", "eyebrow label", "numbered markers",
             "dark bg"]

    def phi(pool, a, b):
        n = len(pool)
        n11 = sum(1 for r in pool if r[a] and r[b])
        n10 = sum(1 for r in pool if r[a] and not r[b])
        n01 = sum(1 for r in pool if not r[a] and r[b])
        n00 = n - n11 - n10 - n01
        den = ((n11 + n10) * (n01 + n00) * (n11 + n01) * (n10 + n00)) ** 0.5
        return (n11 * n00 - n10 * n01) / den if den else float("nan")

    sf = [r for r in bare if r["brief"] == "streamforge"]
    bl = [r for r in bare if r["brief"] == "backlot"]
    scored = sorted(((phi(bare, a, b), a, b)
                     for i, a in enumerate(feats) for b in feats[i + 1:]),
                    key=lambda t: -t[0])[:8]

    y = np.arange(len(scored))
    fig, ax = plt.subplots(figsize=(9, 3.6))
    ax.set_facecolor(BG)
    for i, (v, a, b) in enumerate(scored):
        for pool in (sf, bl):
            w = phi(pool, a, b)
            if w == w:
                ax.plot(w, i, "o", color=HAIR, markersize=6, zorder=2)
        ax.plot(v, i, "o", color=ACCENT, markersize=9, zorder=3,
                markeredgecolor=BG, markeredgewidth=1.3)
        ax.text(1.02, i, f"{v:+.2f}", va="center", color=MUTED, fontsize=8,
                **MONO)

    ax.set_yticks(y)
    ax.set_yticklabels([f"{a}  +  {b}" for _, a, b in scored],
                       color=TEXT, fontsize=9)
    ax.invert_yaxis()
    ax.set_xlim(0, 1.16)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xticklabels(["0", "0.25", "0.50", "0.75", "1"], **MONO)
    ax.set_xlabel("phi correlation between the two patterns  (0 = independent)",
                  color=MUTED, fontsize=8, labelpad=8)
    ax.tick_params(colors=MUTED, labelsize=8)
    ax.grid(True, axis="x", color=HAIR, lw=0.4)
    ax.set_axisbelow(True)
    for s in ax.spines.values():
        s.set_color(HAIR)
    handles = [plt.Rectangle((0, 0), 1, 1, color=ACCENT),
               plt.Rectangle((0, 0), 1, 1, color=HAIR)]
    ax.legend(handles, ["all untouched pages", "within one brief"],
              loc="upper center", bbox_to_anchor=(0.5, -0.24), ncol=2,
              frameon=False, labelcolor=TEXT, fontsize=8)
    ax.set_title("Patterns are correlated, not independent",
                 color=TEXT, fontsize=12, loc="left", pad=10)
    fig.text(0.125, -0.30,
             "40 untouched pages  ·  eight strongest pairs of 36  ·  "
             "llm-frontend-evals", color=MUTED, fontsize=7.5, **MONO)
    return _finish(fig, OUT / "chart-clusters.png")


def fig_grounding(rows: list[dict] | None = None) -> Path:
    """What the models say the direction means, before they build anything.

    Answers: does one sentence of direction land on a shared idea, or does each
    model invent its own? Read from the grounding turn, which is prose written
    before any markup exists, so this is the model's understanding rather than
    its output.
    """
    import re
    docs = [p.read_text().lower()
            for p in sorted((ROOT / "grounding").glob("*direct*.md"))]
    terms = [("rave", r"rave"), ("flyer", r"flyer"),
             ("monospace", r"monospace|mono type"), ("toxic", r"toxic"),
             ("Y2K", r"y2k"), ("chrome", r"chrome"), ("magenta", r"magenta"),
             ("the nineties", r"nineties|1990s|\b90s\b"),
             ("glitch", r"glitch"), ("brutalism", r"brutalis"),
             ("cyber-", r"cyber"), ("warped type", r"warped|distort")]
    counts = sorted(((sum(1 for d in docs if re.search(p, d)), n)
                     for n, p in terms), key=lambda t: t[0])
    y = np.arange(len(counts))

    fig, ax = plt.subplots(figsize=(9, 3.6))
    ax.set_facecolor(BG)
    ax.barh(y, [c for c, _ in counts], height=0.6, color=ACCENT)
    for i, (c, _) in enumerate(counts):
        ax.text(c + 0.5, i, f"{c}", va="center", color=TEXT, fontsize=9, **MONO)
    ax.set_yticks(y)
    ax.set_yticklabels([n for _, n in counts], color=TEXT, fontsize=9)
    ax.set_xlim(0, len(docs) + 3)
    ax.set_xticks([0, 10, 20, 30, 40])
    ax.set_xticklabels(["0", "10", "20", "30", "40"], **MONO)
    ax.set_xlabel(f"grounding documents mentioning the term  (of {len(docs)})",
                  color=MUTED, fontsize=8, labelpad=8)
    ax.tick_params(colors=MUTED, labelsize=8)
    ax.grid(True, axis="x", color=HAIR, lw=0.4)
    ax.set_axisbelow(True)
    for s in ax.spines.values():
        s.set_color(HAIR)
    ax.set_title("Four models, one sentence, the same art history",
                 color=TEXT, fontsize=12, loc="left", pad=10)
    fig.text(0.125, -0.14,
             "written before any markup exists  ·  median 717 words each  ·  "
             "llm-frontend-evals", color=MUTED, fontsize=7.5, **MONO)
    return _finish(fig, OUT / "chart-grounding.png")


def _rows_plate(rows_of_cells, title: str, out: Path,
                cell_w: int, cell_h: int) -> Path:
    """Several labelled rows of screenshots, for a before/after contrast."""
    from PIL import Image, ImageDraw, ImageFont

    from .sheets import FONT_DIR

    pad, label_h, head = 16, 26, 44

    def font(size: int, mono: bool = True):
        name = "jetbrainsmono-400.ttf" if mono else "archivo-500.ttf"
        try:
            return ImageFont.truetype(str(FONT_DIR / name), size)
        except OSError:
            return ImageFont.load_default()

    cols = max(len(r["cells"]) for r in rows_of_cells)
    width = cols * cell_w + (cols + 1) * pad
    height = head + sum(cell_h + label_h + pad for _ in rows_of_cells) + pad
    canvas = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(canvas)
    draw.text((pad, 13), title, fill=TEXT, font=font(19, mono=False))

    y = head
    for row in rows_of_cells:
        draw.text((pad, y), row["label"], fill=MUTED, font=font(12))
        for i, (cap, path) in enumerate(row["cells"]):
            x = pad + i * (cell_w + pad)
            box = (x, y + label_h, x + cell_w, y + label_h + cell_h)
            im = Image.open(path).convert("RGB")
            crop = im.crop((0, 0, im.width,
                            min(im.height, int(im.width * cell_h / cell_w))))
            canvas.paste(crop.resize((cell_w, cell_h), Image.LANCZOS), box[:2])
            draw.rectangle(box, outline=HAIR, width=1)
        y += cell_h + label_h + pad

    OUT.mkdir(parents=True, exist_ok=True)
    canvas.quantize(colors=256, method=Image.MEDIANCUT,
                    dither=Image.FLOYDSTEINBERG).save(out, optimize=True)
    return out


def fig_forbid_vs_direct() -> Path:
    """The same four models, told what not to do and told what to aim at."""
    from .sheets import SHOTS
    models = ["claude", "gpt", "kimi", "gemini"]

    def row(cond, label):
        return {"label": label,
                "cells": [(m, SHOTS / f"{m}__streamforge__{cond}__1.png")
                          for m in models]}

    return _rows_plate(
        [row("forbid", "four patterns banned by name"),
         row("direct", 'one sentence: "take the visual direction from acid '
                       'design", then grounded')],
        "Same brief, same four models, two kinds of instruction",
        OUT / "shot-forbid-vs-direct.png", cell_w=440, cell_h=300)


def fig_richness(rows: list[dict]) -> Path:
    """How much colour survives each instruction.

    Answers: what does each kind of instruction do to how much is actually on
    the page, for someone deciding how to prompt. Every page is a dot rather
    than a bar of the median, because the spread is the point: forbidding
    collapses it and direction widens it.
    """
    order = ["bare", "nudge", "forbid", "direct1", "direct"]
    label = {"bare": "nothing said", "nudge": '"be distinctive"',
             "forbid": "four patterns banned", "direct1": "direction",
             "direct": "direction + grounding"}
    fig, ax = plt.subplots(figsize=(9, 3.6))
    ax.set_facecolor(BG)

    rng = np.random.default_rng(0)   # jitter only, never a data value
    for i, cond in enumerate(order):
        vals = [r["chromatic_elements"] for r in rows if r["cond"] == cond]
        ax.plot(vals, i + rng.uniform(-0.16, 0.16, len(vals)), "o",
                color=HAIR, markersize=5, zorder=1)
        med = sorted(vals)[len(vals) // 2]
        ax.plot([med], [i], "o", color=ACCENT, markersize=11, zorder=3,
                markeredgecolor=BG, markeredgewidth=1.4)
        ax.text(med, i - 0.34, f"{med}", color=TEXT, fontsize=9,
                ha="center", **MONO)

    ax.set_yticks(range(len(order)))
    ax.set_yticklabels([label[c] for c in order], color=TEXT, fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel("coloured elements on the page", color=MUTED, fontsize=8,
                  labelpad=8)
    ax.tick_params(colors=MUTED, labelsize=8)
    for lbl in ax.get_xticklabels():
        lbl.set(**MONO)
    ax.grid(True, axis="x", color=HAIR, lw=0.4)
    ax.set_axisbelow(True)
    for s in ax.spines.values():
        s.set_color(HAIR)
    handles = [plt.Rectangle((0, 0), 1, 1, color=HAIR),
               plt.Rectangle((0, 0), 1, 1, color=ACCENT)]
    # Upper right: the two lightest rows carry no data past ~100, so the
    # legend sits in real empty space rather than over the bottom row's tail.
    ax.legend(handles, ["one page", "median"], loc="upper right",
              frameon=False, labelcolor=TEXT, fontsize=8)
    ax.set_title("Banning patterns empties the page; direction fills it",
                 color=TEXT, fontsize=12, loc="left", pad=10)
    fig.text(0.125, -0.09,
             "every page, both briefs, all four models  ·  n=39-40 per row  ·  "
             "llm-frontend-evals", color=MUTED, fontsize=7.5, **MONO)
    return _finish(fig, OUT / "chart-richness.png")


def fig_exemplar() -> Path:
    """One page carrying every pattern on the measured list at once."""
    from .sheets import SHOTS
    return _plate(
        [("claude · dev tool · nothing said about design",
          SHOTS / "claude__streamforge__bare__2.png")],
        "All seven patterns on one page", OUT / "shot-exemplar.png",
        cell_w=1180, cell_h=740)


def fig_bare_vs_nudge() -> Path:
    """Same model, same brief, one sentence of difference."""
    from .sheets import SHOTS
    return _plate(
        [("untouched", SHOTS / "claude__streamforge__bare__1.png"),
         ('+ "avoid generic AI aesthetics. make it distinctive."',
          SHOTS / "claude__streamforge__nudge__1.png")],
        "Claude, same brief, with and without the nudge",
        OUT / "shot-bare-vs-nudge.png", cell_w=900, cell_h=620)


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--mode", choices=["dark", "light", "both"], default="both")
    args = ap.parse_args()

    rows = load()
    modes = ["dark", "light"] if args.mode == "both" else [args.mode]
    for mode in modes:
        use_theme(mode)
        for build in (fig_genre, fig_fingerprint, fig_tells, fig_nudge,
                      fig_richness, fig_banned_vs_not,
                      fig_clusters, fig_grounding):
            print(f"wrote {mode}/{build(rows).name}")
        for shot_build in (fig_exemplar, fig_bare_vs_nudge, fig_forbid_vs_direct):
            print(f"wrote {mode}/{shot_build().name}")


if __name__ == "__main__":
    main()

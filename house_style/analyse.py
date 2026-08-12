"""Aggregate the measured pages into figures and a table.

Two design constraints shape every chart here.

The brand has exactly one accent hue, so a categorical palette does not exist to
be validated -- there is no honest way to give four models four hues. Every
comparison is therefore faceted: one panel per model, the panel's own data in
coral, everything else ghosted behind it for scale.

And hue is angular. Plotting it on a linear axis puts 355 degrees and 5 degrees
at opposite ends of the chart when they are neighbours, which would invent a
difference between two nearly identical reds. The accent chart is polar for that
reason, not for decoration.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from .style import ACCENT, BG, HAIR, MONO, MUTED, RAMP, TEXT, use_brand

ROOT = Path(__file__).resolve().parent.parent
STYLES = ROOT / "styles.jsonl"
RUNS = ROOT / "runs.jsonl"
FIGURES = ROOT / "figures"

MODEL_ORDER = ["claude", "gpt", "kimi", "gemini"]
COND_ORDER = ["bare", "nudge", "skill"]
ATTRACTORS = ["1-cream-serif-terracotta", "2-near-black-bright-accent",
              "3-broadsheet-hairline", "other", "unknown"]
ATTRACTOR_SHORT = {
    "1-cream-serif-terracotta": "1 cream/serif",
    "2-near-black-bright-accent": "2 dark/neon",
    "3-broadsheet-hairline": "3 broadsheet",
    "other": "other", "unknown": "unknown",
}


def load() -> list[dict]:
    if not STYLES.exists():
        raise SystemExit("no styles.jsonl - run house_style.extract first")
    rows = []
    for line in STYLES.read_text().splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        parts = r["name"].split("__")
        if len(parts) != 4:
            continue
        r["model_key"], r["brief"], r["condition"], r["run"] = parts
        rows.append(r)
    return rows


def table(rows: list[dict]) -> str:
    """The table-view twin: every figure's numbers, readable without colour."""
    out = [f"{'model':8} {'brief':11} {'cond':7} {'n':>3} "
           f"{'bg_L':>6} {'acc_H':>7} {'acc_C':>6} {'serif':>6} "
           f"{'eyebrow':>8} {'radius':>7}  attractors"]
    out.append("-" * len(out[0]))
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for r in rows:
        groups[(r["model_key"], r["brief"], r["condition"])].append(r)

    def med(vals):
        vals = [v for v in vals if v is not None]
        return sorted(vals)[len(vals) // 2] if vals else float("nan")

    for model in MODEL_ORDER:
        for brief in sorted({r["brief"] for r in rows}):
            for cond in COND_ORDER:
                g = groups.get((model, brief, cond))
                if not g:
                    continue
                att = Counter(ATTRACTOR_SHORT.get(x["attractor"], x["attractor"])
                              for x in g)
                serif = sum(1 for x in g if x.get("heading_font") == "serif")
                out.append(
                    f"{model:8} {brief:11} {cond:7} {len(g):>3} "
                    f"{med([x['bg_L'] for x in g]):6.3f} "
                    f"{med([x['accent_H'] for x in g]):7.1f} "
                    f"{med([x['accent_C'] for x in g]):6.3f} "
                    f"{serif:>3}/{len(g):<2} "
                    f"{med([x['eyebrows'] for x in g]):8.1f} "
                    f"{med([x['median_radius'] for x in g]):7.1f}  "
                    + ", ".join(f"{k}x{v}" for v, k in
                                sorted(((v, k) for k, v in att.items()),
                                       reverse=True)))
    return "\n".join(out)


def fig_accent_polar(rows: list[dict]) -> Path:
    """Where each model puts its accent, in hue-chroma space."""
    fig, axes = plt.subplots(1, len(MODEL_ORDER), figsize=(3.1 * len(MODEL_ORDER), 3.6),
                             subplot_kw={"projection": "polar"})
    allpts = [(math.radians(r["accent_H"]), r["accent_C"]) for r in rows
              if r.get("accent_H") is not None and r.get("accent_C")]
    cmax = max((c for _, c in allpts), default=0.3) * 1.1

    for ax, model in zip(np.atleast_1d(axes), MODEL_ORDER):
        pts = [(math.radians(r["accent_H"]), r["accent_C"]) for r in rows
               if r["model_key"] == model and r.get("accent_H") is not None
               and r.get("accent_C")]
        ax.set_facecolor(BG)
        for t, c in allpts:
            ax.plot(t, c, "o", color=HAIR, markersize=3, zorder=1)
        for t, c in pts:
            ax.plot(t, c, "o", color=ACCENT, markersize=5, zorder=3,
                    markeredgecolor=BG, markeredgewidth=0.6)
        ax.set_ylim(0, cmax)
        ax.set_yticklabels([])
        ax.set_xticks(np.radians([0, 90, 180, 270]))
        ax.set_xticklabels(["0°", "90°", "180°", "270°"], color=MUTED, fontsize=7)
        ax.tick_params(pad=1)
        ax.grid(color=HAIR, lw=0.4)
        ax.spines["polar"].set_color(HAIR)
        ax.set_title(f"{model}   n={len(pts)}", color=TEXT, fontsize=9, pad=12)

    fig.suptitle("Accent colour by model  ·  angle = hue, radius = chroma",
                 color=TEXT, fontsize=12, y=0.99)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    FIGURES.mkdir(exist_ok=True)
    out = FIGURES / "accent-polar.png"
    fig.savefig(out, facecolor=BG)
    plt.close(fig)
    return out


def fig_attractors(rows: list[dict]) -> Path:
    """Which documented look each model lands in, and whether the brief moves it."""
    briefs = sorted({r["brief"] for r in rows})
    fig, axes = plt.subplots(len(briefs), 1,
                             figsize=(9, 2.6 * len(briefs)), squeeze=False)
    present = [a for a in ATTRACTORS
               if any(r["attractor"] == a for r in rows)]
    # A one-hue ramp, not four hues. The attractors are ordered categories and
    # the brand has a single accent, so lightness carries the distinction --
    # this is the ramp already validated in style.py (one hue, monotone L,
    # visible step gaps, light end clears the surface).
    steps = list(reversed(RAMP))  # lightest first so "1" reads strongest
    shades = [steps[min(i, len(steps) - 1)] for i in range(len(present))]

    for bi, brief in enumerate(briefs):
        ax = axes[bi][0]
        ax.set_facecolor(BG)
        width = 0.8 / len(COND_ORDER)
        for ci, cond in enumerate(COND_ORDER):
            for mi, model in enumerate(MODEL_ORDER):
                g = [r for r in rows if r["model_key"] == model
                     and r["brief"] == brief and r["condition"] == cond]
                if not g:
                    continue
                bottom = 0
                x = mi + (ci - 1) * width
                for ai, a in enumerate(present):
                    n = sum(1 for r in g if r["attractor"] == a)
                    if not n:
                        continue
                    ax.bar(x, n, width=width * 0.86, bottom=bottom,
                           color=shades[ai], edgecolor=BG, linewidth=1.5)
                    bottom += n
                ax.text(x, bottom + 0.12, cond[0], ha="center", color=MUTED,
                        fontsize=7, **MONO)
        ax.set_xticks(range(len(MODEL_ORDER)))
        ax.set_xticklabels(MODEL_ORDER, color=TEXT, fontsize=9)
        ax.set_ylabel("pages", color=MUTED, fontsize=8)
        ax.set_title(f"{brief}   (b = bare, n = nudge, s = skill)",
                     color=TEXT, fontsize=10, loc="left", pad=8)
        ax.tick_params(colors=MUTED, labelsize=8)
        for s in ax.spines.values():
            s.set_color(HAIR)
        ax.grid(True, axis="y", color=HAIR, lw=0.4)
        ax.set_axisbelow(True)

    handles = [plt.Rectangle((0, 0), 1, 1, color=shades[i])
               for i in range(len(present))]
    fig.legend(handles, [ATTRACTOR_SHORT.get(a, a) for a in present],
               loc="lower center", ncol=len(present), frameon=False,
               labelcolor=TEXT, fontsize=8, bbox_to_anchor=(0.5, -0.01))
    fig.suptitle("Which documented AI-design look each model produces",
                 color=TEXT, fontsize=12, y=0.995)
    fig.tight_layout(rect=[0, 0.06, 1, 0.96])
    FIGURES.mkdir(exist_ok=True)
    out = FIGURES / "attractors.png"
    fig.savefig(out, facecolor=BG)
    plt.close(fig)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.parse_args()
    use_brand()
    rows = load()
    print(table(rows), "\n")
    print("wrote", fig_accent_polar(rows).name)
    print("wrote", fig_attractors(rows).name)


if __name__ == "__main__":
    main()

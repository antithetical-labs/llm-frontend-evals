"""Chart styling: brand tokens, a validated ramp, and the site's typefaces.

Colours come from DESIGN.md in the site repo, which is the single source of
truth -- they are OKLCH there and sRGB here, but nothing is invented.

The sequential ramp is validated, not eyeballed, and the validator is in this
repo so the claim can be rechecked rather than taken on faith:

    python scripts/validate_palette.py --ramp dark
    python scripts/validate_palette.py --ramp light
    -> ALL CHECKS PASS (one hue, monotone L, visible gaps, first step clears
       the surface)

The dark end deliberately sits *above* the page background rather than equal to
it. Zero-attention cells and the causal mask must not look the same: the mask is
"no data" and gets the surface, the lowest data step gets the ramp's first step.

Two modes, because a chart leaves the site. The blog is dark only, but the same
PNG gets republished on a white page, and a figure saved with a near-black
background lands there as a dark slab. The light mode is not an inversion: it is
the same hue 34 with every token re-derived at the same *distance* from its own
page colour, so a mark that recedes on the dark page also recedes on the white
one. Both sets go through the validator.
"""

from pathlib import Path

import matplotlib as mpl
from matplotlib import font_manager
from matplotlib.colors import LinearSegmentedColormap

ASSETS = Path(__file__).resolve().parent.parent / "assets" / "fonts"

# --- brand tokens (DESIGN.md, OKLCH -> sRGB) ------------------------------
# RAMP is the validated sequential ramp, hue locked to 34, for any
# ordinal/categorical use (tiers, buckets, discrete steps). Step 0 is the one
# nearest the page and is deliberately lifted off it, so the lowest *category*
# stays visible; that is what the validator's surface-clearance check protects.
PALETTES = {
    "dark": {
        "BG": "#0E0A09",       # --neutral-950, page background
        "SURFACE": "#171312",  # --neutral-900, raised surface
        "HAIR": "#3C3735",     # --neutral-600, hairline borders
        "MUTED": "#8C8482",    # --neutral-400, muted text (>=4.5:1 on bg)
        "TEXT": "#F4EDEB",     # --neutral-100, primary text
        "ACCENT": "#FF5732",   # --accent, coral (5.7:1 on bg)
        "RAMP": ["#6E372A", "#A3442F", "#DB5032",
                 "#FF6E4C", "#FFA287", "#FFD2BF"],
    },
    # Not on the site: this exists so a figure survives republication on a white
    # page. Pure white rather than a warm off-white, because the common hosts
    # (Substack, X, GitHub light) are #FFFFFF and a near-miss shows its seam.
    # The accent drops from L 0.68 to 0.62 for 4.0:1 on white; at the brand's own
    # lightness a 7px dot only reaches 3.15:1, which is the non-text floor with
    # nothing to spare. The hue does not move, so it still reads as the coral.
    "light": {
        "BG": "#FFFFFF",
        "SURFACE": "#F6F2F2",
        "HAIR": "#C6BFBD",
        "MUTED": "#716A68",    # 5.3:1 on bg
        "TEXT": "#191514",
        "ACCENT": "#E54723",
        "RAMP": ["#FBAE9C", "#F87153", "#D74321",
                 "#A32D12", "#701C08", "#410C03"],
    },
}

BG, SURFACE, HAIR, MUTED, TEXT, ACCENT, RAMP = (
    PALETTES["dark"][k]
    for k in ("BG", "SURFACE", "HAIR", "MUTED", "TEXT", "ACCENT", "RAMP")
)

# For the continuous heatmaps, the ramp is anchored at the background instead.
# This deliberately fails the validator's light-end contrast check, and the
# reason is that the check is aimed at discrete steps used as marks. In a causal
# attention map the upper triangle is structurally zero -- a token cannot attend
# to its own future -- so "no data" and "no attention" are the same statement and
# should look the same. Anchoring above the background instead made every
# near-zero cell glow, which read as attention that is not there. A chart that
# fails a check for a stated reason beats one that passes and misleads.
ATTN_CMAP = LinearSegmentedColormap.from_list("attn", [BG] + RAMP)
ATTN_CMAP.set_bad(BG)

# Attention is extremely peaked, so the colour scale is gamma-compressed. That
# is a real distortion and the colourbar must be tick-labelled with true values
# so nobody reads the picture as linear. 0.4 pushed 1% attention to 16% of the
# ramp, which was too much; 0.55 keeps the tail readable without inflating it.
GAMMA = 0.55


def use_brand(mode: str = "dark") -> None:
    """Register the site's typefaces and set global rcParams for `mode`."""
    p = PALETTES[mode]
    for ttf in ASSETS.glob("*.ttf"):
        font_manager.fontManager.addfont(str(ttf))

    have = {f.name for f in font_manager.fontManager.ttflist}
    sans = "Archivo" if "Archivo" in have else "DejaVu Sans"
    mono = "JetBrains Mono" if "JetBrains Mono" in have else "DejaVu Sans Mono"

    mpl.rcParams.update({
        "figure.facecolor": p["BG"],
        "savefig.facecolor": p["BG"],
        "axes.facecolor": p["BG"],
        "font.family": "sans-serif",
        "font.sans-serif": [sans, "DejaVu Sans"],
        # DESIGN.md assigns mono to labels, numbers and axis furniture.
        "font.monospace": [mono, "DejaVu Sans Mono"],
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "text.color": p["TEXT"],
        "axes.labelcolor": p["MUTED"],
        "axes.edgecolor": p["HAIR"],
        "xtick.color": p["MUTED"],
        "ytick.color": p["MUTED"],
        "axes.linewidth": 0.6,
        "grid.color": p["HAIR"],
        "grid.linewidth": 0.4,
        "grid.linestyle": "-",     # solid hairlines; dashed grids read as thresholds
        "axes.grid": False,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "legend.frameon": False,
        "figure.dpi": 150,
    })
    return {"sans": sans, "mono": mono}


MONO = {"family": "monospace"}

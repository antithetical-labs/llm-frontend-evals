"""Check an ordinal colour ramp against the four properties it has to hold.

This exists because style.py used to assert "ALL CHECKS PASS" next to a command
nobody could run: the validator it cited shipped with a bundled Claude Code
skill, was JavaScript, was never vendored here, and has since been deleted. An
unverifiable claim in a repo whose whole argument is "measure it" is worse than
no claim, so the check now lives with the thing it checks.

    python scripts/validate_palette.py --ramp dark
    python scripts/validate_palette.py --ramp light

Exits non-zero if any check fails, so it works in CI.
"""

from __future__ import annotations

import argparse
import math
import sys

# One hue by construction, so a step's position in the ramp is its only meaning.
# Step 0 is always the one nearest its own page, so the light ramp runs downhill
# in lightness where the dark one runs uphill.
RAMPS = {
    "dark": (["#6E372A", "#A3442F", "#DB5032",
              "#FF6E4C", "#FFA287", "#FFD2BF"], "#0E0A09"),
    "light": (["#FBAE9C", "#F87153", "#D74321",
               "#A32D12", "#701C08", "#410C03"], "#FFFFFF"),
}

# An ordinal ramp is read by comparing neighbours, so the binding constraints
# are that the hue never wanders, lightness moves one way and never doubles
# back, adjacent steps are far enough apart to be told apart, and the step
# closest to the page still reads as a mark rather than dissolving into it.
MAX_HUE_DRIFT = 12.0    # degrees across the whole ramp
MIN_STEP_DL = 0.06      # OKLCH lightness between neighbours
MIN_SURFACE_DL = 0.10   # step 0 against the page it sits on


def hex_to_rgb(s: str) -> tuple[float, float, float]:
    s = s.lstrip("#")
    if len(s) != 6:
        raise ValueError(f"not a 6-digit hex colour: #{s}")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def srgb_to_oklch(r: float, g: float, b: float) -> tuple[float, float, float]:
    """sRGB 0-255 -> (L, C, H degrees). Same space DESIGN.md is written in."""
    def lin(c):
        c /= 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = lin(r), lin(g), lin(b)
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = l ** (1 / 3), m ** (1 / 3), s ** (1 / 3)
    L = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    A = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    B = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_
    return L, math.hypot(A, B), math.degrees(math.atan2(B, A)) % 360


def circular_spread(hues: list[float]) -> float:
    """Widest gap between any two hues, the short way round the wheel."""
    return max(min(abs(a - b), 360 - abs(a - b)) for a in hues for b in hues)


def check(colours: list[str], surface: str) -> list[tuple[bool, str, str]]:
    lch = [srgb_to_oklch(*hex_to_rgb(c)) for c in colours]
    Ls = [c[0] for c in lch]
    Hs = [c[2] for c in lch]
    sL = srgb_to_oklch(*hex_to_rgb(surface))[0]
    results = []

    drift = circular_spread(Hs)
    results.append((drift <= MAX_HUE_DRIFT, "one hue",
                    f"hue spread {drift:.1f}deg, limit {MAX_HUE_DRIFT:.0f}"))

    # Direction is set by the page, not fixed: on a dark surface the ramp climbs
    # away from it and on a light one it descends. Either is monotone; a ramp
    # that doubles back is what makes two different values look the same.
    gaps = [b - a for a, b in zip(Ls, Ls[1:])]
    monotone = all(g > 0 for g in gaps) or all(g < 0 for g in gaps)
    results.append((monotone, "lightness is monotone",
                    f"{'increasing' if gaps and gaps[0] > 0 else 'decreasing'}"
                    if monotone else f"doubles back: {[round(x,3) for x in Ls]}"))

    smallest = min(abs(g) for g in gaps) if gaps else 0.0
    results.append((smallest >= MIN_STEP_DL, "steps are distinguishable",
                    f"smallest gap {smallest:.3f}, floor {MIN_STEP_DL}"))

    clearance = abs(Ls[0] - sL)
    results.append((clearance >= MIN_SURFACE_DL, "step 0 clears the surface",
                    f"dL {clearance:.3f} over {surface}, floor {MIN_SURFACE_DL}"))
    return results


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("colours", nargs="*", help="hex colours, step 0 first")
    ap.add_argument("--ramp", nargs="?", const="all", choices=["all", *RAMPS],
                    help="check a ramp from house_style/style.py")
    ap.add_argument("--surface", help="page colour the ramp is drawn on")
    args = ap.parse_args()

    if args.colours:
        if args.surface is None:
            ap.error("--surface is required with explicit colours")
        jobs = [("given", args.colours, args.surface)]
    else:
        wanted = list(RAMPS) if args.ramp in (None, "all") else [args.ramp]
        jobs = [(m, RAMPS[m][0], args.surface or RAMPS[m][1]) for m in wanted]

    failed = 0
    for name, colours, surface in jobs:
        print(f"{name}: {len(colours)} steps on {surface}: {' '.join(colours)}\n")
        results = check(colours, surface)
        for ok, label, detail in results:
            print(f"  {'PASS' if ok else 'FAIL'}  {label:32} {detail}")
        failed += sum(1 for r in results if not r[0])
        print()

    print("ALL CHECKS PASS" if not failed else f"{failed} CHECK(S) FAILED")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

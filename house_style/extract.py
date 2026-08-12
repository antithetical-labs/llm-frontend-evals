"""Render each page and measure what it actually looks like.

Computed styles from the live DOM, not the CSS source: cascade, inheritance and
shorthand all resolve before anything is counted, so a colour declared in one
place and overridden in another is read as the browser reads it.

What gets measured is chosen to match the claim under test. Anthropic's own
frontend-design skill names three attractors AI design falls into:

  1  warm cream background (near #F4F1EA), high-contrast serif display,
     terracotta accent
  2  near-black background, one bright acid-green or vermilion accent
  3  broadsheet: hairline rules, zero border-radius, dense columns

Those are palette *and* structure, so measuring colour alone would miss most of
it. The component vocabulary -- eyebrow labels, numbered markers, hairline rules,
corner rounding -- is measured too, because "it copies the eyebrows" is a claim
about components, not hue.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "pages"
SHOTS = ROOT / "shots"
STYLES = ROOT / "styles.jsonl"

VIEWPORT = {"width": 1440, "height": 900}

# Collected in-page: one pass over every element, reading resolved values.
PROBE = """
() => {
  const out = {elements: [], eyebrows: [], numbered: 0};
  const px = v => parseFloat(v) || 0;

  // Normalise any CSS colour to rgb() by rasterising one pixel.
  //
  // Computed styles preserve the authored colour space: a page written in
  // oklch() reports 'oklch(0.15 0.006 34)' back, and so does canvas
  // fillStyle, so a string round-trip through the canvas is a no-op. Painting
  // the colour and reading the pixel is the only thing that actually resolves
  // it, and it works for every syntax the browser supports -- oklch, oklab,
  // color(), hsl, hex, named -- without this file needing to know any of them.
  const cv = document.createElement('canvas');
  cv.width = cv.height = 1;
  const ctx = cv.getContext('2d', {willReadFrequently: true});
  const cache = new Map();
  const norm = v => {
    if (!v) return '';
    if (v.startsWith('rgb(')) return v;
    if (cache.has(v)) return cache.get(v);
    let res = v;
    try {
      ctx.clearRect(0, 0, 1, 1);
      ctx.fillStyle = v;
      ctx.fillRect(0, 0, 1, 1);
      const d = ctx.getImageData(0, 0, 1, 1).data;
      res = d[3] === 0
        ? 'rgba(0, 0, 0, 0)'
        : `rgba(${d[0]}, ${d[1]}, ${d[2]}, ${(d[3] / 255).toFixed(3)})`;
    } catch (e) { /* leave as-is; parse_rgb will reject it */ }
    cache.set(v, res);
    return res;
  };

  for (const el of document.querySelectorAll('body, body *')) {
    const cs = getComputedStyle(el);
    const rect = el.getBoundingClientRect();
    const area = rect.width * rect.height;
    const text = (el.textContent || '').trim();
    const tag = el.tagName.toLowerCase();

    out.elements.push({
      tag,
      area,
      color: norm(cs.color),
      background: norm(cs.backgroundColor),
      borderColor: norm(cs.borderTopColor),
      borderWidth: px(cs.borderTopWidth),
      radius: px(cs.borderTopLeftRadius),
      fontFamily: cs.fontFamily,
      fontSize: px(cs.fontSize),
      fontWeight: cs.fontWeight,
      letterSpacing: cs.letterSpacing,
      textTransform: cs.textTransform,
      hasOwnText: Array.from(el.childNodes).some(
        n => n.nodeType === 3 && n.textContent.trim().length > 0),
    });

    // Eyebrow: a small, letterspaced, upper-cased label sitting directly
    // above a heading. Detected structurally rather than by class name,
    // since class names are whatever the model felt like calling them.
    //
    // Site chrome is excluded. Nav links and footers are small, uppercase
    // and letterspaced too, and counting them turned a real site's 1 eyebrow
    // into 8. The next element must *be* a heading, not merely contain one
    // somewhere -- "the next section has an h2 in it" matches nearly
    // everything on a landing page.
    const ls = cs.letterSpacing === 'normal' ? 0 : px(cs.letterSpacing);
    const isUpper = cs.textTransform === 'uppercase' ||
      (text.length > 1 && text === text.toUpperCase() && /[A-Z]/.test(text));
    const inChrome = el.closest('nav, header, footer') !== null;
    if (!inChrome && text.length > 0 && text.length < 60 && isUpper &&
        !text.includes('\\n') &&
        ls / px(cs.fontSize) > 0.04 && px(cs.fontSize) < 20) {
      const isHeading = x => x && /^h[1-4]$/.test(x.tagName.toLowerCase());
      if (isHeading(el.nextElementSibling) ||
          isHeading(el.parentElement?.nextElementSibling)) {
        out.eyebrows.push({text: text.slice(0, 40),
                           fontSize: px(cs.fontSize),
                           letterSpacing: ls});
      }
    }

    // Numbered section markers (01 / 02 / 03), the other structural tell
    // the skill calls out by name.
    if (el.children.length === 0 && /^(0\\d|\\d{2})$/.test(text)) {
      out.numbered += 1;
    }
  }
  // The page background is not reliably on <body>. It is often painted on
  // :root, or on a full-bleed wrapper, leaving body transparent. Walk up
  // first, then fall back to the largest element that actually paints one.
  const opaque = v => v && v !== 'transparent' &&
    !/rgba\\(\\s*0,\\s*0,\\s*0,\\s*0\\s*\\)/.test(v);
  let bg = null;
  for (const el of [document.body, document.documentElement]) {
    const v = norm(getComputedStyle(el).backgroundColor);
    if (opaque(v)) { bg = v; break; }
  }
  if (!bg) {
    let bestArea = 0;
    for (const el of document.querySelectorAll('body, body *')) {
      const v = norm(getComputedStyle(el).backgroundColor);
      if (!opaque(v)) continue;
      const r = el.getBoundingClientRect();
      const a = r.width * r.height;
      if (a > bestArea) { bestArea = a; bg = v; }
    }
  }
  out.bodyBackground = bg || 'rgb(255, 255, 255)';
  out.docHeight = document.documentElement.scrollHeight;
  return out;
}
"""


def parse_rgb(s: str) -> tuple[float, float, float, float] | None:
    if not s or not s.startswith("rgb"):
        return None
    nums = [float(x) for x in s[s.index("(") + 1:s.index(")")].replace("/", " ")
            .replace(",", " ").split()]
    if len(nums) < 3:
        return None
    a = nums[3] if len(nums) > 3 else 1.0
    return nums[0], nums[1], nums[2], a


def srgb_to_oklch(r: float, g: float, b: float) -> tuple[float, float, float]:
    """sRGB 0-255 -> (L, C, H degrees). Same space DESIGN.md uses."""
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
    C = math.hypot(A, B)
    H = math.degrees(math.atan2(B, A)) % 360
    return L, C, H


def classify_font(stack: str) -> str:
    s = (stack or "").lower()
    mono = ("mono", "courier", "consolas", "menlo", "jetbrains")
    serif = ("serif", "georgia", "times", "garamond", "fraunces", "playfair",
             "baskerville", "didot", "bodoni", "freight", "tiempos", "lora")
    if any(k in s for k in mono):
        return "mono"
    # "sans-serif" contains "serif", so sans must be ruled out first.
    if "sans" in s:
        return "sans"
    if any(k in s for k in serif):
        return "serif"
    return "sans"


def summarise(probe: dict) -> dict:
    els = probe["elements"]

    bg = parse_rgb(probe["bodyBackground"])
    bg_oklch = srgb_to_oklch(*bg[:3]) if bg and bg[3] > 0 else None

    # Accent: the most chromatic colour in use, weighted to things that are
    # actually visible. A saturated hue on a 2px border is still the accent.
    best = None
    for e in els:
        for field in ("color", "background", "borderColor"):
            c = parse_rgb(e.get(field) or "")
            if not c or c[3] < 0.5:
                continue
            L, C, H = srgb_to_oklch(*c[:3])
            if C < 0.06 or L < 0.15 or L > 0.95:
                continue  # near-neutral or near-black/white: not an accent
            if best is None or C > best[1]:
                best = (L, C, H)

    # The display face is the *largest* heading, not the first one in DOM
    # order. A real site put a small monospace label ahead of its h1 and the
    # first-match version reported the wrong typeface for the whole page.
    # Multi-hue metrics. Everything above assumes a page has one accent, which
    # is true of all three documented attractors and false of anything
    # deliberately maximal. Without these, a page using six saturated hues and
    # a page using one score identically.
    hues, chromas = [], []
    for e in els:
        if e["area"] < 200:
            continue
        for field in ("color", "background", "borderColor"):
            c = parse_rgb(e.get(field) or "")
            if not c or c[3] < 0.5:
                continue
            L, C, H = srgb_to_oklch(*c[:3])
            if C < 0.08 or L < 0.12 or L > 0.96:
                continue
            hues.append(H)
            chromas.append(C)
    # 30-degree bins: finer than that and antialiasing noise invents hues.
    bins = {int(h // 30) for h in hues}
    if hues:
        rad = [math.radians(h) for h in hues]
        cx = sum(math.cos(r) for r in rad) / len(rad)
        cy = sum(math.sin(r) for r in rad) / len(rad)
        hue_spread = 1.0 - math.hypot(cx, cy)   # 0 = one hue, 1 = all over
    else:
        hue_spread = 0.0

    headings = sorted(
        [e for e in els if e["tag"] in ("h1", "h2") and e["hasOwnText"]],
        key=lambda e: -e["fontSize"])
    body = sorted(
        [e for e in els if e["tag"] in ("p", "li") and e["hasOwnText"]],
        key=lambda e: -e["area"])

    radii = [e["radius"] for e in els if e["area"] > 400]
    borders = [e["borderWidth"] for e in els
               if e["borderWidth"] > 0 and e["area"] > 400]

    return {
        "bg_L": round(bg_oklch[0], 3) if bg_oklch else None,
        "bg_C": round(bg_oklch[1], 3) if bg_oklch else None,
        "bg_H": round(bg_oklch[2], 1) if bg_oklch else None,
        "accent_L": round(best[0], 3) if best else None,
        "accent_C": round(best[1], 3) if best else None,
        "accent_H": round(best[2], 1) if best else None,
        "heading_font": classify_font(headings[0]["fontFamily"]) if headings else None,
        "heading_stack": headings[0]["fontFamily"][:70] if headings else None,
        "body_font": classify_font(body[0]["fontFamily"]) if body else None,
        "median_radius": sorted(radii)[len(radii) // 2] if radii else 0.0,
        "max_radius": max(radii) if radii else 0.0,
        "hairline_borders": sum(1 for b in borders if b <= 1.5),
        "hue_bins": len(bins),
        "max_chroma": round(max(chromas), 3) if chromas else 0.0,
        "hue_spread": round(hue_spread, 3),
        "chromatic_elements": len(chromas),
        "eyebrows": len(probe["eyebrows"]),
        "eyebrow_samples": [e["text"] for e in probe["eyebrows"][:4]],
        "numbered_markers": probe["numbered"],
        "n_elements": len(els),
        "doc_height": probe["docHeight"],
    }


def attractor(s: dict) -> str:
    """Which of the three documented AI-design looks, if any."""
    L, aC, aH = s.get("bg_L"), s.get("accent_C"), s.get("accent_H")
    if L is None:
        return "unknown"
    warm_bg = L > 0.88 and (s.get("bg_C") or 0) > 0.008
    if warm_bg and s.get("heading_font") == "serif":
        return "1-cream-serif-terracotta"
    if L < 0.30 and aC and aC > 0.12:
        return "2-near-black-bright-accent"
    if s.get("median_radius", 0) == 0 and s.get("hairline_borders", 0) >= 3:
        return "3-broadsheet-hairline"
    return "other"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--only", nargs="*", help="substring filter on page names")
    args = ap.parse_args()

    pages = sorted(PAGES.glob("*.html"))
    if args.only:
        pages = [p for p in pages if any(o in p.stem for o in args.only)]
    if not pages:
        raise SystemExit("no pages found - run house_style.generate first")

    SHOTS.mkdir(exist_ok=True)
    rows = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport=VIEWPORT, device_scale_factor=2)
        for p in pages:
            page.goto(p.resolve().as_uri(), wait_until="load")
            page.wait_for_timeout(300)
            probe = page.evaluate(PROBE)
            s = summarise(probe)
            s["name"] = p.stem
            s["attractor"] = attractor(s)
            rows.append(s)
            page.screenshot(path=str(SHOTS / f"{p.stem}.png"), full_page=True)
            print(f"  {p.stem:46} bg_L={s['bg_L']} "
                  f"head={s['heading_font']:5} eyebrows={s['eyebrows']:2} "
                  f"r={s['median_radius']:.0f}  {s['attractor']}", flush=True)
        browser.close()

    # Merge rather than replace. A filtered run used to truncate the file to
    # whatever it had just measured, silently destroying every other page's
    # numbers -- an expensive way to lose a corpus that took an hour to render.
    merged: dict[str, dict] = {}
    if STYLES.exists():
        for line in STYLES.read_text().splitlines():
            if line.strip():
                prev = json.loads(line)
                merged[prev["name"]] = prev
    for r in rows:
        merged[r["name"]] = r
    with STYLES.open("w") as f:
        for name in sorted(merged):
            f.write(json.dumps(merged[name]) + "\n")
    print(f"\nwrote {STYLES.name} ({len(rows)} measured, "
          f"{len(merged)} total) and {SHOTS.name}/")


if __name__ == "__main__":
    main()

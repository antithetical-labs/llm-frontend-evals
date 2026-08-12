"""Contact sheets from the full-page screenshots.

Full-page shots are 2880 x 5000+ and unreadable side by side. Each cell here is
the top of the page -- the hero -- scaled down, because the hero is where the
palette, the type and the surface treatment are all decided. Scrolling further
mostly repeats them.

Two sheets, answering two different questions:

  grid       models across, conditions down, one brief -- does the intervention
             move anything, and do the models agree with each other?
  runs       one model, one brief, one condition, five runs -- is the default
             a tendency or a fixture?
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
SHOTS = ROOT / "shots"
FIGURES = ROOT / "figures"

BG = (14, 10, 9)
TEXT = (244, 237, 235)
MUTED = (140, 132, 130)
HAIR = (60, 55, 53)

CELL_W = 460
CELL_H = 320          # hero crop, 1440x1000 of the page at 2x, scaled
PAD = 14
LABEL_H = 22

FONT_DIR = ROOT / "assets" / "fonts"


def font(size: int, mono: bool = True):
    name = "jetbrainsmono-400.ttf" if mono else "archivo-500.ttf"
    try:
        return ImageFont.truetype(str(FONT_DIR / name), size)
    except OSError:
        return ImageFont.load_default()


def hero(path: Path) -> Image.Image:
    """Top of the page, scaled to a cell."""
    im = Image.open(path).convert("RGB")
    # Screenshots are device_scale_factor=2 on a 1440 viewport.
    crop_h = min(im.height, int(im.width * CELL_H / CELL_W))
    im = im.crop((0, 0, im.width, crop_h))
    return im.resize((CELL_W, CELL_H), Image.LANCZOS)


def sheet(cells: list[list[tuple[str, Path | None]]], title: str,
          out: Path) -> Path:
    rows, cols = len(cells), max(len(r) for r in cells)
    W = cols * CELL_W + (cols + 1) * PAD
    H = rows * (CELL_H + LABEL_H) + (rows + 1) * PAD + 46
    canvas = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(canvas)
    d.text((PAD, 14), title, fill=TEXT, font=font(17, mono=False))

    for ri, row in enumerate(cells):
        for ci, (label, path) in enumerate(row):
            x = PAD + ci * (CELL_W + PAD)
            y = 46 + PAD + ri * (CELL_H + LABEL_H + PAD)
            d.text((x, y), label, fill=MUTED, font=font(11))
            box = (x, y + LABEL_H, x + CELL_W, y + LABEL_H + CELL_H)
            if path and path.exists():
                canvas.paste(hero(path), (box[0], box[1]))
            else:
                d.text((x + 8, y + LABEL_H + 8), "missing", fill=HAIR,
                       font=font(11))
            d.rectangle(box, outline=HAIR, width=1)

    FIGURES.mkdir(exist_ok=True)
    canvas.save(out)
    return out


def shot(model: str, brief: str, cond: str, run: int) -> Path:
    return SHOTS / f"{model}__{brief}__{cond}__{run}.png"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--models", nargs="*",
                    default=["claude", "gpt", "kimi", "gemini"])
    ap.add_argument("--conditions", nargs="*",
                    default=["bare", "nudge", "skill", "forbid",
                             "direct1", "direct"])
    ap.add_argument("--run", type=int, default=1)
    args = ap.parse_args()

    outs = []
    for brief in ("streamforge", "backlot"):
        cells = [[(f"{m}  ·  {c}", shot(m, brief, c, args.run))
                  for m in args.models] for c in args.conditions]
        outs.append(sheet(
            cells,
            f"{brief}  —  run {args.run}   (rows: bare / nudge / skill)",
            FIGURES / f"sheet-{brief}.png"))

    # Persistence: five runs of the untouched default.
    for model in args.models:
        cells = [[(f"run {r}", shot(model, "streamforge", "bare", r))
                  for r in range(1, 6)]]
        outs.append(sheet(
            cells, f"{model} — streamforge, bare, five independent runs",
            FIGURES / f"sheet-runs-{model}.png"))

    for o in outs:
        print("wrote", o.relative_to(ROOT))


if __name__ == "__main__":
    main()

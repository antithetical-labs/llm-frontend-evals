"""The briefs and the conditions.

Two briefs rather than one, because they control for each other. A dev-tool
landing page is the most templated genre on the internet, so every model has seen
thousands of them and may converge for reasons that have nothing to do with the
model -- genre gravity rather than house style. A back-office tool for a
non-technical audience is far less templated, so model-specific style has more
room to show.

If a look appears in both, it is the model. If it appears in one, it is the genre.
"""

import os

BRIEFS = {
    "streamforge": (
        "Design a landing page for Streamforge, a live-streaming platform where "
        "developers broadcast themselves building software with AI assistants. "
        "Viewers watch the prompts, the model's output, and the code evolve in "
        "real time, and can fork any stream's repository. The audience is "
        "working developers aged 25 to 40."
    ),
    "backlot": (
        "Design a landing page for Backlot, an operations tool for full-time "
        "content creators. It consolidates brand-deal contracts, invoices, "
        "sponsor deadlines, and per-platform payout tracking in one place. The "
        "audience is solo creators aged 22 to 35 who earn a living from video "
        "and are not finance people."
    ),
}

# Held identical across every cell so output shape is never a variable. Plain
# HTML and CSS rather than Tailwind: the skill under test assumes Tailwind and
# React, but utility classes push the actual colour and type decisions into class
# names and a framework's default scale, which is exactly what has to be measured
# here. The deviation is real and belongs in the writeup.
FORMAT = (
    "Return one complete, self-contained HTML document. All CSS must be in a "
    "single <style> block in the head. No external stylesheets, no CDN links, no "
    "JavaScript frameworks, no build step. Use system-available fonts or a "
    "@font-face-free font stack. The page needs a hero, a short how-it-works "
    "section, three feature blocks, and a sign-up call to action. Output only "
    "the HTML document, with no commentary before or after it."
)

# The one-line folk remedy, quoted from the wording people actually use.
NUDGE = (
    "Avoid generic AI-generated aesthetics. Make it distinctive."
)

# Specific prohibitions, naming the four patterns the bare pages actually
# produced: gradient 78%, dark-plus-single-bright-accent 49%, pill 31%,
# glass 29%. Because the baseline rate of each is known, compliance is
# measurable per prohibition rather than as a general impression.
FORBID = (
    "Do not use gradients of any kind. Do not use a dark background with a "
    "single bright accent colour. Do not use frosted-glass or blur effects. "
    "Do not use fully-rounded pill-shaped buttons."
)

# Positive direction, deliberately light -- one sentence, no spec. The target
# is chosen to sit outside all three documented attractors: acid design is
# multi-hue and high-chroma where they are single-accent, and its display type
# is warped or blackletter where theirs is grotesque or serif. A target that
# happened to match an attractor could not distinguish "followed the
# direction" from "fell into a default".
DIRECTION = (
    "Take the visual direction from acid design - futuristic, digital, "
    "high-energy."
)

# Asked before any markup exists. The point is to make the model state what the
# aesthetic actually is before it starts building, which is the step that
# separates the two positive arms.
GROUND = (
    "Before building anything, ground the aesthetic. What are the actual "
    "characteristics of this direction - palette, typography, texture, layout "
    "logic, what it borrows from and what it rejects? Write that down first, "
    "as prose. Do not write any HTML yet."
)

CONDITIONS = {
    # What is the actual default when nothing is said?
    "bare": {"system": None, "extra": "", "ground": False},
    # Does the vague negative do anything?
    "nudge": {"system": None, "extra": " " + NUDGE, "ground": False},
    # Does the structured guidance do anything the one-liner does not?
    # Note this delivers the skill's text one-shot; the skill is designed as a
    # three-phase interactive workflow, so this is not a test of it as built.
    "skill": {"system": "SKILL", "extra": "", "ground": False},
    # Does naming the specific patterns to avoid work any better than vagueness?
    "forbid": {"system": None, "extra": " " + FORBID, "ground": False},
    # Same prohibition, run at high reasoning effort. The low-effort forbid
    # pages came back near-blank, and two explanations fit equally well: the
    # white documentation page is genuinely the next attractor down, or a
    # constrained model on a low thinking budget takes the cheapest compliant
    # path. Only the effort knob separates them, so it is the only thing that
    # differs from `forbid`.
    "forbid-hi": {"system": None, "extra": " " + FORBID, "ground": False,
                  "effort": "high"},
    # Positive direction, same weight of instruction, no grounding step.
    "direct1": {"system": None, "extra": " " + DIRECTION, "ground": False},
    # Positive direction plus a turn spent working out what it means. The pair
    # direct1/direct isolates the grounding step from the positive framing.
    "direct": {"system": None, "extra": " " + DIRECTION, "ground": True},
}

# Path to the UI-design skill used by the `skill` condition. It is a local file
# rather than a vendored copy because it is not mine to redistribute; point
# UI_SKILL_PATH at your own to run that condition.
SKILL_PATH = os.environ.get("UI_SKILL_PATH", "")


def prompt_for(brief_key: str, condition: str) -> tuple[str | None, list[str]]:
    """-> (system prompt or None, list of user turns).

    One turn for every condition except `direct`, which spends a first turn
    grounding the aesthetic and only asks for markup on the second. The build
    instruction is identical in both cases, so the only difference between
    direct1 and direct is that one of them thought about it first.
    """
    cond = CONDITIONS[condition]
    system = None
    if cond["system"] == "SKILL":
        if not SKILL_PATH:
            raise SystemExit(
                "the 'skill' condition needs UI_SKILL_PATH set to a SKILL.md")
        with open(SKILL_PATH) as f:
            system = f.read()

    brief = f"{BRIEFS[brief_key]}{cond['extra']}"
    if cond.get("ground"):
        return system, [f"{brief}\n\n{GROUND}", f"Now build the page.\n\n{FORMAT}"]
    return system, [f"{brief}\n\n{FORMAT}"]

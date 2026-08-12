# Streamforge: Aesthetic Grounding — Acid Design Direction

Before a single line of markup, here's what "acid design" actually means and how it applies to Streamforge.

## What Acid Design Is

Acid design (or "acid graphics") descends from early-90s rave flyers and warehouse-party visuals, re-interpreted through a contemporary screen-native lens. Its DNA: the smiley-face era of acid house, cyberpunk's chrome-and-neon fantasy, Y2K techno-optimism, and the raw anti-polish of early web brutalism. What it *rejects* is equally important: the sanitized SaaS gradient, the soft-rounded friendly startup, the beige minimalism of the last decade. Acid design is allergic to corporate calm. It wants to feel like a system running slightly too hot.

For Streamforge this fit is natural. The product is watching code mutate live under AI prompting — inherently glitchy, high-velocity, unpolished-process content. A calm landing page would lie about the experience.

## Palette

The core is a near-black void — not pure `#000` but a deep blue-black like `#050508` — against which everything burns. The accent system:

- **Acid lime / chartreuse** (`#c8ff00` range): the primary signal color. This is the non-negotiable acid color — it reads as phosphor, as terminal, as radiation.
- **Electric magenta or hot violet** as the secondary accent, used sparingly for hover states and secondary CTAs.
- **Chrome/metallic gradients** (silver to gunmetal with harsh specular highlights) for select display type and decorative elements — the Y2K borrow.
- White for body text, but never large calm fields of it.

The rule: darkness dominates, lime screams, everything else supports. Lime is used for data, live indicators, links, and code-highlight accents — things that feel "energized."

## Typography

Two voices, high contrast:

- **Display:** a heavy condensed grotesk or a hyper-extended wide font — think Monument Extended, Neue Haas Grotesk in Black, or a techno face like Space Grotesk pushed to its boldest weight. All caps, tight or exaggerated tracking, often oversized to the point of clipping. Headlines should feel stamped, not typed.
- **Functional/mono:** a technical monospace (JetBrains Mono, IBM Plex Mono) for everything that smells like data — stats, timestamps, stream metadata, code snippets. This is a developer audience; monospace is a trust signal, not a decoration.

Reject: friendly geometric sans at medium weight, sentence-case headlines, generous comfortable leading. Acid type is either monumental or terminal.

## Texture & Atmosphere

- **Scanlines and grain:** a subtle CRT/noise overlay across the page, so the whole thing reads as a *feed*, not a document.
- **Glow, but hard-edged:** lime glows around live indicators — but Gaussian blur used like a weapon, not a softbox.
- **Glitch motifs:** chromatic aberration on hover, RGB-split moments during scroll transitions, occasional "corrupted" text scrambles. These should trigger on interaction, not loop passively — passive loops become noise.
- **Borders and frames:** thin 1px lime rules, corner-bracket "viewfinder" marks, dashed selection rectangles — the visual language of a broadcast HUD.
- **NO soft shadows, no rounded cards, no frosted glass.** That's the aesthetic this direction explicitly rejects. Corners are sharp or chamfered.

## Layout Logic

Acid layouts borrow from rave flyers: maximalist density, layered and slightly chaotic, but with a strict underlying grid so the chaos reads as intentional energy rather than sloppiness.

- **HUD framing:** the page treats itself as a broadcast interface. Persistent status bar, section markers like `// 01 — LIVE FEED`, coordinates and timestamps in margins.
- **Overlap and collision:** type overlapping media, marquees slicing across sections, elements bleeding off edges. But every collision is deliberate.
- **Asymmetry with anchors:** dense left, breathing right; or a massive display block anchoring an otherwise busy section.
- **Marquees and tickers:** horizontally scrolling text (streamer names, live stats) — a direct rave-flyer and stock-ticker inheritance, and thematically perfect for "live."

## What It Borrows

- From **rave flyers**: density, chrome, smiley-adjacent iconography (we'd use a "signal" glyph instead), flyer-style sticker clusters of badges.
- From **terminals/IDEs**: mono type, lime-on-black, prompt syntax (`$ streamforge fork`), blinking cursors.
- From **broadcast graphics**: LIVE badges, lower-thirds, viewfinder brackets.
- From **Y2K/cyberpunk**: chrome gradients, techno fonts, optimistic-machine energy.

## What It Rejects

SaaS purple-blue gradients, illustration-heavy hero sections, rounded-2xl cards, "friendly" tone, whitespace as luxury, pastel anything. Nothing on this page should look like it could be a project-management tool.

## The Streamforge-Specific Twist

The unique asset is that the *product content* — code diffs, prompt/output pairs, live viewer counts — is already acid-native material. The design should let real stream data carry the aesthetic: a hero that's a live code pane with a prompt visible mid-execution, fork buttons styled like terminal commands, viewer counts as HUD telemetry. The page doesn't decorate the concept; it *is* a slice of the broadcast.

---

Want me to proceed to the HTML build on this foundation?
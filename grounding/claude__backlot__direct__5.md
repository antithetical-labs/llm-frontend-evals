# Acid Design — Grounding the Aesthetic

## What it actually is

Acid design is the visual language of late-90s rave flyers, Y2K software packaging, and Winamp skins, filtered back through the browser by way of 2020s Blender renders and CSS that finally got good. Its emotional register is *overload handled confidently*. Not chaos — chaos is punk. Acid is **engineered intensity**: everything is turned up, but everything is also aligned to a grid. The core tension that makes it work is precision hosting excess.

It borrows from: rave and jungle flyers, chrome type from 2001 nu-metal album art, technical readouts (HUDs, oscilloscopes, spectrum analyzers), CAD wireframes, holographic trading cards, bootleg merch, blister-pack product photography, and the specific ugliness of early web gradients used on purpose.

It rejects: the entire 2016–2021 SaaS playbook. No soft blue-to-purple gradient hero. No friendly rounded illustration of a person holding an oversized coin. No 24px border radius on everything. No `#F9FAFB` background with a `#111827` headline. No stock photography. No "trusted by" logo bar rendered at 40% opacity as an apology. It also rejects brutalism's asceticism — acid is not raw HTML with Times New Roman, it's *hyper-produced*.

## Palette

The logic is **one violent hue against near-black, with a cold metallic as the mediator.**

- **Base:** not black but a bruised near-black with a hue in it — `#0A0B0D`, or better, a slightly green-shifted `#080A09`. Flat black reads as "premium dark mode"; tinted black reads as CRT.
- **The acid:** a single high-voltage lead. Candidates are acid lime `#C6FF00`/`#D4FF3F`, cyber cyan `#00F0FF`, or hot magenta `#FF2D9B`. **One of these leads. Only one.** For Backlot I'd take **acid lime** — it's the money color without being literal green-for-finance, it screams on black, and it's not the crypto cyan everyone already used.
- **Secondary accent, used sparingly (5–10% of colored area):** magenta or electric violet, for state changes, warnings, and one or two deliberate clashes. The clash is the point — lime on magenta is physically uncomfortable at large sizes, which is why it appears only in small hits.
- **The mediator:** chrome/silver as a *gradient*, not a flat gray. A four-stop gradient (`#F2F4F5 → #8A9298 → #FFFFFF → #4A5157`) applied to type or panel edges reads instantly as liquid metal and gives the eye a rest between saturated blocks.
- **Text:** off-white `#EDEFED`, never pure white. Muted copy at `#8B928D`, warm enough to avoid looking like disabled state.

Gradients are allowed but must be **hard-edged, angular, or dithered** — a chrome bevel, a two-stop diagonal wipe, a stepped/posterized ramp. Never a soft radial blob.

## Typography

Two-voice system, maximum contrast between them.

**Display voice:** wide, tight, mechanical. A grotesk with a technical build — Neue Haas Grotesk Display, Archivo Expanded, Space Grotesk, Anton for extreme cases, or a squarish techno face like Chakra Petch / Monument Extended. Set **very large** (clamp up to 8–14vw), tracking pulled negative to `-0.03em` or tighter, line-height crushed to `0.85–0.92` so multi-line headlines lock into a solid block. Uppercase for short strings, mixed case for long ones. Occasional single word given chrome or lime fill inside an otherwise white headline.

**Utility voice:** monospace, everywhere else that isn't body copy. JetBrains Mono, Space Mono, or Berkeley Mono. Used for labels, eyebrows, metadata, numbers, nav, buttons, table headers, timestamps, and status pills — always uppercase, `0.7–0.8rem`, letter-spacing `+0.12em`. This is the single highest-leverage move in the whole style: monospace micro-copy makes any layout read as instrumentation rather than marketing.

**Body copy:** here's where the discipline lives. Body is a clean, boring, extremely legible grotesk at 17–19px, `1.55` line-height, `#8B928D`–`#C9CFCB`, max 60ch. Acid design fails when the intensity leaks into the paragraphs. Loud frame, calm content.

Numbers get special treatment — tabular figures, large, mono or display-wide, treated as a graphic element. Backlot is a product about numbers; the numbers should be the hero imagery.

## Texture

Acid design is never flat. It's flat *shapes* with dirty *surfaces*. The stack:

1. **Grain/noise** — a fine film grain at 3–6% opacity over the whole page, or an SVG `feTurbulence` overlay. Kills the plasticky feel of pure CSS color.
2. **Grid lines** — a faint 1px lattice at `rgba(214,255,63,0.06)`, or dotted 2px-on-24px. This is the "engineered" half of engineered intensity, and it makes the layout's alignment visible rather than just felt.
3. **Scanlines / dither** — repeating-linear-gradient horizontal lines on specific panels (hero, media frames) at very low opacity. Suggests CRT and video, which is on-brand for a creator tool.
4. **Chrome and glass** — one or two hero objects with metallic bevels or a blurred backdrop-filter panel. Rare, so they land.
5. **Hard glow** — box-shadow in the acid hue with tight spread on interactive elements, plus a subtle `filter: blur()` duplicate behind key type. Not neon-sign glow; more like a phosphor bloom.
6. **Halftone/dot patterns** at edges and behind headlines, borrowed from risograph and flyer printing.

Corners: mostly `0`, sometimes `2px`. Exception: **pill radius (999px)** on tags, status chips, and small buttons. The 0-or-999 rule — nothing in between — is a strong signature.

## Layout logic

The organizing principle is **a rigid grid, deliberately violated in three or four specific places.**

- 12-column grid, visible via the lattice. Generous section padding vertically (`clamp(6rem, 12vh, 11rem)`), tight horizontally — content wants to press against the viewport edges more than a normal SaaS page allows.
- **Full-bleed horizontal rules and marquees** as section dividers. A scrolling ticker of monospace text (`CONTRACT SIGNED · INVOICE PAID · DEADLINE T-3 · PAYOUT CLEARED ·`) is the canonical acid transition device and is genuinely useful here as ambient product proof.
- **Asymmetry with intent:** a headline occupying columns 1–7, its supporting paragraph starting at column 9 and dropping 120px below the baseline. Nothing centered except one intentional statement moment.
- **Overlap and layering:** cards that break their container, a number that runs over an image edge, a badge rotated 4–8° and pinned to a panel corner. Z-index is a design tool, not an accident.
- **Bento / modular blocks** for the feature grid — panels of unequal weight (2×1, 1×1, 1×2) with hairline lime borders, each carrying a mono label in its top-left and a number or micro-UI as its content.
- **Density over airiness.** Whitespace exists, but the page should feel *packed with information* — a creator's operational dashboard has a lot going on, and the page should mirror that competence. Where a normal SaaS page shows three benefits, this shows nine, arranged so the eye can graze.
- Rotation used at most 3 times per page, always small angles, always on small objects.

## Motion

Fast, mechanical, non-organic. `120–220ms`, `cubic-bezier(.2,.8,.2,1)` or stepped `steps()` for a digital snap. Hover states *invert* (lime fill, black text) rather than lighten. Numbers count up on scroll-in. The marquee runs continuously. One or two elements get a `mix-blend-mode: difference` or a 1-frame glitch offset on hover. Nothing eases slowly, nothing bounces, nothing fades in over 600ms. All of it behind `prefers-reduced-motion`.

## Where this direction has to be restrained — and why that's the design problem

The audience is 22–35, video-native, aesthetically fluent, and would find a Stripe-clone landing page condescending. They *want* something that looks like the software their editing suite would use. That's the mandate for acid.

But the subject matter is contracts, invoices, deadlines, and payouts — things that create genuine anxiety in people who explicitly do not identify as finance people. If the page feels chaotic, it undermines the entire promise, which is *relief*. So:

- **Chaos in the chrome, order in the content.** Every actual piece of information — a deadline, a dollar figure, a contract status — is presented with dead-clear hierarchy and high contrast. All the noise lives in borders, backgrounds, tickers, and dividers.
- **Contrast is non-negotiable.** Lime on near-black clears AA comfortably; lime on white does not, so lime never sits on light backgrounds. Body text never drops below `#8B928D` on `#0A0B0D`.
- **Product screenshots are the payoff, not decoration.** The UI mockups should look *calmer* than the marketing frame around them. That inversion — wild page, serene app — is the strongest possible argument for the product.
- **No finance clichés.** No stock charts trending up-and-right for their own sake, no coin/wallet/vault iconography, no "wealth" language. The tone is *your business, handled* — spoken in the language of a video editor's timeline and a rave flyer, not a bank.
- The copy voice matches: short, declarative, mono-cased, a little cocky. "Every deal. Every deadline. Every dollar." Not "Streamline your creator finances."

The whole page should read as if a very good record label designed accounting software.

---

Ready to build on this — say go and I'll produce the page.
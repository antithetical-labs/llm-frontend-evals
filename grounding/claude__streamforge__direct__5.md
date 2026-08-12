# Acid Design — Aesthetic Grounding for Streamforge

## What this direction actually is

Acid design is the visual language of the late-90s rave flyer and the CD-ROM demo disc, retrieved and rebuilt with modern rendering. Its emotional register is *overload under control*: a surface that looks like it's running hot, generating more signal than the frame can hold, but held together by a rigid underlying grid. It is not "neon cyberpunk," which is nostalgic and cinematic and mostly dark-blue. Acid is chemical, iridescent, and closer to industrial design documentation than to Blade Runner. Think Y2K optimism reprocessed through 2020s tooling: chrome that looks liquid rather than metallic, gradients that behave like oil on water, type that has been stretched on a machine rather than drawn by hand.

For Streamforge this is unusually apt, because the product's core subject *is* generation — a model producing more output than a human can read in real time, code mutating on screen. The aesthetic should feel like a readout of that process, not decoration applied over it.

## Palette

The rule is a **dark, slightly-warm graphite base** — not pure black, not navy. Something around `#0A0A0B` to `#141416`, with a faint green or violet cast so it reads as a screen rather than a void. On top of that, two or three acid accents at maximum chroma:

- **Acid lime / chartreuse** (`#C8FF00`, `#A3F600`) as the primary. This is the load-bearing color: it's the color of hazard tape, of highlighter, of terminal green pushed into yellow. It signals "live" better than red does, because red is an error state in developer tooling and lime is not.
- **Electric magenta / hot violet** (`#FF2FB4`, `#7B2BFF`) as the counterweight. Used sparingly, mostly in gradients and glows, to create the chromatic-aberration tension that makes lime feel radioactive rather than merely bright.
- **Iridescent transitions** — cyan bleeding into lilac into pale gold — reserved for large-format objects: a hero blob, a chrome nameplate, a section divider. Never for text at body size.

Neutrals stay cold and slightly tinted: `#8A8A94` for secondary copy, `#EDEDF0` for primary. Pure white appears only where something needs to feel blown out.

Crucially, acid palettes work by **ratio discipline**: roughly 80% near-black, 15% neutral, 5% screaming color. The energy comes from restraint around the accents. If everything glows, nothing does.

## Typography

Two voices, deliberately mismatched in temperature.

**Display:** a wide, tightly-tracked grotesque or a compressed technical sans — Neue Haas Grotesk Display, Archivo Expanded, Suisse Intl Condensed, or in a web-safe stack something like Inter set very tight with negative letter-spacing and optical sizing pushed. Headlines run large, uppercase or sentence-case-but-huge, with tracking pulled to -3% to -5% so words lock into slabs. Line height under 0.9 for multi-line headlines so the block reads as a mass. Occasional stretched or squashed setting — horizontally scaled type — is on-brand here in a way it would be sacrilege elsewhere; acid design borrows the *distorted* type of flyer culture, where the tool's limits were visible.

**Utility:** a monospace, used far more than in a normal marketing site — for labels, stat readouts, timestamps, nav items, badge text, form fields. JetBrains Mono, Berkeley Mono, or IBM Plex Mono. Set small (11–13px), uppercase, with wide positive tracking (0.1–0.2em). This is where the developer credibility lives, and it doubles as texture: monospace at small sizes reads as machine annotation, which lets the page look like an interface rather than a brochure.

Body copy stays modest and genuinely readable — 16–18px, generous measure, neutral grey. The audience is 25-40-year-old working developers; they will forgive a loud hero and will not forgive unreadable paragraphs. The contrast between howling display type and calm body text is itself part of the style.

## Texture

Acid design is never flat, but it's also never skeuomorphic. The textures are all *optical*:

- **Noise/grain** at low opacity over the entire page, so gradients don't band and the black feels like film or CRT phosphor rather than hex code.
- **Scanlines and dither** — 1px horizontal rules at 2–4px intervals, at very low alpha, layered over dark panels. This is the cheapest, most effective signal of "broadcast."
- **Blurred chromatic blobs** behind content: large radial gradients of lime and magenta at heavy blur, clipped and multiplied. They imply a light source outside the frame.
- **Chrome and liquid metal** as a punctuation element — a conic-gradient sphere, an extruded logotype, a warped grid plane. One per page at most; chrome is a spice.
- **Hairline strokes** in lime at 10–20% opacity forming the grid itself, visible. Acid design likes to show its construction: crop marks, registration ticks, dimension lines, bounding boxes with corner brackets.
- **Halftone or duotone treatment** on any photography, so imagery matches the synthetic surfaces rather than fighting them.

Corner radii tend toward extremes — either 0px (technical, drafted) or very large pill shapes (Y2K bubble). Mid-range 8px radii read as generic SaaS and should be avoided.

## Layout logic

The underlying structure is a **visible, over-specified grid** — 12-column, hairlines drawn, with content deliberately breaking it. The tension between rigid substrate and rule-breaking content is the whole game. Concretely:

- Asymmetry over centering. Hero copy pinned left, filling maybe 7 of 12 columns, with a live-stream artifact bleeding off the right edge.
- **Edge-to-edge bleed.** Panels, marquees, and code windows run past the viewport edge to imply the frame is a crop of something larger.
- **Dense information clusters** next to large voids. Acid pages breathe unevenly: a wall of monospace telemetry, then 200px of nothing, then a headline at 120px.
- **Marquee tickers** as horizontal rules — scrolling text as a structural device, not a gimmick, because a live-streaming product genuinely has a ticker's worth of state to report.
- **Layering with z-depth** — overlapping cards with slight rotation, badges pinned outside their parent's bounds, sticky labels that sit *on top* of section boundaries.
- Stacked, full-bleed sections separated by 1px lime rules and small monospace section numbers (`§ 02 / HOW IT WORKS`) in the margin.

Motion, when present, is mechanical and looping rather than easing-and-fading: cursor blinks, token-by-token text reveals, counters incrementing, marquees at constant velocity. Nothing bounces.

## What it borrows

Rave and jungle flyer design (Designers Republic above all), Wipeout and PS1-era game UI, Winamp skins and demoscene intros, CD-ROM encyclopedia interfaces, Japanese technical packaging, Swiss grid pedagogy inverted into maximalism, oscilloscope and spectrum-analyzer readouts, warning labels and industrial safety graphics.

## What it rejects

Soft pastel gradients and blurred purple SaaS heroes. Rounded friendly illustration — no isometric people, no blobby mascots, no hand-drawn arrows. Centered-everything hero layouts with a single CTA and a floating dashboard screenshot. Glassmorphism as a default. Drop shadows that imply paper. Stock photography of teams laughing at laptops. Lorem-ipsum-shaped benefit copy. Anything that reads as "trustworthy enterprise" — this direction trades institutional reassurance for the sense that you've found something before it got big.

## Application notes specific to Streamforge

The product hands us three native assets that *are* the aesthetic: the prompt, the model output, and the diff. The page should treat these as its primary imagery — a live code panel with token-streaming text, a prompt bubble in monospace, a diff gutter with lime `+` lines. No abstract 3D shapes standing in for software when the software itself is more interesting.

"LIVE" needs a real visual system: a lime dot with a pulse, viewer counts in monospace, elapsed timers. Fork counts belong in the same readout language, since forking is the differentiating verb.

Tone of voice should be flat, declarative, slightly cocky, and technically literate — short sentences, real nouns (repo, commit, context window, diff), zero exclamation marks. The visuals carry the volume; the copy stays deadpan.

---

Ready to build on this when you give the word — I'd propose: sticky mono nav with live-count ticker, split hero with streaming code panel, an acid marquee, a three-step "watch / read / fork" section using real diff UI, a stream directory grid, a fork-mechanics section, social proof as monospace telemetry, and a hard-edged CTA footer.
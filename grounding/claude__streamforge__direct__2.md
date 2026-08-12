# Streamforge — Visual Direction

*Aesthetic grounding, written before any markup.*

---

## What "acid" actually is

Acid design is the current revival of late-90s/Y2K rave-flyer graphics filtered through contemporary tooling. Its ancestors are Designers Republic sleeve art, drum-and-bass and trance flyers, Wipeout and Ridge Racer HUDs, early Maya/3D Studio renders, Winamp skins, chrome-and-blob logotypes, and the visual language of CD-ROM demos. Its present-day form lives in techno label identities, Blender-rendered liquid metal, cyber-sigilism, and the "hyper-industrial" look of Vercel/Linear-adjacent dev tooling pushed several notches past corporate safety.

The core emotional payload is *machine energy*: something running hot, computed rather than drawn, high voltage, slightly hostile. It is not playful. It is not friendly. It reads as instrumentation for a system you don't fully control yet.

That maps almost perfectly onto Streamforge. Watching someone prompt an AI into a working codebase in real time *is* a high-voltage spectator sport: telemetry, latency, output streaming into a buffer, a repo mutating live. The design job is to make the page feel like the console of that machine rather than a brochure about it.

## Palette

Acid palettes are built on extreme luminance contrast, not on color harmony. The base is near-black — not pure `#000`, which flattens glow, but a cold charcoal in the `#07090A`–`#0B0D0E` range so that grain and hairlines have somewhere to live. Off-white for text sits around `#E6EBE7`, very slightly green-shifted so it never reads as warm paper.

One dominant acid: **lime/chartreuse**, roughly `#C6FF00` to `#B8FF2E`. This is the signature. It carries the logotype, the primary CTA, the live indicators, the active states. It should appear in maybe 8–12% of the pixel area — enough to feel radioactive, not enough to become the background.

Two supporting voltages: **electric cyan** `#00E9FF` for data, links, and secondary structure; **hot magenta** `#FF2D8F` reserved almost exclusively for the "LIVE" state and moments of alarm or heat. Magenta must stay scarce or the whole thing collapses into generic cyberpunk.

Underneath, a single **iridescent gradient** — cyan → violet → lime, mesh-blurred — used for large soft light sources behind hero elements and nothing else. Chrome, where it appears, is not a color but a gradient ramp: dark steel → white specular → cyan bounce → dark, at a hard angle.

Neutrals in between are cold greys used for chrome UI edges: `#15181A` panel fills, `#232829` hairlines, `#6B7472` for metadata.

Explicitly rejected: pastels, dark-mode purple-blue SaaS gradients, terracotta/sage, anything beige, and multi-hue rainbows applied decoratively.

## Typography

Two-voice system, with a hard rule for each.

**Voice one — display: a wide, tightly-tracked neo-grotesque.** Helvetica Now Display / Neue Haas Grotesk Display / Suisse Intl / Inter Tight in the heaviest available weight, set at negative tracking (`-0.03em` to `-0.05em`), all-caps or sentence case, sizes that are genuinely aggressive — hero headline at 8–14vw, filling the measure edge to edge with almost no side margin. The letterforms should nearly touch. Acid typography treats headlines as *architecture*, not as reading material: they get stretched horizontally, clipped by container edges, overlapped by other elements, occasionally rendered as outline-only or filled with the iridescent gradient.

**Voice two — everything else: monospace.** JetBrains Mono, Berkeley Mono, or IBM Plex Mono. This is the working language of the page. All labels, metadata, nav, timestamps, viewer counts, bylines, and microcopy are mono, uppercase, small (10–12px), with *positive* letterspacing (`0.08em`–`0.16em`) and slash separators: `LIVE / 04:12:38 / 1,204 WATCHING / CLAUDE-SONNET-4`. This is the single most load-bearing decision. Mono microcopy is native to the 25–40 developer audience — it signals instrumentation rather than marketing — and it does most of the work of making the page feel like a system.

Body copy is the one place to break acid's usual illegibility: short mono or a neutral sans at 15–16px with generous leading. Developers will read it. Don't make them squint.

Rejected: rounded friendly geometrics (Poppins, Nunito), serif "editorial" pairings, script accents, and gradient-filled body text.

## Texture and surface

Acid is never flat. Every surface needs at least one of: **film grain / noise** at low opacity over the entire viewport; **scanlines** or faint horizontal repeats on dark panels; **bloom** — glow bleeding outward from lime and cyan elements; **chromatic aberration** — a 1px red/cyan offset on select display type or image edges; **1px hairline grids**, visible at ~4% white, running the full page so nothing floats free.

Motion is functional, not decorative: text cursors blinking, numbers ticking, a marquee ticker of live stream titles, a waveform or token-stream animation, hover states that snap rather than ease. Transitions are fast (80–140ms) and mostly `steps()` or hard cubic — digital, quantized, never bouncy.

No soft drop shadows. Depth comes from glow and from hard-edged layering, not from CSS shadow blur.

## Layout logic

The organizing metaphor is a **HUD over a broadcast**, not a document. That means:

Edge-to-edge composition with content pushed to the extremes — a persistent top rail and bottom rail with mono telemetry, sections that bleed past the viewport, corner brackets and tick marks framing key modules. Asymmetry over centering: the hero headline hard-left, the live-stream card overlapping it from the right, a rotated sticker label breaking the grid at −7°. Density over whitespace — acid layouts pack information into gridded panels, filmstrip rows, and tabular data blocks, then use one enormous empty black field as contrast, rather than distributing air evenly.

Dividers are 1px lime or grey hairlines, sometimes doubled. Cards are square-cornered or 2px maximum. Everything snaps to a visible 12-column grid whose gutters you can literally see.

Rejected wholesale: the modern SaaS template — centered hero with a subhead and two buttons, 16px-radius cards with pastel gradient borders, isometric illustrations, "Trusted by" logo greyscale rows, three-across feature cards with rounded icons in tinted circles, testimonial carousels with circular avatars.

## The tension to hold

Acid can tip into unreadable poster art. The audience here is working developers evaluating a tool — they need to understand, within eight seconds, that they can *watch someone build with AI and fork the repo*. So: **maximum aggression in the chrome, maximum clarity in the content.** The frame, the type scale, the grain, the glow, the tickers — all acid. The actual sentences, the stream cards, the fork button, the pricing — legible, plain-spoken, engineered. The page should feel like a rave flyer that also happens to be correct documentation.

---

Say the word and I'll build it — full page, single file, in this direction.
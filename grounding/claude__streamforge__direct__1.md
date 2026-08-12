# Acid design — grounding the aesthetic

## Where it comes from

Acid graphics are the visual residue of three lineages colliding. First, **rave and jungle flyer culture** of the early-to-mid nineties: photocopied, over-saturated, illegible-on-purpose, printed on cheap stock in fluorescent spot inks. Second, **chrome-era 3D** — the Y2K liquid-metal blob, the bevelled logotype, the lens-flared wireframe, all the things a Silicon Graphics workstation could do that felt like the future. Third, the **anti-design / post-Swiss reaction** of the 2010s: David Rudnick, Bráulio Amado, Studio Moross, Jonathan Zawada, the Blackletra and Pangram Pangram type foundries, and the whole ecosystem of techno label art where the record sleeve looks like a corrupted CAD file.

What holds these together is a single attitude: **the interface as artifact rather than as service.** Acid design treats a screen the way a rave flyer treats paper — as a surface to be maxed out, not a neutral container to be respected. It is loud on purpose, and its loudness is a filter. It's saying: if this hurts your eyes you are not the audience.

That matters here because the audience *is* the filter. Developers aged 25–40 grew up on this exact visual vocabulary — Winamp skins, demoscene intros, Newgrounds, terminal green, Warp Records sleeves. Acid design flatters them by assuming they can read a dense screen. It is the opposite of the SaaS landing page that treats them as a lead to be nurtured.

## Palette

The core move is **one nuclear accent against near-black, with everything else stripped out.** Not a palette of six harmonised tints — a hostage situation between two colours.

The accent should be a colour that doesn't exist in nature and barely exists in print: acid lime (`#CCFF00`, `#D0FF14`), chartreuse, cyber yellow-green. It reads as radioactive, as highlighter, as terminal phosphor, as hazard tape. Its critical property is that it sits at the very top of the sRGB gamut for perceived luminance — it *glows* on an OLED laptop in a dark room, which is where this page will actually be read.

Against it: not pure black but a black with a cast — `#0A0A0B`, or a very dark cool green-grey, so the background feels like unlit screen rather than ink. Then a mid-grey for body copy (`#8A8F8A`) so the accent never has to compete. A single secondary accent is permissible and useful — a hot magenta or an electric cyan — but it should appear three or four times on the entire page, as a signal of state change (live indicator, error, hover), never as decoration.

Rejected: gradients that blend two brand colours into mush; pastel; the purple-to-blue developer-tool gradient that every AI company shipped in 2023; anything that could be described as "soft." Where gradients appear they should be **duotone or metallic** — a hard chrome ramp with a specular hit, or a two-stop dither, not a smooth cloud.

## Typography

Two voices, held far apart.

**Display: a grotesque pushed to an extreme.** Very tight tracking (negative, `-0.03em` to `-0.05em`), very large, set in all-caps or in a mixed case that ignores grammar. Candidates in the free tier: Archivo Expanded / Archivo Black, Anton, Inter Tight at weight 900, Space Grotesk at its heaviest. The headline should be big enough that it functions as an image — occupying a third of the viewport, with lines stacked so tightly the ascenders and descenders nearly interlock. Optical alignment over metric alignment. Words broken across lines without hyphens if the shape is better.

**Body and UI: a monospace, used everywhere, not just in code blocks.** This is the single most load-bearing decision. When nav labels, metadata, timestamps, button text, and eyebrow labels are all monospace and uppercase at 11–12px with wide positive tracking (`0.1em`+), the page stops reading as marketing and starts reading as instrumentation. JetBrains Mono, Berkeley Mono, IBM Plex Mono, Departure Mono. Numbers should be tabular so counters twitch without reflowing.

Rejected: any humanist sans; anything with a friendly single-storey `a`; two display faces competing; serif "editorial" pull-quotes; the 18px/1.7 Medium-article body block.

Typographic texture comes from **labelling everything.** Sections get numbers (`01 / WATCH`), figures get captions, buttons get keyboard shortcuts, panels get IDs. It's the aesthetic of a system diagram: nothing unlabelled, nothing centred without reason.

## Texture and surface

This direction is not flat and it is not glassmorphic. It is **printed and then scanned.**

The vocabulary: 1px hairline rules in a low-opacity accent, used to draw a visible grid; halftone and Bayer dither instead of smooth blur; scanline overlays at very low opacity; chromatic aberration on a single hero element; noise/grain as a global overlay at 3–6% opacity so no area is ever perfectly clean; hard-edged shapes with no border radius, or a radius so large it's obviously a pill. Drop shadows are absent or they are hard offsets in the accent colour, like misregistered ink.

Motion is **stepped, not eased.** Type that reveals character by character, counters that tick, a live badge that snaps on and off rather than pulsing, cursor blinks at exactly 530ms, marquees that scroll at constant velocity. Where there's easing it should be sharp — a fast-out curve, 120–200ms. Nothing floats, nothing gently fades up on scroll. The reference is a terminal repainting, or a VJ cutting on the beat.

Rejected: soft shadows, frosted glass, rounded 12px cards, gentle 600ms fade-and-rise, blurred colour orbs behind the hero, isometric illustrations of little people.

## Layout logic

The organising principle is a **visible, rigid grid that is then deliberately violated.**

Draw the grid — literally, with hairlines. Then let one or two elements break out: a headline that bleeds off the right edge, an image that overlaps two columns, a rotated label sitting in the gutter, a marquee that runs full-bleed edge to edge and cuts the page in half horizontally. The tension between the strict frame and the escapee is where the energy comes from. Without the visible grid, the violations just look sloppy.

Density is high. Acid layouts don't fear a screen with forty text elements on it, because the hierarchy is carried by scale and colour rather than by whitespace. Padding is asymmetric — generous on one side, tight on another. Vertical rhythm is intentionally interrupted: a very tall hero, then a compressed strip of metadata, then a tall section again. Stacked full-bleed horizontal bands, each with its own internal logic, rather than a uniform centred column of cards.

Chrome is honest about being chrome. Fixed rails at the screen edges with rotated text, a persistent status bar, corner brackets, crosshair marks at grid intersections. The page looks like it's running, not like it's been published.

## What it borrows and what it rejects — stated plainly

It **borrows** from: rave flyers, techno record sleeves, terminal emulators, oscilloscopes, aviation HUDs, warning labels and safety signage, CAD wireframes, Y2K chrome, demoscene intros, and the visual language of piracy and warez.

It **rejects**: the entire Stripe-descended SaaS template. No three-column feature cards with 24px icons. No "Trusted by" logo wall in 40% grey. No smiling stock photography. No centred hero with a subhead and two buttons and a browser mockup floating on a gradient. No "Everything you need to ship faster." No emoji. It also rejects the *other* default — the brutalist-minimal Times New Roman portfolio — because that's low-energy, and this direction is fundamentally about energy.

## How this maps onto Streamforge specifically

The product is unusually well-served by this aesthetic, because the actual subject matter *is* the texture. A stream of Streamforge content is: a prompt being typed, tokens arriving, a diff turning green, a test suite going red then green, a viewer count climbing. All of that is native to a monospace, high-contrast, terminal-adjacent visual world. The design doesn't need to invent decoration — it needs to frame the real artifacts and make them enormous.

Concretely, the aesthetic argues for:

- A hero that is not a screenshot but a **live-feeling composite**: an oversized headline breaking the grid, with a real prompt typing itself out and a diff resolving beside it. The proof of the product is the product.
- The **live indicator as the page's second accent** — a single magenta dot, hard-blinking, used in the nav, on stream cards, in the section labels. It's the one element allowed to be urgent.
- **Fork as a physical action.** The signature interaction of the product deserves a signature treatment: a button with a hard offset shadow, a keyboard shortcut printed on it, a counter that ticks up. Not a ghost button labelled "Learn more."
- **A marquee of what's live right now**, full-bleed, constant velocity, listing repo names and languages and viewer counts in monospace. This does the work of both social proof and product demonstration, and it replaces the logo wall.
- **Numbered sections** (`01 WATCH → 02 FORK → 03 SHIP`) rather than feature cards, so the page reads as a pipeline, which is how developers already think about it.
- Copy that is **declarative and short**, in the register of documentation and release notes rather than marketing. "Watch the prompt. Watch it compile. Take the repo." Not "Unlock the power of collaborative AI development."

The risk to manage: acid design fails when the loudness eats the information. Guardrails — body copy stays at a readable 15–16px in mid-grey with real line-height, the accent never sits under long-form text, and every section has exactly one thing that shouts. Loud shell, legible core.

---

That's the direction. Say the word and I'll build it — I'd start with the hero and the live-streams marquee, since those two set the tone for everything below.
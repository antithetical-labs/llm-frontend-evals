# Acid design, defined before we touch it

## Where it comes from

Acid design is what happened when the rave flyer met the browser. Its lineage runs through late-90s techno and jungle record sleeves, the chrome-and-Y2K graphics of Designers Republic and Wipeout's HUD, early-2000s DVD menus, Winamp skins, and the "Acidwave" wave of 2019–2023 that took all of that and re-rendered it at retina resolution in Blender and Cinema 4D. It is nostalgic for a future that never arrived — the frictionless liquid-metal digital utopia promised by 1999 — and it performs that nostalgia at very high fidelity, which is the joke and the appeal at once.

It borrows: chrome and iridescence, blob and liquid-metal 3D, warped type, gradient meshes, holographic foil, the visual language of technical interfaces (crosshairs, tickers, coordinates, version numbers, monospaced metadata), and the *density* of a club flyer where every square centimeter is doing something.

It rejects: the entire flat-pastel-illustration SaaS consensus. No rounded friendly blobs with smiling faces, no soft drop shadows, no #F9FAFB backgrounds, no lavender-and-sage palettes, no "Simple. Secure. Smart." Also, and this matters here, it rejects the specific visual language of *finance* software — the navy blues, the serif trust signals, the stock photography of people shaking hands, the charts drawn in polite corporate green. That rejection is the strategic core of this project.

## Palette

Acid palettes are built on a **dark, near-black base** — not pure black but a cold charcoal or an ink with a blue or violet bias, so that the accents read as *emitting* light rather than sitting on top of it. Against that, one or two **hyper-saturated accents that hurt slightly**: acid lime, chartreuse, electric cyan, hot magenta, an orange that is nearly signal-red. These are RGB colors, screen-native colors, colors that do not exist in ink. They're used as light sources: glows, edge lighting, ring flare, the bloom around a text glyph.

The third element is **iridescence** — not a color but a gradient behavior. Chrome and holographic surfaces where a single form runs magenta→cyan→lime across its own curvature. This is where the "futuristic" reads from; a flat neon green on black is just a terminal, but a chrome blob catching three neon colors is acid.

Restraint lives in the ratio. The dark base should hold something like 75–80% of the surface. Neon at full saturation over more than a quarter of the page stops being high-energy and becomes unreadable noise, and for a product about money and deadlines, unreadable is fatal. For Backlot specifically I'd run a **single primary acid** (lime-chartreuse, because it reads as "money" without ever saying green-bank-green) plus **one hot secondary** (magenta or electric orange) reserved almost entirely for urgency states — overdue invoices, deadlines inside 48 hours. That gives the palette a job: the product's most important semantic distinction is "fine" versus "you are about to lose money," and the palette can carry it natively.

## Typography

Two voices, hard contrast between them.

**Display:** a wide, tight, technical grotesque — Neue Haas Grotesk Display-adjacent, or better, a *wide* extended sans in the vein of Monument Extended, PP Neue Machina, or Aeonik. Set enormous, tracked tight to negative, in all-caps or sentence case with the leading crushed so lines nearly touch. The headline should feel *engineered* and slightly compressed by its own container. Occasional treatments: chrome fill, outline-only, a single word in the accent color, or a word set in the mono to break rhythm.

**Body and UI:** a monospace or a mono-adjacent grotesque. This is the load-bearing choice for credibility. Monospaced numerals mean the invoice figures align, the dates align, the payout columns align — the type does actual work rather than just signaling "tech." Something like JetBrains Mono, Space Mono, or Söhne Mono. Mono at small sizes with generous letterspacing also produces the *metadata texture* the style depends on: labels like `STATUS: UNPAID`, `PLATFORM_04`, `DUE — T-2D`, version stamps, tiny run-on captions in the margins.

What we do **not** do: no Inter for headlines, no humanist serif, no script or handwriting, no variable-weight "friendly" geometric sans. And crucially — no cute language dressed in the type. The copy should be blunt and short, closer to a spec sheet than to onboarding cheer. This audience is 22–35, fluent in internet irony, and instantly allergic to being spoken to like a small business owner.

## Texture and surface

Acid design is not flat, but its depth is *optical* rather than material. The tools are:

- **Bloom and glow.** Neon elements bleed light into the dark ground. Text shadows in the accent hue at low opacity, layered blurs.
- **Grain and noise.** A fine film grain over the whole page kills the plasticky flatness of pure CSS gradients and makes the darks feel like a photographed screen rather than a hex value.
- **Chrome / liquid metal.** One or two hero objects — a torus, a warped blob, a metallic ribbon — rendered with iridescent environment reflection. In a build without real 3D these can be faked convincingly with layered conic and radial gradients, or sourced as a single hero render.
- **Scanlines, grids, and dot matrices.** Faint repeating structure in the background, at very low contrast. Never decorative enough to compete; just enough that the void has a coordinate system.
- **Halation on edges.** Thin 1px borders in accent color at 20–40% opacity, which read as etched or laser-cut rather than drawn.
- **Sticker and badge layers.** Small rotated elements — a starburst, a `NEW`, a circular rotating word ring — pinned at angles over the grid. This is the flyer inheritance, and it's what keeps it from becoming sterile.

## Layout logic

The underlying grid is strict and visible; the content deliberately violates it. That tension is the whole compositional engine. So: a real 12-column structure with visible rules and gutter marks, and then elements that bleed past the margin, rotate a few degrees, overlap each other, or sit half-off the viewport edge. Type is set to the *edges* of the frame, not politely centered with symmetric whitespace.

Vertical rhythm is uneven on purpose — a suffocatingly dense hero, then a long breath of near-empty dark, then a dense specimen block. Sections don't announce themselves with the same treatment twice; each one gets its own layout personality, held together only by the palette, the type pair, and the grain.

Motion is essential and must be cheap: marquee tickers, a slow-rotating chrome object, counters that tick, hover states that shift hue or invert, a cursor-tracked glow. Nothing bouncy or spring-eased — acid motion is *linear and mechanical*, like machine readout, or *slow and liquid*, like the metal blob. Never both in the same element.

## The tension specific to this product

Backlot handles contracts, invoices, and payouts. Acid design is loud, ironic, and anti-institutional. If we push the style all the way, the product looks like it will lose your money.

So the discipline is: **the marketing surface is acid; the product surface shown inside it is quiet.** Hero, section headers, background, big type, chrome object, tickers — full acid. But every screenshot, table, and data mock we show is dark-neutral, monospaced, tightly aligned, and uses exactly one accent color. The product looks *competent and boring in the good way*, framed by packaging that has energy. That contrast actually sells better than either extreme: it says "this was made by someone who understands your world, and it will not embarrass you in front of a brand's legal team."

Second discipline: **numbers are the hero imagery.** For this audience, the emotional payload isn't an illustration, it's `$14,200 OUTSTANDING · 3 INVOICES OVERDUE · SPONSOR DEADLINE T-2D`. Monospace, huge, acid green. That's the poster.

Third: **accessibility is not optional here.** Neon-on-black is a contrast trap. Acid lime on near-black passes easily; magenta on near-black often doesn't. Body copy stays in a light warm grey at 90%+ opacity, never in the accent. Accent color is for display type, borders, glows, and states — never for paragraphs. Grain and scanline layers stay under ~6% opacity, and all decorative motion respects `prefers-reduced-motion`.

---

That's the ground. Tell me to go and I'll build it — I'd propose a dark ink base around `#0A0B0D`, acid chartreuse `#C6FF3D` as primary, hot magenta `#FF2D8B` reserved for urgency, an extended grotesque for display against JetBrains Mono for everything else, and a hero built around a live-looking payout readout rather than a hero illustration.
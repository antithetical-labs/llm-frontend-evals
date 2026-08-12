# Backlot — Aesthetic Grounding

*Written before any markup. This is the rulebook the page has to obey.*

---

## 1. What "acid design" actually is

Acid design (acid graphics, "acidwave," the current chrome-and-lime revival) is the visual language of the rave flyer rebuilt with 2020s rendering tools. Its lineage is specific: The Designers Republic's work for Warp Records and *WipEout*, mid-90s techno and jungle sleeve art, Y2K liquid-chrome logotypes, DVD menu bevels, hardware-catalog technical drawings, and the aesthetic of a UI that was designed to look like it belonged to a machine you weren't authorized to use.

Its emotional register is **cold surface, high energy underneath**. It is not "playful." It is not "friendly." It looks expensive and slightly hostile, and then it does something absurd — a warped chrome blob, a marquee screaming a build number — so you know it's in on the joke. That combination is exactly right for a 26-year-old who edits ten hours a day, has strong taste, and has been talked down to by every invoicing product they've ever opened.

Critically: acid design is **maximal in decoration and minimal in shape**. Every element is a rectangle, a hairline, or a circle. The intensity comes from color, texture, layering, and typographic scale — never from cute custom shapes. That is what keeps it from becoming a Memphis-pattern startup page.

---

## 2. Palette

The base is **not white**. It's a blue-leaning near-black — around `#08090C` to `#0B0D12` — because acid work assumes an emissive screen, not paper. On top of that:

- **Acid lime as the single signal color.** Something in the `#C9FF3C` / `#D4FF4F` range: aggressive, slightly nauseating, unmistakably digital. This is the brand. It appears on primary actions, active states, and about three words on the entire page. The moment it's used for two different meanings it stops working.
- **Ultraviolet / electric indigo** (`#4B2BFF`–`#6B4BFF`) as the secondary field color — used for large soft glows and gradient meshes behind content, never for text.
- **Chrome:** a silver gradient ramp from `#F4F6F8` through `#9AA3AE` down to `#2A2F38`, with one warm-cool inflection so it reads as reflective metal rather than gray. Chrome is for headline treatments, an object or two, and hairline highlights on card edges.
- **Hot magenta** (`#FF2E88`) as the emergency accent — overdue deadlines, alerts, one crossed-out word. Under 1% of surface area.
- **Neutral grays** for everything that carries actual information: labels, body copy, table values. `#8C93A1` for secondary, `#E6E9EF` for primary text.

Rules: no more than two saturated colors visible in any one viewport. Lime never touches magenta directly. No pastels, no earth tones, no gradient-from-purple-to-pink SaaS hero. Dark mode isn't a mode here — it's the only mode.

---

## 3. Typography

Two families, three voices.

**Display voice:** a wide, tightly-tracked grotesk with mechanical terminals — Archivo Expanded, Anton, or Chakra Petch for the more technical read. Set in **uppercase**, at absurd scale (clamp up to ~12–14vw), with negative letter-spacing so the letters nearly collide. Headlines should feel like they're being extruded through the viewport rather than placed on it. Lines are stacked tight (leading ~0.85) and left-aligned to a hard edge.

**Data voice:** a true monospace — JetBrains Mono, Space Mono, or Geist Mono — used for **all** micro-labels, numbers, currency, dates, platform names, and technical annotation. This is the load-bearing decision. Acid design's texture comes largely from monospace debris: `REF/BL-0092`, `▲ 04 DAYS`, `USD 4,200.00`, `SYS.STATUS: SYNCED`. It reads as instrumentation. For a money product it does double duty — it makes the numbers look accurate.

**Body voice:** the same grotesk at normal width, 15–17px, generous line-height (1.6), gray not white. Deliberately calm. The page yells in the display layer and speaks plainly in the paragraph layer. This is the contrast that makes it usable rather than exhausting.

Rejected outright: humanist serifs, anything rounded and friendly (no Poppins, no Nunito), script or handwriting, and the soft-Inter-everything default. Also rejected: sentence-case marketing headlines with a period at the end.

---

## 4. Texture and surface

Flat design is the enemy here, but so is skeuomorphic gloss. The surface strategy is **layered atmosphere over clinical geometry**:

- **Grain.** A fine noise overlay at 3–6% opacity across the entire page, fixed. It unifies every element, kills banding in gradients, and does more to sell the aesthetic than any single graphic.
- **Bloom.** Large, very soft radial glows (blur radius in the hundreds of pixels) in ultraviolet and lime, sitting behind content, low opacity. Light escaping from behind panels.
- **Chrome objects.** One or two conic/linear-gradient forms — a pill, a torus, a warped bar — that read as rendered metal. Achievable purely in CSS with conic gradients plus blur.
- **Hairlines.** 1px rules at `rgba(255,255,255,0.08)` everywhere: dividers, panel borders, crosshair marks at grid intersections, tick marks along edges. The grid is *visible*. Acid layouts show their construction lines.
- **Scanline / halftone.** Repeating 2–4px horizontal line patterns at very low opacity on select panels. Used once or twice, not everywhere.
- **Glass.** Backdrop-blur panels over the glows, with a 1px light top edge to suggest a bevel catching light.
- **Chromatic fringe.** A faint magenta/cyan offset on one display element — a duplicated headline shifted 2px. Suggests a signal that isn't quite locked.

Rejected: soft box-shadow cards floating on light gray, 3D character illustrations, blob backgrounds, iso-drawings of dashboards, stock photography of anyone smiling at a laptop.

---

## 5. Layout logic

Acid layouts are **grids that get violated on purpose**. The underlying structure is rigid — a 12-column technical grid with visible gutters and hairline column markers. Then specific elements break it: a headline that bleeds past the right edge, a card rotated 1.5°, a ticker running full-bleed edge to edge, a number set so large it's clipped by its own container.

Density is the point. Acid design borrows the information density of technical documentation and equipment panels: everything is labeled, versioned, and numbered, even when the numbers are decorative. Section headers get monospace prefixes (`01 / THE MESS`). Corners get crop marks. Edges get measurement ticks.

Motion follows the same logic: **snap, don't ease**. Fast transitions (120–180ms), stepped counters, marquees at constant velocity, hover states that flip color instantly rather than fading. Nothing bounces. Nothing floats gently. One slow element — a rotating chrome object or a drifting glow — for contrast.

Structurally the page should walk this arc:
1. **Full-bleed hero** — oversized display lockup, one lime CTA, a live-looking data strip underneath. Status bar pinned at the top like a device readout.
2. **Ticker** — full-bleed marquee of the actual pain: `CONTRACT UNSIGNED · INVOICE 41 DAYS LATE · TIKTOK PAYOUT MISSING · WHO OWES ME`.
3. **The mess** — the problem stated in creator language, rendered as a chaotic layered stack of screenshots/notes/DMs, deliberately misaligned.
4. **Product panels** — four modules (Contracts, Invoices, Deadlines, Payouts), each a glass panel containing a *real-looking* UI fragment. Aligned, calm, monospace-heavy. This is where the design proves the product is legible even if the marketing is loud.
5. **Payout ledger** — one wide table showing platform-by-platform money. The hero moment for the audience. Mono, right-aligned figures, lime for paid, magenta for late.
6. **Proof** — creator quotes with follower counts and platform tags, treated as terminal output rather than testimonial cards.
7. **Pricing** — two or three plans as hard-edged rectangles, no rounded corners, one lime-filled.
8. **Closing lockup + footer** — footer as a system readout: version, build, timezone, links in monospace.

---

## 6. The tension I have to manage

This is a **money tool for people who are avoidant about money**. Acid design's default posture is "you are not authorized." That's fine for the marketing frame and lethal for the product surface. So the split is:

- **Chrome, noise, oversized type, tickers, glows** → the marketing frame. Loud, fast, confident, a little arrogant.
- **Numbers, dates, tables, labels** → clinical, high-contrast, monospace, generously spaced, boring on purpose.

Copy follows the same rule. The display type can say `STOP GUESSING WHO OWES YOU`. The body copy must then say, in plain gray sentences, exactly what the product does — no jargon like *reconciliation*, *cash flow visibility*, or *revenue operations*. The audience does not want to feel like they've become a finance person. They want to feel like the finance part has been handled by something that looks cooler than they are.

Accessibility guardrails, non-negotiable: lime is only ever used as a background under near-black text, or as large-scale text on the near-black base. Body copy never drops below `#8C93A1` on `#0B0D12`. Grain and scanlines stay under 8% opacity so they never fight legibility. All motion respects `prefers-reduced-motion` — the tickers stop, the glows hold still.

---

Ready to build. Say go and I'll produce the page as a single self-contained HTML file — no images, all texture and chrome generated in CSS.
## Aesthetic Grounding: Acid Design for Backlot

Before any code, let's define what acid design actually is and why it fits.

**Origins and borrowing.** Acid design descends from 90s rave flyers and acid-house visuals — the smiley, the dayglo, the chaotic collage — filtered through late-2010s "anti-design" poster culture and Y2K tech nostalgia. It borrows from brutalism (exposed structure, visible grids, unapologetic system fonts and monospace), from rave ephemera (chrome liquid blobs, warped type, aggressive color clashes), and from early-web/glitch culture (scanlines, dithering, CRT glow). What it rejects: the soft, pastel, rounded-corner SaaS aesthetic — everything Notion and Stripe look like. No gentle gradients to white, no friendly illustrations of people high-fiving, no "calm productivity" vibes. This matters for Backlot because the audience is 22–35 creators who live in After Effects, Twitch overlays, and TikTok editing apps — their visual language *is* high-energy digital. A tool that looks like enterprise accounting software would signal "not for me" instantly.

**Palette.** The anchor is acid green / chartreuse — that specific electric lime (#C8FF00 / #B4FF00 range) that reads as both toxic and digital. It sits against near-black backgrounds (#0A0A0A to #111), because acid design is almost always dark-mode-native; the brightness comes from the accents, not the canvas. Supporting accents: hot magenta or electric violet for secondary emphasis, plus cyan for data/terminal-feel elements. White is used for body text but sparingly; gray text is kept high-contrast. Color is applied as hard blocks and outlines, not washes.

**Typography.** Two-typeface system, high contrast between them. Display type: a condensed, heavy, uppercase grotesk or a warped tech display face — tight tracking, often stretched or glitched, set enormous. Think posters, not paragraphs. Supporting type: monospace everywhere — labels, buttons, prices, metadata, eyebrows. Monospace is the signature texture of acid design; it makes everything feel like a terminal, a HUD, a receipt. For a finance-adjacent tool this is a gift: invoices and payout numbers in mono read as "accurate data" while the display face screams "not boring accounting." Numbers and money amounts are always mono, often oversized, treated as hero elements.

**Texture and surface.** Visible grid lines and borders — sections separated by 1px rules, often with corner crosshairs or registration marks like a printed flyer or CAD drawing. Dithering/noise overlays, scanline bands, ASCII-art decorations, barcode motifs, starburst stickers, rotating badges. Chrome or liquid-metal blobs used sparingly as accents. Slight glitch effects on hover — RGB-split text, jitter. Marquees (scrolling ticker text) are nearly mandatory. Everything feels like it was output by a machine with attitude.

**Layout logic.** Deliberately "mis-aligned but gridded" — a strict underlying grid with elements that break it: rotated stickers, overlapping labels, type that bleeds off edges, ticket-stub and receipt-like cards with dashed perforation lines. Asymmetry, dense information clusters next to huge empty black space. The page should feel like a dashboard designed by a rave flyer artist: receipts, invoices, and sponsor deals literally rendered as ticket stubs and terminal readouts.

**For Backlot specifically.** The acid direction does real conceptual work: it reframes finance ops (boring, scary) as creator-native tooling (exciting, theirs). Money numbers become HUD readouts. Deadlines become countdown terminals. The message is: "your business, but it looks like your world." Restraint rule: chaos lives in the hero and section decorations; the actual product demo area stays legible — even acid design knows when to shut up and show the tool.

Now the build:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>BACKLOT — Run Your Creator Business Like a Business</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Space+Grotesk:wght@400;500;700&family=Space+Mono:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
<style>
  :root{
    --acid:#C8FF00;
    --acid-dim:#8fb500;
    --magenta:#FF2ED1;
    --violet:#7B3BFF;
    --cyan:#00E5FF;
    --bg:#0A0A0B;
    --bg2:#101012;
    --line:#26262a;
    --txt:#F2F2EF;
    --dim:#9a9a93;
  }
  *{margin:0;padding:0;box-sizing:border-box;}
  html{scroll-behavior:smooth;}
  body{
    background:var(--bg);
    color:var(--txt);
    font-family:'Space Grotesk',sans-serif;
    overflow-x:hidden;
    -webkit-font-smoothing:antialiased;
  }
  ::selection{background:var(--acid);color:#000;}

  /* ---------- global texture ---------- */
  body::before{
    content:"";position:fixed;inset:0;pointer-events:none;z-index:9998;
    background:repeating-linear-gradient(0deg,transparent 0 2px,rgba(0,0,0,.14) 2px 4px);
    mix-blend-mode:overlay;opacity:.5;
  }
  body::after{
    content:"";position:fixed;inset:0;pointer-events:none;z-index:9997;
    background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2'/%3E%3C/filter%3E%3Crect width='120' height='120' filter='url(%23n)' opacity='0.06'/%3E%3C/svg%3E");
    opacity:.6;
  }
  .mono{font-family:'Space Mono',monospace;}

  /* ---------- crosshair / registration marks ---------- */
  .crosshair{position:relative;}
  .crosshair::before,.crosshair::after{
    content:"+";position:absolute;font-family:'Space Mono',monospace;
    color:var(--acid);font-size:14px;line-height:1;z-index:5;
  }
  .crosshair::before{top:-7px;left:-6px;}
  .crosshair::after{bottom:-7px;right:-6px;}

  /* ---------- nav ---------- */
  nav{
    position:fixed;top:0;left:0;right:0;z-index:100;
    display:flex;align-items:center;justify-content:space-between;
    padding:0 28px;height:60px;
    background:rgba(10,10,11,.82);backdrop-filter:blur(14px);
    border-bottom:1px solid var(--line);
  }
  .logo{display:flex;align-items:center;gap:10px;font-family:'Archivo Black',sans-serif;font-size:20px;letter-spacing:-.5px;text-transform:uppercase;}
  .logo .dot{width:12px;height:12px;background:var(--acid);border-radius:50%;box-shadow:0 0 14px var(--acid);animation:pulse 2s infinite;}
  @keyframes pulse{0%,100%{box-shadow:0 0 6px var(--acid);}50%{box-shadow:0 0 20px var(--acid);}}
  .nav-links{display:flex;gap:26px;font-family:'Space Mono',monospace;font-size:12px;text-transform:uppercase;letter-spacing:1px;}
  .nav-links a{color:var(--dim);text-decoration:none;transition:color .2s;position:relative;}
  .nav-links a::before{content:"[";opacity:0;margin-right:2px;color:var(--acid);transition:opacity .2s;}
  .nav-links a::after{content:"]";opacity:0;margin-left:2px;color:var(--acid);transition:opacity .2s;}
  .nav-links a:hover{color:var(--txt);}
  .nav-links a:hover::before,.nav-links a:hover::after{opacity:1;}
  .btn{
    font-family:'Space Mono',monospace;font-size:13px;font-weight:700;text-transform:uppercase;
    letter-spacing:1px;text-decoration:none;cursor:pointer;border:none;
    padding:12px 24px;background:var(--acid);color:#000;
    clip-path:polygon(0 0,calc(100% - 12px) 0,100% 12px,100% 100%,12px 100%,0 calc(100% - 12px));
    transition:transform .15s, background .2s;display:inline-block;
  }
  .btn:hover{transform:translate(-2px,-2px);background:#dfff5c;box-shadow:4px 4px 0 var(--magenta);}
  .btn.ghost{background:transparent;color:var(--acid);outline:1px solid var(--acid);outline-offset:-1px;}
  .btn.ghost:hover{background:rgba(200,255,0,.08);box-shadow:4px 4px 0 var(--violet);}
  @media(max-width:820px){.nav-links{display:none;}}

  /* ---------- hero ---------- */
  header{
    min-height:100svh;display:flex;flex-direction:column;justify-content:center;
    padding:130px 5vw 60px;position:relative;overflow:hidden;
  }
  .hero-grid-bg{
    position:absolute;inset:0;
    background-image:linear-gradient(var(--line) 1px,transparent 1px),linear-gradient(90deg,var(--line) 1px,transparent 1px);
    background-size:80px 80px;
    mask-image:radial-gradient(ellipse 90% 80% at 50% 40%,black 30%,transparent 75%);
    opacity:.5;
  }
  .eyebrow{
    display:inline-flex;align-items:center;gap:10px;
    font-family:'Space Mono',monospace;font-size:12px;letter-spacing:2px;text-transform:uppercase;
    color:var(--acid);border:1px solid var(--acid);padding:7px 14px;width:fit-content;
    background:rgba(200,255,0,.05);margin-bottom:34px;position:relative;z-index:2;
  }
  .eyebrow .blink{width:8px;height:8px;background:var(--acid);animation:blink 1s steps(2) infinite;}
  @keyframes blink{50%{opacity:0;}}
  h1{
    font-family:'Archivo Black',sans-serif;text-transform:uppercase;
    font-size:clamp(46px,9.2vw,132px);line-height:.92;letter-spacing:-.02em;
    position:relative;z-index:2;
  }
  h1 .acid{color:var(--acid);text-shadow:0 0 40px rgba(200,255,0,.4);}
  h1 .stroke{
    color:transparent;-webkit-text-stroke:2px var(--txt);
  }
  h1 .glitch{position:relative;display:inline-block;}
  h1 .glitch::before,h1 .glitch::after{
    content:attr(data-t);position:absolute;left:0;top:0;width:100%;
    overflow:hidden;
  }
  h1 .glitch::before{color:var(--magenta);animation:gl1 3s infinite steps(1);clip-path:inset(0 0 60% 0);}
  h1 .glitch::after{color:var(--cyan);animation:gl2 3.7s infinite steps(1);clip-path:inset(65% 0 0 0);}
  @keyframes gl1{0%,92%{transform:none;opacity:0;}93%{transform:translate(-4px,2px);opacity:.9;}96%{transform:translate(3px,-1px);opacity:.9;}98%,100%{transform:none;opacity:0;}}
  @keyframes gl2{0%,88%{transform:none;opacity:0;}89%{transform:translate(4px,1px);opacity:.9;}93%{transform:translate(-3px,2px);opacity:.9;}95%,100%{transform:none;opacity:0;}}
  .hero-sub{
    max-width:560px;margin-top:34px;font-size:18px;line-height:1.55;color:var(--dim);
    position:relative;z-index:2;
  }
  .hero-sub b{color:var(--txt);}
  .hero-cta{display:flex;gap:16px;margin-top:40px;flex-wrap:wrap;position:relative;z-index:2;align-items:center;}
  .hero-note{font-family:'Space Mono',monospace;font-size:11px;color:var(--dim);letter-spacing:1px;}

  /* chrome blob */
  .blob{
    position:absolute;width:520px;height:520px;right:-140px;top:8%;z-index:1;
    background:radial-gradient(circle at 35% 30%,#e8e8e8 0%,#8a8a8a 25%,#2a2a2e 55%,transparent 72%);
    border-radius:46% 54% 60% 40%/50% 42% 58% 50%;
    filter:blur(1px) contrast(1.2);opacity:.5;
    animation:blobmorph 14s ease-in-out infinite alternate;
  }
  .blob::after{content:"";position:absolute;inset:18%;background:radial-gradient(circle at 40% 35%,var(--acid) 0%,transparent 60%);border-radius:inherit;mix-blend-mode:screen;opacity:.5;}
  @keyframes blobmorph{
    0%{border-radius:46% 54% 60% 40%/50% 42% 58% 50%;transform:rotate(0) scale(1);}
    100%{border-radius:58% 42% 40% 60%/42% 58% 42% 58%;transform:rotate(18deg) scale(1.08);}
  }

  /* ---------- marquee ---------- */
  .marquee{
    border-top:1px solid var(--line);border-bottom:1px solid var(--line);
    background:var(--acid);overflow:hidden;white-space:nowrap;position:relative;z-index:3;
  }
  .marquee-track{display:inline-block;padding:12px 0;animation:scroll 22s linear infinite;}
  .marquee span{
    font-family:'Archivo Black',sans-serif;font-size:16px;text-transform:uppercase;
    color:#000;margin:0 22px;letter-spacing:1px;
  }
  .marquee span.alt{-webkit-text-stroke:1.2px #000;color:transparent;}
  @keyframes scroll{to{transform:translateX(-50%);}}

  /* ---------- section chrome ---------- */
  section{padding:110px 5vw;position:relative;border-bottom:1px solid var(--line);}
  .sec-label{
    font-family:'Space Mono',monospace;font-size:12px;letter-spacing:2px;text-transform:uppercase;
    color:var(--magenta);margin-bottom:16px;display:flex;align-items:center;gap:12px;
  }
  .sec-label::after{content:"";flex:1;max-width:120px;height:1px;background:var(--magenta);}
  h2{
    font-family:'Archivo Black',sans-serif;text-transform:uppercase;
    font-size:clamp(32px,5vw,64px);line-height:1;letter-spacing:-.01em;margin-bottom:18px;
  }
  h2 .acid{color:var(--acid);}
  .sec-sub{color:var(--dim);max-width:520px;font-size:17px;line-height:1.5;}

  /* ---------- pain section ---------- */
  .pain-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:1px;background:var(--line);border:1px solid var(--line);margin-top:56px;}
  .pain-card{background:var(--bg);padding:34px 28px;position:relative;transition:background .25s;}
  .pain-card:hover{background:var(--bg2);}
  .pain-card:hover .pain-num{color:var(--acid);}
  .pain-num{font-family:'Space Mono',monospace;font-size:12px;color:var(--dim);letter-spacing:2px;transition:color .25s;}
  .pain-card h3{font-family:'Archivo Black',sans-serif;font-size:19px;text-transform:uppercase;margin:16px 0 12px;line-height:1.15;}
  .pain-card p{color:var(--dim);font-size:14.5px;line-height:1.55;}
  .pain-card .tag{
    position:absolute;top:14px;right:14px;font-family:'Space Mono',monospace;font-size:10px;
    color:var(--magenta);border:1px solid var(--magenta);padding:3px 8px;letter-spacing:1px;transform:rotate(3deg);
  }

  /* ---------- product / dashboard demo ---------- */
  .demo-wrap{
    margin-top:60px;border:1px solid var(--line);background:var(--bg2);position:relative;
  }
  .demo-bar{
    display:flex;align-items:center;gap:10px;padding:12px 18px;border-bottom:1px solid var(--line);
    font-family:'Space Mono',monospace;font-size:11px;color:var(--dim);letter-spacing:1px;
  }
  .demo-bar .lights{display:flex;gap:6px;}
  .demo-bar .lights i{width:10px;height:10px;border-radius:50%;background:var(--line);}
  .demo-bar .lights i:first-child{background:var(--magenta);}
  .demo-bar .lights i:nth-child(2){background:var(--acid);}
  .demo-bar .lights i:last-child{background:var(--cyan);}
  .demo-body{display:grid;grid-template-columns:1fr 1fr;min-height:380px;}
  @media(max-width:860px){.demo-body{grid-template-columns:1fr;}}
  .demo-left{padding:34px;border-right:1px solid var(--line);}
  @media(max-width:860px){.demo-left{border-right:none;border-bottom:1px solid var(--line);}}
  .demo-h{font-family:'Space Mono',monospace;font-size:11px;letter-spacing:2px;color:var(--dim);text-transform:uppercase;margin-bottom:20px;display:flex;justify-content:space-between;}
  .deal{
    border:1px solid var(--line);padding:16px 18px;margin-bottom:12px;display:flex;
    justify-content:space-between;align-items:center;gap:14px;background:var(--bg);
    transition:border-color .2s, transform .2s;
  }
  .deal:hover{border-color:var(--acid);transform:translateX(6px);}
  .deal .brand{font-weight:700;font-size:15px;}
  .deal .meta{font-family:'Space Mono',monospace;font-size:11px;color:var(--dim);margin-top:4px;}
  .deal .amt{font-family:'Space Mono',monospace;font-size:18px;font-weight:700;color:var(--acid);white-space:nowrap;}
  .pill{font-family:'Space Mono',monospace;font-size:10px;padding:3px 9px;letter-spacing:1px;text-transform:uppercase;white-space:nowrap;}
  .pill.signed{color:var(--acid);border:1px solid var(--acid);}
  .pill.due{color:var(--magenta);border:1px solid var(--magenta);animation:blink 1.4s steps(2) infinite;}
  .pill.paid{color:var(--dim);border:1px solid var(--line);}
  .demo-right{padding:34px;background:
    repeating-linear-gradient(0deg,transparent 0 39px,rgba(38,38,42,.5) 39px 40px);}
  .big-num{
    font-family:'Space Mono',monospace;font-size:clamp(38px,4.5vw,56px);font-weight:700;
    color:var(--acid);text-shadow:0 0 30px rgba(200,255,0,.35);letter-spacing:-2px;
  }
  .stat-row{display:flex;justify-content:space-between;align-items:baseline;border-bottom:1px dashed var(--line);padding:14px 0;font-family:'Space Mono',monospace;font-size:13px;}
  .stat-row .k{color:var(--dim);}
  .stat-row .v{font-weight:700;}
  .stat-row .v.up{color:var(--cyan);}
  .progress{height:8px;background:var(--line);margin-top:8px;position:relative;overflow:hidden;}
  .progress i{position:absolute;inset:0;right:auto;background:var(--acid);width:0;transition:width 1.4s cubic-bezier(.2,.9,.2,1);}
  .progress.mag i{background:var(--magenta);}

  /* ---------- features / receipts ---------- */
  .feat-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:26px;margin-top:60px;}
  .receipt{
    background:var(--bg2);border:1px solid var(--line);padding:30px 26px 34px;position:relative;
    transition:transform .25s;
  }
  .receipt:hover{transform:translateY(-8px) rotate(-.6deg);border-color:var(--acid);}
  .receipt::after{
    content:"";position:absolute;left:0;right:0;bottom:-9px;height:9px;
    background:radial-gradient(circle at 8px -2px,transparent 7px,var(--bg2) 7px);
    background-size:16px 9px;
  }
  .receipt .r-icon{
    width:46px;height:46px;border:1px solid var(--acid);display:grid;place-items:center;
    margin-bottom:22px;background:rgba(200,255,0,.06);
  }
  .receipt .r-icon svg{width:22px;height:22px;stroke:var(--acid);fill:none;stroke-width:1.8;}
  .receipt h3{font-family:'Archivo Black',sans-serif;font-size:18px;text-transform:uppercase;margin-bottom:12px;}
  .receipt p{color:var(--dim);font-size:14.5px;line-height:1.55;}
  .receipt .r-code{
    margin-top:22px;font-family:'Space Mono',monospace;font-size:10px;color:var(--dim);
    letter-spacing:3px;border-top:1px dashed var(--line);padding-top:14px;
    display:flex;justify-content:space-between;
  }
  .barcode{height:22px;background:repeating-linear-gradient(90deg,var(--txt) 0 2px,transparent 2px 5px,var(--txt) 5px 6px,transparent 6px 10px);opacity:.7;width:90px;}

  /* ---------- how it works ---------- */
  .steps{margin-top:60px;border-top:1px solid var(--line);}
  .step{
    display:grid;grid-template-columns:110px 1fr auto;gap:28px;align-items:center;
    padding:30px 10px;border-bottom:1px solid var(--line);transition:background .2s;cursor:default;
  }
  .step:hover{background:rgba(200,255,0,.03);}
  .step .n{
    font-family:'Archivo Black',sans-serif;font-size:44px;color:transparent;
    -webkit-text-stroke:1.5px var(--acid);
  }
  .step h3{font-family:'Archivo Black',sans-serif;font-size:20px;text-transform:uppercase;margin-bottom:8px;}
  .step p{color:var(--dim);font-size:15px;line-height:1.5;max-width:600px;}
  .step .arr{font-family:'Space Mono',monospace;color:var(--acid);font-size:22px;opacity:0;transform:translateX(-10px);transition:.25s;}
  .step:hover .arr{opacity:1;transform:none;}
  @media(max-width:700px){.step{grid-template-columns:70px 1fr;}.step .arr{display:none;}.step .n{font-size:32px;}}

  /* ---------- pricing ---------- */
  .price-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:26px;margin-top:60px;align-items:stretch;}
  .price-card{
    border:1px solid var(--line);background:var(--bg2);padding:36px 30px;position:relative;
    display:flex;flex-direction:column;
  }
  .price-card.hot{border-color:var(--acid);box-shadow:0 0 40px rgba(200,255,0,.12);}
  .price-card .plan{font-family:'Space Mono',monospace;font-size:12px;letter-spacing:2px;text-transform:uppercase;color:var(--dim);}
  .price-card.hot .plan{color:var(--acid);}
  .price-card .amount{font-family:'Space Mono',monospace;font-size:52px;font-weight:700;margin:18px 0 4px;letter-spacing:-2px;}
  .price-card .amount small{font-size:15px;color:var(--dim);letter-spacing:0;}
  .price-card ul{list-style:none;margin:26px 0 30px;flex:1;}
  .price-card li{font-size:14.5px;color:var(--dim);padding:9px 0;border-bottom:1px dashed var(--line);display:flex;gap:10px;}
  .price-card li::before{content:"▸";color:var(--acid);}
  .sticker{
    position:absolute;top:-18px;right:-14px;width:86px;height:86px;background:var(--magenta);
    border-radius:50%;display:grid;place-items:center;text-align:center;
    font-family:'Archivo Black',sans-serif;font-size:11px;text-transform:uppercase;color:#000;
    transform:rotate(12deg);line-height:1.15;animation:spin-slow 9s linear infinite;padding:8px;
  }
  @keyframes spin-slow{to{transform:rotate(372deg);}}

  /* ---------- final cta ---------- */
  .final{
    text-align:center;padding:140px 5vw;position:relative;overflow:hidden;
    background:radial-gradient(ellipse 60% 55% at 50% 55%,rgba(123,59,255,.18),transparent 70%);
  }
  .final h2{font-size:clamp(40px,7vw,96px);}
  .final .sec-sub{margin:22px auto 44px;}
  .final .btn{font-size:15px;padding:18px 42px;}
  .ascii{
    font-family:'Space Mono',monospace;font-size:11px;color:var(--violet);opacity:.8;
    line-height:1.3;margin-top:50px;white-space:pre;letter-spacing:1px;
  }

  /* ---------- footer ---------- */
  footer{
    padding:40px 5vw;display:flex;justify-content:space-between;flex-wrap:wrap;gap:20px;
    font-family:'Space Mono',monospace;font-size:11px;color:var(--dim);letter-spacing:1px;
  }
  footer a{color:var(--dim);text-decoration:none;margin-left:20px;}
  footer a:hover{color:var(--acid);}

  /* reveal */
  .rv{opacity:0;transform:translateY(28px);transition:opacity .7s ease,transform .7s cubic-bezier(.2,.9,.3,1);}
  .rv.in{opacity:1;transform:none;}
</style>
</head>
<body>

<nav>
  <div class="logo"><span class="dot"></span>BACKLOT</div>
  <div class="nav-links">
    <a href="#problem">The Problem</a>
    <a href="#product">Product</a>
    <a href="#features">Features</a>
    <a href="#pricing">Pricing</a>
  </div>
  <a href="#pricing" class="btn">Get Access</a>
</nav>

<!-- HERO -->
<header>
  <div class="hero-grid-bg"></div>
  <div class="blob"></div>
  <div class="eyebrow"><span class="blink"></span> v1.0 // OPS SYSTEM FOR FULL-TIME CREATORS</div>
  <h1>
    <span class="stroke">YOU MAKE</span><br>
    <span class="acid">THE VIDEOS.</span><br>
    <span class="glitch" data-t="WE RUN THE">WE RUN THE</span><br>
    BACK OFFICE.
  </h1>
  <p class="hero-sub">
    Contracts, invoices, sponsor deadlines, and payouts from every platform —
    consolidated into one command center. <b>Built for creators, not accountants.</b>
    No spreadsheets. No missed invoices. No "wait, did that brand ever pay me?"
  </p>
  <div class="hero-cta">
    <a href="#pricing" class="btn">Start Free →</a>
    <a href="#product" class="btn ghost">See the dashboard</a>
    <span class="hero-note mono">// 5 MIN SETUP. NO FINANCE DEGREE REQUIRED.</span>
  </div>
</header>

<!-- MARQUEE -->
<div class="marquee">
  <div class="marquee-track" id="mtrack">
    <span>Contracts ✶</span><span class="alt">Invoices ✶</span><span>Sponsor Deadlines ✶</span><span class="alt">Payout Tracking ✶</span><span>YouTube ✶</span><span class="alt">Twitch ✶</span><span>TikTok ✶</span><span class="alt">Get Paid On Time ✶</span>
  </div>
</div>

<!-- PROBLEM -->
<section id="problem">
  <div class="sec-label">01 / DIAGNOSTIC</div>
  <h2 class="rv">Your business is<br><span class="acid">duct-taped together.</span></h2>
  <p class="sec-sub rv">You're a full-time creator running a real business through DMs, email threads, and a Notes app. Here's what that actually costs you.</p>
  <div class="pain-grid">
    <div class="pain-card crosshair rv">
      <span class="tag">ERROR</span>
      <div class="pain-num mono">LOG_001</div>
      <h3>The invoice you forgot to send</h3>
      <p>The video went live three weeks ago. The brand is happy. You never sent the invoice — and now it feels awkward to ask. That's real money sitting in limbo.</p>
    </div>
    <div class="pain-card crosshair rv">
      <span class="tag">WARN</span>
      <div class="pain-num mono">LOG_002</div>
      <h3>Deadlines living in your head</h3>
      <p>Sponsor read due Thursday. Draft approval Friday. Second deliverable next Tuesday. One bad week and you're apologizing to the partner who pays your rent.</p>
    </div>
    <div class="pain-card crosshair rv">
      <span class="tag">CRIT</span>
      <div class="pain-num mono">LOG_003</div>
      <h3>Five platforms, zero clarity</h3>
      <p>AdSense, Twitch subs, TikTok Creator Rewards, affiliate links, direct deals — you know money is coming in, but you couldn't say how much, from where, or when.</p>
    </div>
    <div class="pain-card crosshair rv">
      <span class="tag">FATAL</span>
      <div class="pain-num mono">LOG_004</div>
      <h3>Tax season panic attack</h3>
      <p>Every April you rebuild a year of finances from bank statements and PayPal exports. It takes a weekend, costs you sleep, and you still miss deductions.</p>
    </div>
  </div>
</section>

<!-- PRODUCT DEMO -->
<section id="product">
  <div class="sec-label">02 / THE SYSTEM</div>
  <h2 class="rv">One screen.<br><span class="acid">Total control.</span></h2>
  <p class="sec-sub rv">Every deal, deadline, and dollar — visible at a glance. This is what Monday morning looks like on Backlot.</p>

  <div class="demo-wrap crosshair rv">
    <div class="demo-bar">
      <div class="lights"><i></i><i></i><i></i></div>
      <span>BACKLOT://DASHBOARD — SYNCED 12 SEC AGO</span>
    </div>
    <div class="demo-body">
      <div class="demo-left">
        <div class="demo-h"><span>ACTIVE DEALS</span><span>Q3 // 2025</span></div>
        <div class="deal">
          <div>
            <div class="brand">Nova Energy Drink</div>
            <div class="meta">60s integration · due in 4 days · invoice sent</div>
          </div>
          <div style="text-align:right"><div class="amt">$4,500</div><span class="pill due">FILMING</span></div>
        </div>
        <div class="deal">
          <div>
            <div class="brand">Keychron</div>
            <div class="meta">Dedicated video · contract countersigned · Net-30</div>
          </div>
          <div style="text-align:right"><div class="amt">$7,200</div><span class="pill signed">SIGNED</span></div>
        </div>
        <div class="deal">
          <div>
            <div class="brand">Skillshare</div>
            <div class="meta">3-month retainer · month 2 payout cleared</div>
          </div>
          <div style="text-align:right"><div class="amt">$3,000</div><span class="pill paid">PAID ✓</span></div>
        </div>
        <div class="deal">
          <div>
            <div class="brand">HelloFresh</div>
            <div class="meta">Shorts package · invoice overdue — auto-chaser sent</div>
          </div>
          <div style="text-align:right"><div class="amt" style="color:var(--magenta)">$1,850</div><span class="pill due">CHASE</span></div>
        </div>
      </div>
      <div class="demo-right">
        <div class="demo-h"><span>THIS MONTH // ALL PLATFORMS</span></div>
        <div class="big-num" id="revnum">$0</div>
        <div style="font-family:'Space Mono',monospace;font-size:11px;color:var(--dim);margin:6px 0 26px;">▲ +18.4% VS LAST MONTH</div>
        <div class="stat-row"><span class="k">BRAND DEALS</span><span class="v">$16,550</span></div>
        <div class="progress"><i data-w="82%"></i></div>
        <div class="stat-row"><span class="k">YOUTUBE ADSENSE</span><span class="v">$5,940</span></div>
        <div class="progress"><i data-w="40%"></i></div>
        <div class="stat-row"><span class="k">TWITCH + TIKTOK</span><span class="v up">$3,112</span></div>
        <div class="progress mag"><i data-w="26%"></i></div>
        <div class="stat-row"><span class="k">OUTSTANDING INVOICES</span><span class="v" style="color:var(--magenta)">$1,850</span></div>
      </div>
    </div>
  </div>
</section>

<!-- FEATURES -->
<section id="features">
  <div class="sec-label">03 / MODULES</div>
  <h2 class="rv">Everything you avoid doing,<br><span class="acid">done.</span></h2>
  <div class="feat-grid">
    <div class="receipt rv">
      <div class="r-icon"><svg viewBox="0 0 24 24"><path d="M6 3h9l4 4v14H6zM15 3v4h4M9 12h7M9 16h7"/></svg></div>
      <h3>Deal Vault</h3>
      <p>Every contract in one place, translated to plain English. Backlot flags usage rights, exclusivity windows, and payment terms — so you know what you actually signed.</p>
      <div class="r-code"><span>MOD_01</span><span class="barcode"></span></div>
    </div>
    <div class="receipt rv">
      <div class="r-icon"><svg viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16"/><path d="M4 9h16M9 9v11"/></svg></div>
      <h3>Invoice Autopilot</h3>
      <p>Generate an invoice from any deal in two clicks. Backlot tracks when it's viewed, nags late payers automatically, and celebrates when the money lands.</p>
      <div class="r-code"><span>MOD_02</span><span class="barcode"></span></div>
    </div>
    <div class="receipt rv">
      <div class="r-icon"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8"/><path d="M12 7v5l3 3"/></svg></div>
      <h3>Deadline Radar</h3>
      <p>Sponsor deliverables on a live countdown. Drafts, approvals, go-live dates — sorted by urgency, pushed to your phone before they become emergencies.</p>
      <div class="r-code"><span>MOD_03</span><span class="barcode"></span></div>
    </div>
    <div class="receipt rv">
      <div class="r-icon"><svg viewBox="0 0 24 24"><path d="M4 19V10M10 19V5M16 19v-8M22 19H2"/></svg></div>
      <h3>Payout Tracker</h3>
      <p>Connect YouTube, Twitch, TikTok, and affiliate networks. See per-platform income monthly, spot trends, and finally know which content actually pays.</p>
      <div class="r-code"><span>MOD_04</span><span class="barcode"></span></div>
    </div>
    <div class="receipt rv">
      <div class="r-icon"><svg viewBox="0 0 24 24"><path d="M12 3l7 4v5c0 5-3.5 8-7 9-3.5-1-7-4-7-9V7z"/></svg></div>
      <h3>Tax-Ready Exports</h3>
      <p>Income and expenses tagged all year. In April, export a clean report your accountant (or TurboTax) can use in minutes — not a shoebox of chaos.</p>
      <div class="r-code"><span>MOD_05</span><span class="barcode"></span></div>
    </div>
    <div class="receipt rv">
      <div class="r-icon"><svg viewBox="0 0 24 24"><path d="M4 12h4l2-6 4 12 2-6h4"/></svg></div>
      <h3>Rate Intelligence</h3>
      <p>See what creators at your size and niche actually charge. Walk into every negotiation with real numbers instead of a guess and a prayer.</p>
      <div class="r-code"><span>MOD_06</span><span class="barcode"></span></div>
    </div>
  </div>
</section>

<!-- HOW IT WORKS -->
<section>
  <div class="sec-label">04 / SEQUENCE</div>
  <h2 class="rv">Live in <span class="acid">five minutes.</span></h2>
  <div class="steps">
    <div class="step rv"><div class="n">01</div><div><h3>Connect your platforms</h3><p>Link YouTube, Twitch, TikTok, and Stripe. Payout history syncs automatically — no CSV uploads, no manual entry.</p></div><div class="arr">→→</div></div>
    <div class="step rv"><div class="n">02</div><div><h3>Drop in your deals</h3><p>Forward a contract or paste the details. Backlot extracts the deadline, deliverables, and payment terms for you.</p></div><div class="arr">→→</div></div>
    <div class="step rv"><div class="n">03</div><div><h3>Never think about it again</h3><p>Invoices go out, late payers get chased, deadlines ping your phone. You just make videos and watch the dashboard fill up.</p></div><div class="arr">→→</div></div>
  </div>
</section>

<!-- PRICING -->
<section id="pricing">
  <div class="sec-label">05 / ACCESS</div>
  <h2 class="rv">Costs less than one<br><span class="acid">forgotten invoice.</span></h2>
  <div class="price-grid">
    <div class="price-card rv">
      <div class="plan">// HOBBYIST</div>
      <div class="amount">$0<small>/mo</small></div>
      <ul>
        <li>Track up to 3 active deals</li>
        <li>Manual invoice creation</li>
        <li>Deadline calendar</li>
        <li>1 platform connection</li>
      </ul>
      <a href="#" class="btn ghost" style="text-align:center">Start Free</a>
    </div>
    <div class="price-card hot rv">
      <div class="sticker">MOST PICKED</div>
      <div class="plan">// FULL-TIME</div>
      <div class="amount">$19<small>/mo</small></div>
      <ul>
        <li>Unlimited deals & contracts</li>
        <li>Auto-invoicing + late-payment chasers</li>
        <li>All platform payout tracking</li>
        <li>Tax-ready exports</li>
        <li>Rate intelligence database</li>
      </ul>
      <a href="#" class="btn" style="text-align:center">Go Full-Time →</a>
    </div>
    <div class="price-card rv">
      <div class="plan">// STUDIO</div>
      <div class="amount">$49<small>/mo</small></div>
      <ul>
        <li>Everything in Full-Time</li>
        <li>Multi-channel & team seats</li>
        <li>Manager/agent collaboration</li>
        <li>Priority support</li>
      </ul>
      <a href="#" class="btn ghost" style="text-align:center">Scale Up</a>
    </div>
  </div>
</section>

<!-- FINAL CTA -->
<section class="final">
  <div class="sec-label" style="justify-content:center;">06 / EXECUTE</div>
  <h2 class="rv">Stop losing money<br>to <span class="acid">your inbox.</span></h2>
  <p class="sec-sub rv">Join 4,000+ full-time creators who know exactly what they're owed, what's due, and what's next.</p>
  <a href="#" class="btn rv">Claim Your Backlot →</a>
  <div class="ascii rv">
╔══════════════════════════════╗
  STATUS: OPERATIONAL ▓▓▓▓▓ 100%
  SPREADSHEETS FOUND: 0
╚══════════════════════════════╝
  </div>
</section>

<footer>
  <span>© 2025 BACKLOT SYSTEMS // BUILT BY CREATORS, FOR CREATORS</span>
  <span><a href="#">TERMS</a><a href="#">PRIVACY</a><a href="#">CONTACT</a><a href="#">X/TWITTER</a></span>
</footer>

<script>
  // duplicate marquee for seamless loop
  const mt = document.getElementById('mtrack');
  mt.innerHTML += mt.innerHTML;

  // scroll reveal
  const io = new IntersectionObserver(es => {
    es.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('in');
        // animate progress bars inside revealed demo
        e.target.querySelectorAll('.progress i').forEach(b => b.style.width = b.dataset.w);
        io.unobserve(e.target);
      }
    });
  }, { threshold: .15 });
  document.querySelectorAll('.rv').forEach(el => io.observe(el));

  // animated revenue counter
  const rev = document.getElementById('revnum');
  const target = 25602;
  const revObs = new IntersectionObserver(es => {
    if (es[0].isIntersecting) {
      const t0 = performance.now(), dur = 1600;
      (function tick(t) {
        const p = Math.min((t - t0) / dur, 1);
        const eased = 1 - Math.pow(1 - p, 3);
        rev.textContent = '$' + Math.round(target * eased).toLocaleString();
        if (p < 1) requestAnimationFrame(tick);
      })(t0);
      revObs.disconnect();
    }
  }, { threshold: .5 });
  revObs.observe(rev);
</script>
</body>
</html>
```

**Delivery notes:**

- **Palette** — true acid chartreuse (`#C8FF00`) on near-black, with magenta and cyan as glitch/alert accents; color applied as hard blocks (marquee band, sticker) rather than gradients.
- **Typography** — Archivo Black for warped-poster display type, Space Mono for every label, number, and money amount. Money is always mono and oversized, per the HUD-readout principle.
- **Acid signatures included** — scanline + noise overlays, glitch-RGB-split on the hero headline, corner crosshair registration marks, ticket-stub receipt cards with perforated edges, barcodes, a rotating starburst sticker, a chrome morphing blob, ASCII-art decoration, and a mandatory scrolling ticker.
- **The one restraint rule held** — the hero and section chrome carry the chaos, but the dashboard demo itself stays clean and legible, because that's where the product has to prove it's a real operations tool and not just a vibe.
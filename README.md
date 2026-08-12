# llm-frontend-evals

What four LLMs produce when you ask for a landing page, measured rather than
eyeballed.

Four models, two briefs, six prompting conditions, five runs each. 240 cells,
239 completed, $44.39 through OpenRouter. Every page is rendered in headless
Chromium at 1440px and measured from computed styles, so the cascade,
inheritance and shorthands resolve before anything is counted.

Writeups: [The most likely page](https://antithetical-labs.com/blog/the-most-likely-page/)

## What is in here

| path | what it is |
|---|---|
| `pages/` | all 239 generated HTML documents, exactly as returned |
| `runs.jsonl` | one row per generation: tokens, cost, seconds, retries |
| `styles.jsonl` | one row per page: the measurements every chart is built from |
| `grounding/` | what each model wrote about the aesthetic before building, for the conditions that ask |
| `house_style/` | generation, measurement, analysis, figures |
| `figures/` | rendered charts and contact sheets |

`shots/` is not committed. It is 325 MB of full-page screenshots and fully
derivable: `python -m house_style.extract` re-renders it from `pages/`.

## Reproducing

```bash
uv sync
uv run playwright install chromium

# measure the committed pages, no API key needed
uv run python -m house_style.extract
uv run python -m house_style.analyse
uv run python -m house_style.post_figures
```

Regenerating the pages themselves costs money and needs an OpenRouter key in
`.env` as `OPENROUTER_API_KEY`:

```bash
uv run python -m house_style.generate --runs 5
```

`generate` is resumable and refuses to run twice at once: it records every
completed cell in `runs.jsonl` and holds a PID lockfile. Both of those exist
because I paid twice for the same pages during a pilot.

## The conditions

| key | what the model is told |
|---|---|
| `bare` | nothing beyond the brief |
| `nudge` | "avoid generic AI-generated aesthetics, make it distinctive" |
| `forbid` | the four most common patterns, banned by name |
| `direct1` | one sentence of positive direction |
| `direct` | the same direction, after a turn spent grounding the aesthetic |
| `skill` | a UI-design skill delivered as a system prompt |

`skill` needs `UI_SKILL_PATH` pointing at a `SKILL.md`; there isn't one vendored
here because it isn't mine to redistribute. It is also not a fair test of that
skill as designed, which is a three-phase interactive workflow rather than a
one-shot system prompt.

## Known limits

- Reasoning effort is pinned low on every model. Left at defaults one model
  spent 16k tokens thinking before writing a tag and another spent under a
  minute, which is an uncontrolled variable.
- Plain HTML and CSS are required, no Tailwind and no React. Utility classes
  push colour and spacing decisions into class names and a framework's default
  scale, which is the thing being measured. Most real frontend work happens in
  Tailwind, so this is a deviation from practice.
- Two briefs can separate genre from model. They cannot characterise a genre.
- One cell never completed, failing identically twice at 16,380 bytes with three
  reported completion tokens. It is left as a gap rather than papered over.

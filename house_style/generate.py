"""Generate pages through OpenRouter.

One provider and one credential for every model, so the experiment is
reproducible by anyone with a single key rather than four.

Nothing retries silently. A truncated stream -- markup that starts and never
closes -- is retried once and the retry is logged, because that is a transport
failure rather than a result. Everything else is recorded as a failure and shows
up as a gap, since a quietly dropped run would bias whichever model failed most.
Every attempt carries its attempt number into runs.jsonl.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import threading
import time
from itertools import product
from pathlib import Path

import httpx
from dotenv import load_dotenv

from .briefs import BRIEFS, CONDITIONS, prompt_for

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "pages"
RUNS = ROOT / "runs.jsonl"
GROUNDING = ROOT / "grounding"

API = "https://openrouter.ai/api/v1/chat/completions"

_WRITE_LOCK = threading.Lock()

MODELS = {
    "claude": "anthropic/claude-opus-5",
    "gpt": "openai/gpt-5.6-sol",
    "kimi": "moonshotai/kimi-k3",
    "gemini": "google/gemini-3.1-pro-preview",
}


def key() -> str:
    load_dotenv(ROOT / ".env")
    k = os.environ.get("OPENROUTER_API_KEY")
    if not k:
        raise SystemExit(
            "OPENROUTER_API_KEY not set. Put it in house-style/.env as\n"
            "  OPENROUTER_API_KEY=sk-or-v1-..."
        )
    return k


def extract_html(text: str) -> str:
    """Pull the HTML document out of whatever the model wrapped it in."""
    fence = re.search(r"```(?:html)?\s*\n(.*?)```", text, re.S)
    if fence:
        text = fence.group(1)
    start = text.lower().find("<!doctype")
    if start == -1:
        start = text.lower().find("<html")
    return text[start:].strip() if start != -1 else text.strip()


# Enough headroom that a full landing page is never clipped. The earlier cap of
# 16000 truncated one model mid-element, and a truncated page is not a cheaper
# datapoint -- it is a billed non-datapoint.
MAX_TOKENS = 32000

# Reasoning is pinned low for every model. Two reasons: the experiment is about
# visual defaults rather than reasoning ability, and left at defaults one model
# spent 16k tokens and fifteen minutes thinking before writing a tag while
# another spent under a minute. That is an uncontrolled variable, not a feature.
REASONING = {"effort": "low"}


def reasoning_for(condition: str) -> dict:
    """Per-condition override of the pinned effort.

    Only forbid-hi uses it. The low-effort forbid pages came back near-blank,
    and two explanations fit equally well: the white documentation page is
    genuinely the next attractor down, or a constrained model on a small
    thinking budget takes the cheapest compliant path. Effort is the only thing
    that differs between the two conditions, so it is the only thing the
    comparison can be about.
    """
    effort = CONDITIONS[condition].get("effort")
    return {"effort": effort} if effort else REASONING


def stream_completion(client: httpx.Client, payload: dict, api_key: str) -> tuple[str, dict]:
    """POST with stream=true and accumulate.

    Streaming is not for progress display -- it is the fix for the failure that
    lost a paid Claude response. A long non-streaming request through a proxy
    can have its connection closed before the body arrives, and the server still
    bills for work it completed.
    """
    chunks: list[str] = []
    usage: dict = {}
    with client.stream("POST", API,
                       headers={"Authorization": f"Bearer {api_key}"},
                       json={**payload, "stream": True,
                             "usage": {"include": True}},
                       timeout=httpx.Timeout(1800.0, connect=30.0)) as r:
        r.raise_for_status()
        for line in r.iter_lines():
            if not line or not line.startswith("data: "):
                continue
            body = line[6:]
            if body.strip() == "[DONE]":
                break
            try:
                obj = json.loads(body)
            except json.JSONDecodeError:
                continue
            if obj.get("usage"):
                usage = obj["usage"]
            for choice in obj.get("choices") or []:
                piece = (choice.get("delta") or {}).get("content")
                if piece:
                    chunks.append(piece)
    return "".join(chunks), usage


def generate(client: httpx.Client, model_key: str, brief: str, condition: str,
             run: int, api_key: str, attempts: int = 2) -> dict:
    """Generate one cell, retrying transport failures.

    Two things count as transport rather than result, and both are retried.

    A document that starts with <!doctype and never reaches </html> is one:
    an observed case delivered 16 KB of markup and then reported 3 completion
    tokens, meaning the stream ended early without raising.

    A dropped connection is the other. The high-effort run lost seven cells in
    a row to RemoteProtocolError when the local link went down, and because
    only RuntimeError was caught, each one died on first contact and billed for
    work already done. Long requests make this likelier: at high effort a cell
    runs 60 to 670 seconds instead of 20, so there is far more window in which
    a link can drop.

    A gap in the grid is not neutral either way. It biases whichever model
    happened to be slowest, which is exactly the one whose behaviour is most
    interesting. Every attempt is recorded, so this retries loudly.
    """
    last: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            return _generate_once(client, model_key, brief, condition, run,
                                  api_key, attempt)
        except (RuntimeError, httpx.TransportError) as e:
            last = e
            if attempt < attempts:
                # A dropped link rarely comes back inside a second, and the
                # request that just died may already have billed, so there is
                # nothing to gain by retrying instantly.
                time.sleep(5 * attempt)
                print(f"  retrying {model_key}/{brief}/{condition}/{run} "
                      f"after: {type(e).__name__}: {e}", flush=True)
    raise last if last else RuntimeError("unreachable")


def _generate_once(client: httpx.Client, model_key: str, brief: str,
                   condition: str, run: int, api_key: str,
                   attempt: int = 1) -> dict:
    system, turns = prompt_for(brief, condition)
    messages = ([{"role": "system", "content": system}] if system else [])

    t0 = time.time()
    in_tok = out_tok = reas_tok = 0
    cost = 0.0
    grounding = None
    text = ""

    # Multi-turn conditions run the same loop; the model's intermediate answer
    # is fed back as an assistant turn. Usage is summed across turns so the
    # cost of the grounding step is attributed to the condition that spends it.
    for i, turn in enumerate(turns):
        messages = messages + [{"role": "user", "content": turn}]
        payload = {"model": MODELS[model_key], "messages": messages,
                   "max_tokens": MAX_TOKENS,
                   "reasoning": reasoning_for(condition)}
        text, usage = stream_completion(client, payload, api_key)
        in_tok += usage.get("prompt_tokens") or 0
        out_tok += usage.get("completion_tokens") or 0
        reas_tok += (usage.get("completion_tokens_details") or {}
                     ).get("reasoning_tokens") or 0
        cost += usage.get("cost") or 0.0
        if i < len(turns) - 1:
            # The grounding answer is kept: what a model believes an aesthetic
            # is, before it builds anything, is its own result.
            grounding = text
            messages = messages + [{"role": "assistant", "content": text}]

    usage = {"prompt_tokens": in_tok, "completion_tokens": out_tok,
             "completion_tokens_details": {"reasoning_tokens": reas_tok},
             "cost": cost}
    html = extract_html(text)

    starts = html.lower().startswith(("<!doctype", "<html"))
    ends = "</html>" in html.lower()
    complete = starts and ends

    name = f"{model_key}__{brief}__{condition}__{run}"
    rec = {
        "name": name, "model_key": model_key, "model": MODELS[model_key],
        "brief": brief, "condition": condition, "run": run,
        "prompt_tokens": usage.get("prompt_tokens"),
        "completion_tokens": usage.get("completion_tokens"),
        "reasoning_tokens": (usage.get("completion_tokens_details") or {}
                             ).get("reasoning_tokens"),
        "cost": usage.get("cost"),
        "seconds": round(time.time() - t0, 1),
        "html_bytes": len(html),
        "complete": complete,
        "turns": len(turns),
        "grounding_chars": len(grounding) if grounding else 0,
        "attempt": attempt,
    }

    # A page missing </html> is a fragment. Writing it would let a truncated
    # document be screenshotted and measured as though it were a design.
    if not complete:
        raise RuntimeError(
            f"incomplete document (starts={starts} ends={ends}, "
            f"{len(html)}B, {rec['completion_tokens']} tok)")

    PAGES.mkdir(exist_ok=True)
    (PAGES / f"{name}.html").write_text(html)
    if grounding:
        GROUNDING.mkdir(exist_ok=True)
        (GROUNDING / f"{name}.md").write_text(grounding)
    # Single write of a single line: append mode plus one write() call is
    # atomic enough for concurrent workers on the same file.
    with _WRITE_LOCK:
        with RUNS.open("a") as f:
            f.write(json.dumps(rec) + "\n")
    return rec


def done() -> set[str]:
    if not RUNS.exists():
        return set()
    return {json.loads(line)["name"] for line in RUNS.read_text().splitlines()
            if line.strip()}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--models", nargs="*", default=list(MODELS))
    ap.add_argument("--briefs", nargs="*", default=list(BRIEFS))
    ap.add_argument("--conditions", nargs="*", default=list(CONDITIONS))
    ap.add_argument("--runs", type=int, default=5)
    args = ap.parse_args()

    # Refuse to run twice at once. Two processes started minutes apart each read
    # an empty runs.jsonl, decided every cell was outstanding, and generated the
    # same pages in parallel -- billed twice, kept once. Resumability alone does
    # not prevent that, because the dedup check happens before either has
    # written anything.
    lock = ROOT / ".generate.lock"
    if lock.exists():
        pid = lock.read_text().strip()
        alive = Path(f"/proc/{pid}").exists() or _pid_alive(pid)
        if alive:
            raise SystemExit(
                f"another generate is already running (pid {pid}). "
                f"Wait for it, or remove {lock} if you are sure it is dead.")
        print(f"clearing stale lock from pid {pid}")
    lock.write_text(str(os.getpid()))

    try:
        _run(args)
    finally:
        lock.unlink(missing_ok=True)


def _pid_alive(pid: str) -> bool:
    try:
        os.kill(int(pid), 0)
    except (OSError, ValueError):
        return False
    return True


def _run(args) -> None:
    api_key = key()
    already = done()
    cells = list(product(args.models, args.briefs, args.conditions,
                         range(1, args.runs + 1)))
    todo = [c for c in cells
            if f"{c[0]}__{c[1]}__{c[2]}__{c[3]}" not in already]
    print(f"{len(cells)} cells, {len(cells) - len(todo)} already done, "
          f"{len(todo)} to run")

    # Progress goes to a file as well as stdout. The first pilot lost its whole
    # diagnostic because the only copy was on a stdout that vanished when the
    # process was backgrounded, leaving a paid failure with no error message.
    log = ROOT / "generate.log"

    def say(msg: str) -> None:
        print(msg, flush=True)
        with log.open("a") as f:
            f.write(msg + "\n")

    failures: list[tuple[str, str]] = []
    spend = 0.0
    state = threading.Lock()

    # One worker per model, each working through its own cells in order.
    # Parallelising by model rather than across all cells keeps concurrent
    # requests to any single provider at one, so this cannot look like a burst
    # to a rate limiter, while still cutting wall-clock roughly fourfold.
    by_model: dict[str, list] = {}
    for cell in todo:
        by_model.setdefault(cell[0], []).append(cell)

    def worker(model_key: str, cells: list) -> None:
        nonlocal spend
        with httpx.Client() as client:
            for _, brief, condition, run in cells:
                label = f"{model_key}/{brief}/{condition}/{run}"
                try:
                    rec = generate(client, model_key, brief, condition, run,
                                   api_key)
                    reas = rec.get("reasoning_tokens")
                    with state:
                        spend += rec.get("cost") or 0.0
                        say(f"  {label:42} "
                            f"{rec['completion_tokens'] or '?':>6} tok"
                            f"{f' (+{reas} reas)' if reas else '':>14}  "
                            f"{rec['seconds']:6.1f}s  "
                            f"${rec.get('cost') or 0:.3f}  "
                            f"[running ${spend:.2f}]")
                except Exception as e:
                    with state:
                        say(f"  {label:42} FAILED {type(e).__name__}: "
                            f"{str(e)[:160]}")
                        failures.append(
                            (label, f"{type(e).__name__}: {str(e)[:200]}"))

    threads = [threading.Thread(target=worker, args=(m, c), daemon=True)
               for m, c in by_model.items()]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    say(f"\ndone: {len(todo) - len(failures)} ok, {len(failures)} failed, "
        f"${spend:.2f} on successful calls (failed calls may also bill)")
    for label, err in failures:
        say(f"  {label}: {err}")


if __name__ == "__main__":
    main()

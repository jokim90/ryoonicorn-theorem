"""Odds-screen photo -> odds dictionary.

Uses the Claude vision API to read the numbers on a photographed odds monitor and return JSON.
Requires ANTHROPIC_API_KEY. Results are checked with model.check_sum, so misreads show up in the UI.
"""
from __future__ import annotations

import base64
import json
import os
import re

PROMPTS = {
    "trio": ("This photo shows a Korean horse-racing TRIO odds screen (삼복승, three horses in any order). "
             "Read every three-horse combination and its odds and answer with a JSON array only, in the form "
             "[{\"h\":[1,2,3],\"o\":45.2}, ...]. Skip combinations whose odds are blank or '-'. JSON only, no explanation."),
    "exa": ("This photo shows a Korean horse-racing EXACTA odds screen (쌍승, 1st and 2nd in exact order). "
            "Read every two-horse combination and its odds and answer with a JSON array only, in the form "
            "[{\"h\":[1,2],\"o\":12.4}, ...] where h[0] is 1st and h[1] is 2nd. JSON only, no explanation."),
    "tri": ("This photo shows a Korean horse-racing TRIFECTA odds screen (삼쌍승, 1st-2nd-3rd in exact order). "
            "Read every three-horse combination and its odds and answer with a JSON array only, in the form "
            "[{\"h\":[1,2,3],\"o\":1234.5}, ...]. Write capped odds (e.g. 9999.9) as shown. JSON only, no explanation."),
}


def _client():
    try:
        import anthropic
    except ImportError as e:
        raise RuntimeError("pip install anthropic is required") from e
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise RuntimeError("Set the ANTHROPIC_API_KEY environment variable")
    return anthropic.Anthropic(api_key=key)


def extract(image_bytes: bytes, pool: str, media_type: str = "image/jpeg", model: str = "claude-sonnet-4-5") -> dict:
    """One photo -> {combination tuple: odds}. If a pool spans several photos, the caller merges with dict.update."""
    client = _client()
    msg = client.messages.create(
        model=model, max_tokens=8000,
        messages=[{"role": "user", "content": [
            {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": base64.b64encode(image_bytes).decode()}},
            {"type": "text", "text": PROMPTS[pool]},
        ]}],
    )
    text = "".join(b.text for b in msg.content if getattr(b, "type", "") == "text")
    m = re.search(r"\[.*\]", text, re.S)
    if not m:
        raise ValueError(f"No JSON found in response: {text[:200]}")
    rows = json.loads(m.group(0))
    out = {}
    for r in rows:
        h = [int(x) for x in r["h"]]
        o = float(r["o"])
        if pool == "trio":
            h = sorted(h)
        key = tuple(h) if len(h) > 1 else h[0]
        out[key] = o
    return out


def parse_manual(text: str, pool: str) -> dict:
    """Parse pasted text instead of a photo. One combination per line: '1-2-3 1234.5' or '1,2,3,1234.5'."""
    out = {}
    for line in text.splitlines():
        nums = re.findall(r"\d+(?:\.\d+)?", line)
        need = 3 if pool in ("trio", "tri") else 2
        if len(nums) < need + 1:
            continue
        h = [int(float(x)) for x in nums[:need]]
        o = float(nums[need])
        if pool == "trio":
            h = sorted(h)
        out[tuple(h)] = o
    return out

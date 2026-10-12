"""배당 화면 사진 → 배당 딕셔너리.

Claude 비전 API로 모니터 사진의 숫자를 JSON으로 추출한다. 키는 ANTHROPIC_API_KEY.
추출 후 model.check_sum 으로 검산하므로 오인식은 화면에서 잡힌다.
"""
from __future__ import annotations

import base64
import json
import os
import re

PROMPTS = {
    "trio": ("이 사진은 한국 경마 삼복승식 배당 화면입니다. 세 마리 말 번호 조합(순서 없음)과 배당을 모두 읽어 "
             "JSON 배열로만 답하세요. 형식: [{\"h\":[1,2,3],\"o\":45.2}, ...]. 배당이 보이지 않거나 '-'면 빼세요. 설명 없이 JSON만."),
    "exa": ("이 사진은 한국 경마 쌍승식 배당 화면입니다. 1착-2착 순서가 있는 두 마리 조합과 배당을 모두 읽어 "
            "JSON 배열로만 답하세요. 형식: [{\"h\":[1,2],\"o\":12.4}, ...] (h[0]=1착, h[1]=2착). 설명 없이 JSON만."),
    "tri": ("이 사진은 한국 경마 삼쌍승식 배당 화면입니다. 1착-2착-3착 순서가 있는 세 마리 조합과 배당을 모두 읽어 "
            "JSON 배열로만 답하세요. 형식: [{\"h\":[1,2,3],\"o\":1234.5}, ...]. 배당 상한 표시(9999.9 등)는 그대로 적으세요. 설명 없이 JSON만."),
}


def _client():
    try:
        import anthropic
    except ImportError as e:
        raise RuntimeError("pip install anthropic 이 필요합니다") from e
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise RuntimeError("ANTHROPIC_API_KEY 환경변수를 설정하세요")
    return anthropic.Anthropic(api_key=key)


def extract(image_bytes: bytes, pool: str, media_type: str = "image/jpeg", model: str = "claude-sonnet-4-5") -> dict:
    """사진 1장 → {조합 튜플: 배당}. 같은 조합이 여러 장에 걸쳐 나오면 호출 측에서 dict.update로 합친다."""
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
        raise ValueError(f"JSON을 찾지 못했습니다: {text[:200]}")
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
    """사진 대신 붙여 넣은 텍스트 파싱. 한 줄에 '1-2-3 1234.5' 또는 '1,2,3,1234.5' 형식."""
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

"""삼쌍승 가치 조합 계산 모듈.

입력: 경주의 삼복승·쌍승·(선택) 단승 배당과 삼쌍승 전 조합 배당
출력: 모든 순서조합의 결합확률, EV, 가치 조합 목록

가중치는 2024년 경주로 학습해 고정한 값(data/weights.json)이며, 논문 3.5절의
조합 단위 조건부 로짓을 그대로 구현한다.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

WEIGHTS_PATH = Path(__file__).resolve().parent.parent / "data" / "weights.json"
TAKEOUT = {"tri": 0.273, "trio": 0.270, "exa": 0.25, "win": 0.20}


def load_weights(path: Path = WEIGHTS_PATH) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


# ---------------------------------------------------------------- 배당 → 확률

def implied_probs(odds: np.ndarray, unique_mask: np.ndarray, valid_mask: np.ndarray):
    """배당 행렬을 풀 내재확률로 바꾼다. 결측/0은 그 풀 최솟값의 절반으로 채운다.
    반환: (확률 행렬, 역산 공제율)"""
    q = np.where(np.isnan(odds) | (odds <= 0), np.nan, 1.0 / odds)
    total = np.nansum(np.where(unique_mask, q, np.nan))
    if not np.isfinite(total) or total <= 0:
        raise ValueError("배당이 비어 있습니다")
    p = q / total
    floor = 0.5 * np.nanmin(np.where(valid_mask, p, np.nan))
    return np.where(np.isnan(p), floor, p), 1 - 1 / total


def sym2(a: np.ndarray) -> np.ndarray:
    return np.fmin(a, a.T)


def sym3(a: np.ndarray) -> np.ndarray:
    b = a.copy()
    for perm in [(0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)]:
        b = np.fmin(b, np.transpose(a, perm))
    return b


def harville_benter(p: np.ndarray, lam: tuple[float, float]) -> np.ndarray:
    """우승확률 → 1-2-3착 순서조합 확률 (논문 3.4절)."""
    p = np.clip(np.asarray(p, float), 1e-6, None)
    p = p / p.sum()
    l2, l3 = lam
    p2, p3 = p ** l2, p ** l3
    s2, s3 = p2.sum(), p3.sum()
    P = (p[:, None, None]
         * (p2[None, :, None] / (s2 - p2[:, None, None]))
         * (p3[None, None, :] / (s3 - p3[:, None, None] - p3[None, :, None])))
    n = len(p)
    I, J, K = np.indices((n, n, n))
    P = np.where((I != J) & (I != K) & (J != K), P, 0.0)
    return P / P.sum()


# ---------------------------------------------------------------- 입력 구조

@dataclass
class RaceOdds:
    """한 경주의 배당. 말 번호는 1부터 n까지 연속이라고 가정(출주 취소마는 제외하고 재번호 없이 NaN)."""
    n: int
    trio: dict[tuple[int, int, int], float] = field(default_factory=dict)   # 순서 없는 세 마리 (a<b<c)
    exa: dict[tuple[int, int], float] = field(default_factory=dict)         # 1착-2착 순서 있음
    tri: dict[tuple[int, int, int], float] = field(default_factory=dict)    # 1-2-3착 순서 있음
    win: dict[int, float] = field(default_factory=dict)                     # 선택
    qnl: dict[tuple[int, int], float] = field(default_factory=dict)         # 선택
    qpl: dict[tuple[int, int], float] = field(default_factory=dict)         # 선택

    def _mat2(self, d, symmetric):
        a = np.full((self.n, self.n), np.nan)
        for (i, j), o in d.items():
            if 1 <= i <= self.n and 1 <= j <= self.n and i != j and o and o > 0:
                a[i - 1, j - 1] = o
        return sym2(a) if symmetric else a

    def _mat3(self, d, symmetric):
        a = np.full((self.n,) * 3, np.nan)
        for (i, j, k), o in d.items():
            if len({i, j, k}) == 3 and all(1 <= x <= self.n for x in (i, j, k)) and o and o > 0:
                a[i - 1, j - 1, k - 1] = o
        return sym3(a) if symmetric else a


# ---------------------------------------------------------------- 핵심 계산

@dataclass
class Result:
    probs: np.ndarray            # (n,n,n) 결합확률, 순서조합
    ev: np.ndarray               # (n,n,n) 결합확률 × 삼쌍승 배당 (배당 없는 곳 NaN)
    tri_odds: np.ndarray
    takeout: dict[str, float]
    model_name: str
    coverage: dict[str, float]   # 풀별 입력된 조합 비율


def compute(race: RaceOdds, weights: dict, model: str = "trio_exa") -> Result:
    """논문 3.5절: P(c) ∝ exp(Σ β_f · ln π_f(c)). model은 weights['weights']의 키."""
    n = race.n
    I, J, K = np.indices((n, n, n))
    valid3 = (I != J) & (I != K) & (J != K)
    uniq3 = (I < J) & (J < K)
    I2, J2 = np.indices((n, n))
    valid2, uniq2 = I2 != J2, I2 < J2

    spec = weights["weights"][model]
    cols, beta = spec["cols"], np.asarray(spec["beta"], float)
    names = weights["names"]
    needed = [names[c] for c in cols]

    feats, takeout, coverage = {}, {}, {}
    sh = (n, n, n)

    if "trio" in needed:
        m = race._mat3(race.trio, True)
        coverage["trio"] = float(np.mean(~np.isnan(m[uniq3])))
        p, t = implied_probs(m, uniq3, valid3); takeout["trio"] = t
        feats["trio"] = np.log(p)
    if "exa" in needed:
        m = race._mat2(race.exa, False)
        coverage["exa"] = float(np.mean(~np.isnan(m[valid2])))
        p, t = implied_probs(m, valid2, valid2); takeout["exa"] = t
        feats["exa"] = np.broadcast_to(np.log(p)[:, :, None], sh)
    if "qnl" in needed:
        m = race._mat2(race.qnl, True)
        p, _ = implied_probs(m, uniq2, valid2)
        feats["qnl"] = np.broadcast_to(np.log(p)[:, :, None], sh)
    if "qpl" in needed:
        m = race._mat2(race.qpl, True)
        p, _ = implied_probs(m, uniq2, valid2); lq = np.log(p)
        feats["qpl"] = lq[:, :, None] + lq[:, None, :] + lq[None, :, :]
    if "win" in needed:
        w = np.array([race.win.get(i + 1, np.nan) for i in range(n)], float)
        q = np.where(np.isnan(w) | (w <= 0), np.nan, 1 / w)
        q = np.where(np.isnan(q), 0.5 * np.nanmin(q), q)
        hb = harville_benter(q / q.sum(), tuple(weights["lam_m"]))
        feats["win"] = np.log(np.where(valid3, hb, 1.0))
    if "tri" in needed:
        m = race._mat3(race.tri, False)
        p, t = implied_probs(m, valid3, valid3); takeout["tri"] = t
        feats["tri"] = np.log(p)
    if "model" in needed:
        raise ValueError("펀더멘털 모형(p_combo)은 경주성적 파이프라인이 필요해 현장 앱에서는 쓰지 않습니다. trio_exa 등을 쓰세요.")

    score = sum(b * feats[names[c]] for c, b in zip(cols, beta))
    score = np.where(valid3, score, -np.inf)
    score -= score[valid3].max()
    probs = np.exp(score); probs /= probs[valid3].sum()

    tri_m = race._mat3(race.tri, False)
    coverage["tri"] = float(np.mean(~np.isnan(tri_m[valid3])))
    if "tri" not in takeout and coverage["tri"] > 0:
        _, takeout["tri"] = implied_probs(tri_m, valid3, valid3)
    ev = np.where(valid3, probs * tri_m, np.nan)
    return Result(probs=probs, ev=ev, tri_odds=tri_m, takeout=takeout, model_name=model, coverage=coverage)


def value_combos(res: Result, threshold: float = 1.4, stake: float = 0.0, pool_total: float | None = None,
                 takeout: float = TAKEOUT["tri"]) -> list[dict]:
    """EV > threshold 인 순서조합 목록 (EV 내림차순).
    stake, pool_total(원)을 주면 논문 8.2절의 시장 충격 반영 배당·EV도 계산한다."""
    n = res.probs.shape[0]
    out = []
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if len({i, j, k}) < 3:
                    continue
                e = res.ev[i, j, k]
                if np.isnan(e) or e <= threshold:
                    continue
                row = {"combo": f"{i+1}-{j+1}-{k+1}", "first": i + 1, "second": j + 1, "third": k + 1,
                       "prob": float(res.probs[i, j, k]), "odds": float(res.tri_odds[i, j, k]), "ev": float(e)}
                if stake and pool_total:
                    a = pool_total * (1 - takeout) / row["odds"]
                    o2 = (pool_total + stake) * (1 - takeout) / (a + stake)
                    row.update(existing_amount=float(a), odds_after=float(o2), ev_after=float(row["prob"] * o2))
                out.append(row)
    out.sort(key=lambda r: -r["ev"])
    return out


def check_sum(odds: dict, expected_takeout: float, tol: float = 0.03) -> dict:
    """OCR 검산: Σ1/배당 가 1/(1−공제율)과 맞는지. 어긋나면 의심 항목(가장 큰 기여)도 돌려준다."""
    vals = {k: v for k, v in odds.items() if v and v > 0}
    if not vals:
        return {"ok": False, "sum": 0, "expected": 1 / (1 - expected_takeout), "suspects": []}
    s = sum(1 / v for v in vals.values()); exp = 1 / (1 - expected_takeout)
    ok = abs(s - exp) / exp <= tol
    suspects = sorted(vals.items(), key=lambda kv: -1 / kv[1])[:5] if not ok else []
    return {"ok": ok, "sum": s, "expected": exp, "implied_takeout": 1 - 1 / s,
            "suspects": [{"combo": k, "odds": v} for k, v in suspects]}

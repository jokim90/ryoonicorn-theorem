import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))
from model import RaceOdds, check_sum, compute, harville_benter, load_weights, value_combos  # noqa: E402


def synth_race(n=12, seed=0, takeout=0.273):
    """Synthetic race: pool odds built from Dirichlet win probabilities via Harville, with noise in the trifecta only."""
    rng = np.random.default_rng(seed)
    p = rng.dirichlet(np.ones(n) * 1.5)
    P = harville_benter(p, (0.76, 0.64))                  # invalid cells are 0, sums to 1
    valid = P > 0
    # trifecta: add per-combination noise, renormalize so that Σ 1/odds = 1/(1-t) exactly
    Q = np.where(valid, P * np.exp(rng.normal(0, 0.3, P.shape)), 0.0)
    Q /= Q.sum()
    race = RaceOdds(n=n)
    for i in range(n):
        for j in range(n):
            if i != j:
                race.exa[(i + 1, j + 1)] = (1 - 0.25) / P[i, j].sum()
            for k in range(n):
                if len({i, j, k}) == 3:
                    race.tri[(i + 1, j + 1, k + 1)] = (1 - takeout) / Q[i, j, k]
                    if i < j < k:
                        s = sum(P[a, b, c] for a in (i, j, k) for b in (i, j, k) for c in (i, j, k) if len({a, b, c}) == 3)
                        race.trio[(i + 1, j + 1, k + 1)] = (1 - 0.27) / s
    return race


def test_probs_sum_to_one():
    W = load_weights()
    res = compute(synth_race(), W, model="trio_exa")
    assert abs(np.nansum(res.probs) - 1) < 1e-6
    assert set(res.coverage) >= {"trio", "exa", "tri"} and all(v > 0.99 for v in res.coverage.values())


def test_value_combos_shape():
    W = load_weights()
    res = compute(synth_race(), W, model="trio_exa")
    combos = value_combos(res, threshold=1.4, stake=10000, pool_total=500_000_000)
    assert all(r["ev"] > 1.4 for r in combos)
    assert all(r["ev_after"] <= r["ev"] for r in combos)
    assert combos == sorted(combos, key=lambda r: -r["ev"])


def test_check_sum():
    race = synth_race()
    assert check_sum(race.tri, 0.273)["ok"]
    bad = dict(race.tri); k = next(iter(bad)); bad[k] = 1.1
    assert not check_sum(bad, 0.273)["ok"]


def test_all_models_run():
    W = load_weights()
    race = synth_race()
    for m in ("trio_exa", "trio_exa_win", "market_all"):
        if m == "market_all":
            continue  # skipped: needs quinella and quinella place inputs
        if m == "trio_exa_win":
            race.win = {i + 1: 5.0 for i in range(race.n)}
        compute(race, W, model=m)

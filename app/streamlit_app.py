"""Ryoonicorn Theorem — upload three odds photos, get the full list of trifecta value combinations.

Run: streamlit run app/streamlit_app.py
"""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent))
from model import RaceOdds, TAKEOUT, check_sum, compute, load_weights, value_combos  # noqa: E402
import ocr  # noqa: E402
import theme  # noqa: E402

_FAVICON = Path(__file__).resolve().parent.parent / "assets" / "favicon.png"
st.set_page_config(page_title="Ryoonicorn Theorem", page_icon=str(_FAVICON) if _FAVICON.exists() else "🦄",
                   layout="centered")
theme.inject(st)
W = load_weights()
LOG = Path(__file__).resolve().parent.parent / "data" / "log.jsonl"

theme.hero(st, "Trifecta value-combination calculator",
           "Three odds screens 7 minutes before the close → every combination with probability × odds above the "
           "threshold. No human picking.")

# ---------------------------------------------------------------- inputs
c1, c2, c3 = st.columns(3)
meet = c1.selectbox("Racecourse", ["Seoul", "Busan-Gyeongnam"])
rc_no = c2.number_input("Race", 1, 20, 1)
n = c3.number_input("Field size", 7, 16, 12)

st.subheader("1. Odds screen photos")
st.caption("Trio (삼복승) · Exacta (쌍승) · Trifecta (삼쌍승). If a pool spans several pages, upload several photos.")
pools = {"trio": "Trio", "exa": "Exacta", "tri": "Trifecta"}
files = {}
cols = st.columns(3)
for col, (k, label) in zip(cols, pools.items()):
    files[k] = col.file_uploader(label, type=["jpg", "jpeg", "png"], accept_multiple_files=True, key=f"f_{k}")

with st.expander("Paste text instead of photos (one per line: '1-2-3 1234.5')"):
    manual = {k: st.text_area(f"{label} odds", key=f"m_{k}", height=80) for k, label in pools.items()}

st.subheader("2. Betting rule")
c1, c2, c3 = st.columns(3)
thr = c1.select_slider("EV threshold", [1.2, 1.3, 1.4, 1.5, 1.6], value=1.4)
stake = c2.selectbox("Stake per combination (KRW)", [1000, 2000, 5000, 10000], index=3)
pool_total = c3.number_input("Trifecta pool size (KRW, if known)", 0, 5_000_000_000, 500_000_000, step=50_000_000)

run = st.button("Compute combinations", type="primary", width="stretch")

# ---------------------------------------------------------------- computation
if run:
    odds = {}
    with st.status("Reading odds…", expanded=True) as status:
        for k, label in pools.items():
            d = {}
            for f in files[k] or []:
                st.write(f"{label}: reading {f.name}")
                d.update(ocr.extract(f.getvalue(), k, media_type=f.type or "image/jpeg"))
            if manual[k].strip():
                d.update(ocr.parse_manual(manual[k], k))
            odds[k] = d
            st.write(f"{label}: {len(d)} combinations")
        status.update(label="Done reading", state="complete")

    if not odds["trio"] or not odds["exa"]:
        st.error("Trio and exacta odds are required.")
        st.stop()

    # sanity check
    st.subheader("3. Sanity check")
    bad = False
    for k, label in pools.items():
        if not odds[k]:
            continue
        chk = check_sum(odds[k], TAKEOUT[k])
        if chk["ok"]:
            st.success(f"{label}: Σ 1/odds {chk['sum']:.3f} (expected {chk['expected']:.3f}) · "
                       f"takeout {chk['implied_takeout']*100:.1f}% · OK")
        else:
            bad = True
            st.warning(f"{label}: Σ 1/odds {chk['sum']:.3f}, expected {chk['expected']:.3f}. Numbers are missing or misread. "
                       "Suspect combinations: " + ", ".join(f"{s['combo']} ({s['odds']})" for s in chk["suspects"]))
    if bad:
        st.info("Computation continues despite the mismatch. Compare suspect combinations with the screen.")

    if not odds["tri"]:
        st.error("EV cannot be computed without trifecta odds. Upload the trifecta screen.")
        st.stop()

    race = RaceOdds(n=int(n), trio=odds["trio"], exa=odds["exa"], tri=odds["tri"])
    res = compute(race, W, model="trio_exa")
    combos = value_combos(res, threshold=thr, stake=stake, pool_total=pool_total or None)

    st.subheader(f"4. Bets — {len(combos)} combinations")
    if len(combos) < 20:
        st.warning("Fewer than 20 value combinations: the rule is to skip this race.")
    if not combos:
        st.stop()

    df = pd.DataFrame(combos)
    show = df[["combo", "prob", "odds", "ev"] + (["odds_after", "ev_after"] if "ev_after" in df else [])].copy()
    show["prob"] = (show["prob"] * 100).map("{:.3f}%".format)
    show["odds"] = show["odds"].map("{:,.1f}".format)
    show["ev"] = show["ev"].map("{:.2f}".format)
    if "ev_after" in show:
        show["odds_after"] = show["odds_after"].map("{:,.0f}".format)
        show["ev_after"] = show["ev_after"].map("{:.2f}".format)
        show.columns = ["Combination (1-2-3)", "Probability", "Current odds", "EV",
                        f"Odds after KRW {stake:,}", "EV after"]
    else:
        show.columns = ["Combination (1-2-3)", "Probability", "Current odds", "EV"]
    st.dataframe(show, hide_index=True, width="stretch")

    total = len(combos) * stake
    exp_ev = df["ev_after"].mean() if "ev_after" in df else df["ev"].mean()
    m1, m2, m3 = st.columns(3)
    m1.metric("Outlay this race", f"KRW {total:,}")
    m2.metric("Model expected return", f"{(exp_ev - 1) * 100:+.0f}%")
    m3.metric("Combined hit probability", f"{df['prob'].sum() * 100:.2f}%")

    st.subheader("5. For the betting terminal")
    st.code("\n".join(r["combo"] for r in combos), language="text")
    csv = "first,second,third,stake\n" + "\n".join(f"{r['first']},{r['second']},{r['third']},{stake}" for r in combos)
    st.download_button("Download CSV", csv, file_name=f"{meet}_R{rc_no}_{datetime.now():%Y%m%d_%H%M}.csv", mime="text/csv")

    # log
    rec = {"ts": datetime.now().isoformat(timespec="seconds"), "meet": meet, "rc_no": int(rc_no), "n": int(n),
           "threshold": thr, "stake": stake, "pool_total": pool_total, "model": res.model_name,
           "takeout": res.takeout, "coverage": res.coverage,
           "combos": [{k: r[k] for k in ("combo", "prob", "odds", "ev")} for r in combos]}
    LOG.parent.mkdir(exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    st.caption(f"Saved to {LOG.name}. After the race, add final odds and the result to the same record "
               "for forward-validation tallies.")

st.divider()
st.markdown(
    '<div class="footnote">Fixed rule: photograph 7 minutes before the close · Ryoonicorn Theorem = trio + exacta '
    "combination model (trained on 2024) · buy every combination above the EV threshold · at most KRW 10,000 per "
    "combination · skip if fewer than 20. Final-odds backtest (2025~, 12 runners) +43%, one hit per 41 races, wide CI. "
    "This tool is not connected to ticket purchasing.</div>",
    unsafe_allow_html=True,
)

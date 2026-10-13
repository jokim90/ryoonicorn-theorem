"""유니콘 정리 (Ryoonicorn Theorem) — 배당 화면 사진 3장으로 삼쌍승 가치 조합 전체 목록을 계산한다.

실행: streamlit run app/streamlit_app.py
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
st.set_page_config(page_title="유니콘 정리 · Ryoonicorn Theorem", page_icon=str(_FAVICON) if _FAVICON.exists() else "🦄",
                   layout="centered")
theme.inject(st)
W = load_weights()
LOG = Path(__file__).resolve().parent.parent / "data" / "log.jsonl"

theme.hero(st, "삼쌍승 가치 조합 계산기",
           "마감 7분 전 배당 화면 3장 → 확률 × 배당이 기준을 넘는 조합 전부. 사람이 고르지 않는다.")

# ---------------------------------------------------------------- inputs
c1, c2, c3 = st.columns(3)
meet_ko = c1.selectbox("경마장", ["서울", "부산경남"])
meet = {"서울": "Seoul", "부산경남": "Busan-Gyeongnam"}[meet_ko]  # 로그 형식은 기존 영문 값 유지
rc_no = c2.number_input("경주 번호", 1, 20, 1)
n = c3.number_input("출전 두수", 7, 16, 12)

st.subheader("1. 배당 화면 사진")
st.caption("삼복승 · 쌍승 · 삼쌍승 화면을 올린다. 한 승식이 여러 화면에 걸치면 사진을 여러 장 올린다.")
pools = {"trio": "삼복승", "exa": "쌍승", "tri": "삼쌍승"}
files = {}
cols = st.columns(3)
for col, (k, label) in zip(cols, pools.items()):
    files[k] = col.file_uploader(label, type=["jpg", "jpeg", "png"], accept_multiple_files=True, key=f"f_{k}")

with st.expander("사진 대신 텍스트로 붙여넣기 (한 줄에 하나: '1-2-3 1234.5')"):
    manual = {k: st.text_area(f"{label} 배당", key=f"m_{k}", height=80) for k, label in pools.items()}

st.subheader("2. 베팅 규칙")
c1, c2, c3 = st.columns(3)
thr = c1.select_slider("기대값(EV) 기준", [1.2, 1.3, 1.4, 1.5, 1.6], value=1.4)
stake = c2.selectbox("조합당 금액 (원)", [1000, 2000, 5000, 10000], index=3)
pool_total = c3.number_input("삼쌍승 매출액 (원, 알면 입력)", 0, 5_000_000_000, 500_000_000, step=50_000_000)

run = st.button("조합 계산하기", type="primary", width="stretch")

# ---------------------------------------------------------------- computation
if run:
    odds = {}
    with st.status("배당 읽는 중…", expanded=True) as status:
        for k, label in pools.items():
            d = {}
            for f in files[k] or []:
                st.write(f"{label}: {f.name} 읽는 중")
                d.update(ocr.extract(f.getvalue(), k, media_type=f.type or "image/jpeg"))
            if manual[k].strip():
                d.update(ocr.parse_manual(manual[k], k))
            odds[k] = d
            st.write(f"{label}: {len(d)}개 조합")
        status.update(label="읽기 완료", state="complete")

    if not odds["trio"] or not odds["exa"]:
        st.error("삼복승과 쌍승 배당은 필수다.")
        st.stop()

    # sanity check
    st.subheader("3. 검산")
    bad = False
    for k, label in pools.items():
        if not odds[k]:
            continue
        chk = check_sum(odds[k], TAKEOUT[k])
        if chk["ok"]:
            st.success(f"{label}: Σ 1/배당 {chk['sum']:.3f} (기대 {chk['expected']:.3f}) · "
                       f"공제율 {chk['implied_takeout']*100:.1f}% · 정상")
        else:
            bad = True
            st.warning(f"{label}: Σ 1/배당 {chk['sum']:.3f}, 기대 {chk['expected']:.3f}. 숫자가 빠졌거나 잘못 읽혔다. "
                       "의심 조합: " + ", ".join(f"{s['combo']} ({s['odds']})" for s in chk["suspects"]))
    if bad:
        st.info("불일치가 있지만 계산은 계속한다. 의심 조합을 화면과 대조하라.")

    if not odds["tri"]:
        st.error("삼쌍승 배당이 없으면 EV를 계산할 수 없다. 삼쌍승 화면을 올려라.")
        st.stop()

    race = RaceOdds(n=int(n), trio=odds["trio"], exa=odds["exa"], tri=odds["tri"])
    res = compute(race, W, model="trio_exa")
    combos = value_combos(res, threshold=thr, stake=stake, pool_total=pool_total or None)

    st.subheader(f"4. 베팅 목록 — {len(combos)}개 조합")
    if len(combos) < 20:
        st.warning("가치 조합이 20개 미만이다. 규칙상 이 경주는 건너뛴다.")
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
        show.columns = ["조합 (1-2-3)", "확률", "현재 배당", "EV",
                        f"{stake:,}원 투입 후 배당", "투입 후 EV"]
    else:
        show.columns = ["조합 (1-2-3)", "확률", "현재 배당", "EV"]
    st.dataframe(show, hide_index=True, width="stretch")

    total = len(combos) * stake
    exp_ev = df["ev_after"].mean() if "ev_after" in df else df["ev"].mean()
    m1, m2, m3 = st.columns(3)
    m1.metric("이번 경주 투입액", f"{total:,}원")
    m2.metric("모형 기대 수익률", f"{(exp_ev - 1) * 100:+.0f}%")
    m3.metric("합산 적중 확률", f"{df['prob'].sum() * 100:.2f}%")

    st.subheader("5. 단말기 입력용")
    st.code("\n".join(r["combo"] for r in combos), language="text")
    csv = "first,second,third,stake\n" + "\n".join(f"{r['first']},{r['second']},{r['third']},{stake}" for r in combos)
    st.download_button("CSV 내려받기", csv, file_name=f"{meet_ko}_R{rc_no}_{datetime.now():%Y%m%d_%H%M}.csv", mime="text/csv")

    # log
    rec = {"ts": datetime.now().isoformat(timespec="seconds"), "meet": meet, "rc_no": int(rc_no), "n": int(n),
           "threshold": thr, "stake": stake, "pool_total": pool_total, "model": res.model_name,
           "takeout": res.takeout, "coverage": res.coverage,
           "combos": [{k: r[k] for k in ("combo", "prob", "odds", "ev")} for r in combos]}
    LOG.parent.mkdir(exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    st.caption(f"{LOG.name}에 저장했다. 경주 후 최종 배당과 결과를 같은 기록에 추가하면 전향 검증 집계에 쓸 수 있다.")

st.divider()
st.markdown(
    '<div class="footnote">고정 규칙: 마감 7분 전 촬영 · 유니콘 정리 = 삼복승 + 쌍승 결합 모형(2024년 학습) · '
    "EV 기준을 넘는 조합 전부 구매 · 조합당 최대 1만 원 · 20개 미만이면 건너뜀. "
    "최종 배당 백테스트(2025~, 12두) +43%, 41경주에 1번 적중, 신뢰구간 매우 넓음. "
    "이 도구는 마권 구매와 연결되어 있지 않다.</div>",
    unsafe_allow_html=True,
)

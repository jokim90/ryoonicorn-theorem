"""삼쌍승 가치 조합 — 사진 3장 넣으면 구매 목록이 나온다.

실행: streamlit run app/streamlit_app.py
"""
from __future__ import annotations

import io
import json
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent))
from model import RaceOdds, TAKEOUT, check_sum, compute, load_weights, value_combos  # noqa: E402
import ocr  # noqa: E402

st.set_page_config(page_title="삼쌍승 가치 조합", page_icon="🐎", layout="centered")
W = load_weights()
LOG = Path(__file__).resolve().parent.parent / "data" / "log.jsonl"

st.title("삼쌍승 가치 조합")
st.caption("마감 7분 전 배당 화면 3장 → 결합확률 × 배당 > 기준인 조합 전부. 사람이 고르지 않습니다.")

# ---------------------------------------------------------------- 입력
c1, c2, c3 = st.columns(3)
meet = c1.selectbox("경마장", ["서울", "부산경남"])
rc_no = c2.number_input("경주", 1, 20, 1)
n = c3.number_input("출주 두수", 7, 16, 12)

st.subheader("1. 배당 화면 사진")
st.caption("삼복승 · 쌍승 · 삼쌍승 세 가지. 한 승식이 여러 페이지면 여러 장 올리세요.")
pools = {"trio": "삼복승", "exa": "쌍승", "tri": "삼쌍승"}
files = {}
cols = st.columns(3)
for col, (k, label) in zip(cols, pools.items()):
    files[k] = col.file_uploader(label, type=["jpg", "jpeg", "png"], accept_multiple_files=True, key=f"f_{k}")

with st.expander("사진 대신 텍스트로 넣기 (한 줄에 '1-2-3 1234.5')"):
    manual = {k: st.text_area(f"{label} 배당", key=f"m_{k}", height=80) for k, label in pools.items()}

st.subheader("2. 구매 기준")
c1, c2, c3 = st.columns(3)
thr = c1.select_slider("EV 기준", [1.2, 1.3, 1.4, 1.5, 1.6], value=1.4)
stake = c2.selectbox("조합당 금액(원)", [1000, 2000, 5000, 10000], index=3)
pool_total = c3.number_input("삼쌍승 풀 매출(원, 알면)", 0, 5_000_000_000, 500_000_000, step=50_000_000)

run = st.button("조합 계산", type="primary", use_container_width=True)

# ---------------------------------------------------------------- 계산
if run:
    odds = {}
    with st.status("배당 읽는 중…", expanded=True) as status:
        for k, label in pools.items():
            d = {}
            for f in files[k] or []:
                st.write(f"{label}: {f.name} 인식 중")
                d.update(ocr.extract(f.getvalue(), k, media_type=f.type or "image/jpeg"))
            if manual[k].strip():
                d.update(ocr.parse_manual(manual[k], k))
            odds[k] = d
            st.write(f"{label}: {len(d)}개 조합")
        status.update(label="인식 완료", state="complete")

    if not odds["trio"] or not odds["exa"]:
        st.error("삼복승과 쌍승 배당은 반드시 필요합니다.")
        st.stop()

    # 검산
    st.subheader("3. 검산")
    bad = False
    for k, label in pools.items():
        if not odds[k]:
            continue
        chk = check_sum(odds[k], TAKEOUT[k])
        if chk["ok"]:
            st.success(f"{label}: 1/배당 합 {chk['sum']:.3f} (기대 {chk['expected']:.3f}) · 공제율 {chk['implied_takeout']*100:.1f}% · 정상")
        else:
            bad = True
            st.warning(f"{label}: 1/배당 합 {chk['sum']:.3f}, 기대 {chk['expected']:.3f}. 숫자가 빠졌거나 잘못 읽혔습니다. "
                       f"의심 조합: " + ", ".join(f"{s['combo']} ({s['odds']})" for s in chk["suspects"]))
    if bad:
        st.info("검산이 어긋나도 계산은 진행합니다. 의심 조합은 화면과 대조하세요.")

    race = RaceOdds(n=int(n), trio=odds["trio"], exa=odds["exa"], tri=odds["tri"])
    res = compute(race, W, model="trio_exa")
    combos = value_combos(res, threshold=thr, stake=stake, pool_total=pool_total or None)

    st.subheader(f"4. 구매 목록 — {len(combos)}개")
    if not odds["tri"]:
        st.error("삼쌍승 배당이 없으면 EV를 계산할 수 없습니다. 삼쌍승 화면을 올리세요.")
        st.stop()
    if len(combos) < 20:
        st.warning("가치 조합이 20개 미만이면 이 경주는 건너뛰는 것이 규칙입니다.")

    df = pd.DataFrame(combos)
    show = df[["combo", "prob", "odds", "ev"] + (["odds_after", "ev_after"] if "ev_after" in df else [])].copy()
    show["prob"] = (show["prob"] * 100).map("{:.3f}%".format)
    show["odds"] = show["odds"].map("{:,.1f}".format)
    show["ev"] = show["ev"].map("{:.2f}".format)
    if "ev_after" in show:
        show["odds_after"] = show["odds_after"].map("{:,.0f}".format); show["ev_after"] = show["ev_after"].map("{:.2f}".format)
        show.columns = ["조합(1-2-3착)", "결합확률", "현재 배당", "EV", f"{stake:,}원 후 배당", "그 후 EV"]
    else:
        show.columns = ["조합(1-2-3착)", "결합확률", "현재 배당", "EV"]
    st.dataframe(show, hide_index=True, use_container_width=True)

    total = len(combos) * stake
    exp_ev = df["ev_after"].mean() if "ev_after" in df else df["ev"].mean()
    m1, m2, m3 = st.columns(3)
    m1.metric("이 경주 지출", f"{total:,}원")
    m2.metric("모형 기대 수익률", f"{(exp_ev - 1) * 100:+.0f}%")
    m3.metric("합산 적중 확률", f"{df['prob'].sum() * 100:.2f}%")

    st.subheader("5. 발매기 입력용")
    st.code("\n".join(r["combo"] for r in combos), language="text")
    csv = "first,second,third,stake\n" + "\n".join(f"{r['first']},{r['second']},{r['third']},{stake}" for r in combos)
    st.download_button("CSV 내려받기", csv, file_name=f"{meet}_{rc_no}R_{datetime.now():%Y%m%d_%H%M}.csv", mime="text/csv")

    # 기록
    rec = {"ts": datetime.now().isoformat(timespec="seconds"), "meet": meet, "rc_no": int(rc_no), "n": int(n),
           "threshold": thr, "stake": stake, "pool_total": pool_total, "model": res.model_name,
           "takeout": res.takeout, "coverage": res.coverage,
           "combos": [{k: r[k] for k in ("combo", "prob", "odds", "ev")} for r in combos]}
    LOG.parent.mkdir(exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    st.caption(f"기록 저장: {LOG.name} · 경주 후 확정 배당과 착순을 같은 경주에 추가하면 전향 검증 집계에 쓰입니다.")

st.divider()
st.caption("규칙(고정): 마감 7분 전 촬영 · 삼복승+쌍승 결합 모형(2024년 학습) · EV 기준 이상 전부 구매 · 조합당 1만 원 이하 · 20개 미만이면 건너뜀. "
           "최종 배당 백테스트(2025~, 12두) +43%, 41경주당 1회 적중, 신뢰구간 넓음. 이 도구는 마권 구매와 연결되지 않습니다.")

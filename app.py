import pandas as pd
import streamlit as st
import altair as alt

st.set_page_config(
    page_title="대한민국 재정 통합 분석",
    layout="wide"
)

# =========================
# 데이터
# =========================
years = list(range(2011, 2025))

df = pd.DataFrame({
    "연도": years,

    "총수입": [
        323.0, 341.8, 351.9, 356.4, 371.8,
        401.8, 430.6, 465.3, 473.1, 478.8,
        570.5, 617.8, 573.9, 594.5
    ],

    "총지출": [
        304.4, 323.3, 337.7, 347.9, 372.0,
        384.9, 406.6, 434.1, 485.1, 549.9,
        601.0, 682.4, 610.7, 638.0
    ],

    "통합재정수지": [
        18.6, 18.5, 14.2, 8.5, -0.2,
        16.9, 24.0, 31.2, -12.0, -71.2,
        -30.5, -64.6, -36.8, -43.5
    ],

    "관리재정수지": [
        -13.5, -17.4, -21.1, -29.5, -38.0,
        -22.7, -18.5, -10.6, -54.4, -112.0,
        -90.6, -117.0, -87.0, -104.8
    ]
})

# =========================
# LHS (총수입/총지출)
# =========================
lhs_df = df.melt(
    id_vars="연도",
    value_vars=["총수입", "총지출"],
    var_name="지표",
    value_name="값"
)

lhs = alt.Chart(lhs_df).mark_line(point=True, strokeWidth=3).encode(
    x=alt.X("연도:O"),
    y=alt.Y(
        "값:Q",
        title="총수입 / 총지출 (LHS, 조 원)"
    ),
    color=alt.Color("지표:N")
)

# =========================
# RHS (재정수지) — 핵심 수정 부분
# =========================
rhs_df = df.melt(
    id_vars="연도",
    value_vars=["통합재정수지", "관리재정수지"],
    var_name="지표",
    value_name="값"
)

# 👉 0 기준을 아래로 내리기 위한 "shift"
rhs_df["shifted"] = rhs_df["값"] - 200  # 기준 하향 (시각적 이동)

rhs = alt.Chart(rhs_df).mark_bar(opacity=0.5).encode(
    x=alt.X("연도:O"),
    y=alt.Y(
        "shifted:Q",
        title="재정수지 (RHS, 조 원)",
        axis=alt.Axis(
            labelOverlap=True,
            tickCount=5
        ),
        scale=alt.Scale(zero=False)
    ),
    color=alt.Color("지표:N")
)

# =========================
# 결합 (dual axis 구조)
# =========================
chart = alt.layer(
    lhs,
    rhs
).resolve_scale(
    y="independent"
).properties(
    height=650
)

# =========================
# Streamlit
# =========================
st.title("🇰🇷 대한민국 재정 통합 분석 대시보드")

st.markdown("""
- LHS: 총수입 / 총지출  
- RHS: 통합재정수지 / 관리재정수지 (하방 이동 적용)
""")

st.altair_chart(chart, use_container_width=True)

with st.expander("데이터"):
    st.dataframe(df)

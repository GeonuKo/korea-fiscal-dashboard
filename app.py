import pandas as pd
import streamlit as st
import altair as alt

st.set_page_config(
    page_title="대한민국 재정 통합 분석",
    layout="wide"
)

# =========================
# 1. 데이터 생성
# =========================
years = list(range(2011, 2025))

df = pd.DataFrame({
    "year": years,

    "total_revenue": [
        323.0, 341.8, 351.9, 356.4, 371.8,
        401.8, 430.6, 465.3, 473.1, 478.8,
        570.5, 617.8, 573.9, 594.5
    ],

    "total_expenditure": [
        304.4, 323.3, 337.7, 347.9, 372.0,
        384.9, 406.6, 434.1, 485.1, 549.9,
        601.0, 682.4, 610.7, 638.0
    ],

    "fiscal_balance": [
        18.6, 18.5, 14.2, 8.5, -0.2,
        16.9, 24.0, 31.2, -12.0, -71.2,
        -30.5, -64.6, -36.8, -43.5
    ],

    "managed_balance": [
        -13.5, -17.4, -21.1, -29.5, -38.0,
        -22.7, -18.5, -10.6, -54.4, -112.0,
        -90.6, -117.0, -87.0, -104.8
    ]
})

# =========================
# 2. long format 변환
# =========================
df_long = df.melt(
    id_vars="year",
    value_vars=[
        "total_revenue",
        "total_expenditure",
        "fiscal_balance",
        "managed_balance"
    ],
    var_name="indicator",
    value_name="value"
)

# =========================
# 3. 차트 생성
# =========================
chart = (
    alt.Chart(df_long)
    .mark_line(point=True, strokeWidth=2)
    .encode(
        x=alt.X("year:O", title="연도"),
        y=alt.Y("value:Q", title="조 원", scale=alt.Scale(zero=False)),
        color=alt.Color("indicator:N", title="재정 지표"),
        tooltip=["year", "indicator", "value"]
    )
    .properties(height=600)
)

# =========================
# 4. Streamlit UI
# =========================
st.title("🇰🇷 대한민국 재정 통합 분석 대시보드")
st.caption("총수입 · 총지출 · 통합재정수지 · 관리재정수지 (2011~2024)")

st.altair_chart(chart, use_container_width=True)

# =========================
# 5. 데이터 테이블
# =========================
with st.expander("데이터 보기"):
    st.dataframe(df, use_container_width=True)

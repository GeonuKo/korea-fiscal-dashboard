import pandas as pd
import streamlit as st
import altair as alt

st.set_page_config(
    page_title="대한민국 재정 통합 분석",
    layout="wide"
)

# =========================
# 1. 데이터
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
# 2. line chart (총수입/총지출)
# =========================
line_df = df.melt(
    id_vars="연도",
    value_vars=["총수입", "총지출"],
    var_name="지표",
    value_name="값"
)

line_chart = alt.Chart(line_df).mark_line(point=True, strokeWidth=3).encode(
    x=alt.X("연도:O", title="연도"),
    y=alt.Y("값:Q", title="조 원"),
    color=alt.Color("지표:N", title="수입/지출"),
    tooltip=["연도", "지표", "값"]
)

# =========================
# 3. bar chart (재정수지)
# =========================
balance_df = df.melt(
    id_vars="연도",
    value_vars=["통합재정수지", "관리재정수지"],
    var_name="지표",
    value_name="값"
)

bar_chart = alt.Chart(balance_df).mark_bar(opacity=0.5).encode(
    x=alt.X("연도:O"),
    y=alt.Y("값:Q", axis=alt.Axis(title="재정수지 (조 원)")),
    color=alt.Color("지표:N", title="재정수지"),
    tooltip=["연도", "지표", "값"]
)

# =========================
# 4. dual axis 결합
# =========================
combined = alt.layer(
    line_chart,
    bar_chart
).resolve_scale(
    y="independent"
).properties(
    height=600
)

# =========================
# 5. Streamlit 출력
# =========================
st.title("🇰🇷 대한민국 재정 통합 대시보드")
st.caption("총수입·총지출(선) + 통합재정수지·관리재정수지(막대)")

st.altair_chart(combined, use_container_width=True)

with st.expander("데이터 보기"):
    st.dataframe(df, use_container_width=True)

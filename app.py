import pandas as pd
import streamlit as st
import altair as alt

st.set_page_config(
    page_title="대한민국 국가 재정통계",
    layout="wide"
)

# =========================
# 사이드바
# =========================
menu = st.sidebar.radio(
    "대한민국 국가 재정통계",
    ["대한민국 국가 재정통계", "국가 재정 기본 개념", "총수입", "총지출"]
)

# =========================
# 데이터 (2011~2024 재정수지)
# =========================
years_fin = list(range(2011, 2025))

df_fin = pd.DataFrame({
    "연도": years_fin,
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
# LHS 선 차트 (총수입/총지출)
# =========================
lhs_df = df_fin.melt(
    id_vars="연도",
    value_vars=["총수입", "총지출"],
    var_name="지표",
    value_name="값"
)

lhs = alt.Chart(lhs_df).mark_line(
    point=True,
    strokeWidth=3
).encode(
    x=alt.X("연도:O"),
    y=alt.Y("값:Q", title="총수입 / 총지출 (LHS, 조 원)"),
    color=alt.Color("지표:N")
)

# =========================
# RHS 바 차트 (통합 / 관리)
# =========================
rhs_df = df_fin.melt(
    id_vars="연도",
    value_vars=["통합재정수지", "관리재정수지"],
    var_name="지표",
    value_name="값"
)

rhs = alt.Chart(rhs_df).mark_bar(
    size=10,   # 바 폭 증가
    opacity=0.85
).encode(
    x=alt.X("연도:O"),
    xOffset=alt.XOffset(
        "지표:N",
        scale=alt.Scale(
            paddingInner=0.05,   # 바 간격 더 좁힘
            paddingOuter=0.1
        )
    ),
    y=alt.Y(
        "값:Q",
        title="재정수지 (RHS, 조 원)",
        scale=alt.Scale(domain=[-200, 200])
    ),
    color=alt.Color(
        "지표:N",
        scale=alt.Scale(
            domain=["통합재정수지", "관리재정수지"],
            range=["#1f77b4", "#d62728"]
        )
    )
)

# =========================
# 결합 (선 + 바 유지)
# =========================
finance_chart = alt.layer(lhs, rhs).resolve_scale(
    y="independent"
).properties(height=800)

# =========================
# 국가채무
# =========================
debt_total = {
    2011: 420.5, 2012: 443.1, 2013: 489.8, 2014: 533.2,
    2015: 591.5, 2016: 626.9, 2017: 660.2, 2018: 680.5,
    2019: 723.2, 2020: 846.6, 2021: 970.7, 2022: 1067.4,
    2023: 1126.8, 2024: 1175.0
}

debt_gdp = {
    2011: 29.0, 2012: 29.5, 2013: 31.2, 2014: 32.5,
    2015: 34.0, 2016: 34.2, 2017: 34.1, 2018: 33.9,
    2019: 35.4, 2020: 41.1, 2021: 43.7, 2022: 45.9,
    2023: 46.9, 2024: 46.0
}

df_debt = pd.DataFrame({
    "연도": list(debt_total.keys()),
    "국가채무": list(debt_total.values()),
    "GDP대비국가채무": list(debt_gdp.values())
})

debt_bar = alt.Chart(df_debt).mark_bar().encode(
    x=alt.X("연도:O"),
    y=alt.Y("국가채무:Q", title="국가채무 (조 원, LHS)")
)

debt_line = alt.Chart(df_debt).mark_line(
    point=True,
    strokeWidth=3,
    color="red"
).encode(
    x=alt.X("연도:O"),
    y=alt.Y("GDP대비국가채무:Q", title="GDP 대비 국가채무 (%)")
)

debt_chart = alt.layer(debt_bar, debt_line).resolve_scale(
    y="independent"
).properties(height=600)

# =========================
# 화면
# =========================
if menu == "대한민국 국가 재정통계":

    st.title("대한민국 국가 재정통계")

    st.subheader("재정수지 (총수입 / 총지출 / 통합 / 관리)")
    st.altair_chart(finance_chart, use_container_width=True)

    st.subheader("국가채무 및 GDP 대비 비율")
    st.altair_chart(debt_chart, use_container_width=True)

elif menu == "국가 재정 기본 개념":
    st.title("국가 재정 기본 개념")
    st.info("빈 화면")

elif menu == "총수입":
    st.title("총수입")
    st.info("빈 화면")

elif menu == "총지출":
    st.title("총지출")
    st.info("빈 화면")

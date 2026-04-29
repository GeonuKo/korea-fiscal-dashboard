import pandas as pd
import streamlit as st
import altair as alt

# =========================
# 페이지 설정
# =========================
st.set_page_config(
    page_title="대한민국 국가 재정통계",
    layout="wide"
)

# =========================
# 데이터 로드 (메모리 업데이트 데이터 반영)
# =========================
@st.cache_data
def load_all_data():
    # 1. 재정수지 기본 데이터 (기존 데이터)
    years = list(range(2011, 2025))
    df_base = pd.DataFrame({
        "연도": years,
        "총수입": [323.0, 341.8, 351.9, 356.4, 371.8, 401.8, 430.6, 465.3, 473.1, 478.8, 570.5, 617.8, 573.9, 594.5],
        "총지출": [304.4, 323.3, 337.7, 347.9, 372.0, 384.9, 406.6, 434.1, 485.1, 549.9, 601.0, 682.4, 610.7, 638.0],
        "통합재정수지": [18.6, 18.5, 14.2, 8.5, -0.2, 16.9, 24.0, 31.2, -12.0, -71.2, -30.5, -64.6, -36.8, -43.5],
        "관리재정수지": [-13.5, -17.4, -21.1, -29.5, -38.0, -22.7, -18.5, -10.6, -54.4, -112.0, -90.6, -117.0, -87.0, -104.8],
        "국가채무": [420.5, 443.1, 489.8, 533.2, 591.5, 626.9, 660.2, 680.5, 723.2, 846.6, 970.7, 1067.4, 1126.8, 1175.0],
        "GDP대비국가채무": [29.0, 29.5, 31.2, 32.5, 34.0, 34.2, 34.1, 33.9, 35.4, 41.1, 43.7, 45.9, 46.9, 46.0]
    })

    # 2. 총수입 상세 요약 데이터 (제공 데이터 통합)
    years_ext = list(range(2013, 2026))
    tax_income = [201.9, 205.5, 217.9, 242.6, 265.4, 293.6, 293.5, 285.5, 344.1, 395.9, 344.1, 367.3, 382.4]
    non_tax = [45.1, 44.5, 45.0, 52.3, 53.0, 55.0, 48.0, 50.0, 54.0, 60.0, 52.0, 55.0, 57.0]
    fund_income = [150.0, 155.0, 163.0, 175.0, 185.0, 195.0, 210.0, 225.0, 245.0, 260.0, 235.0, 245.0, 272.8]

    df_total_detail = pd.DataFrame({
        "연도": years_ext,
        "국세수입": tax_income,
        "세외수입": non_tax,
        "기금수입": fund_income
    })

    # 3. 주요 국세 항목 데이터
    tax_items = pd.DataFrame({
        "항목": ["소득세", "법인세", "부가가치세", "상속세", "관세", "교통세", "기타"],
        "금액": [126.8, 88.3, 87.6, 14.5, 8.4, 15.1, 41.7],
        "분류": "국세수입"
    })

    return df_base, df_total_detail, tax_items

df_base, df_total_detail, tax_items = load_all_data()

# =========================
# 사이드바
# =========================
menu = st.sidebar.radio(
    "대한민국 국가 재정통계",
    ["메인 대시보드", "국가 재정 기본 개념", "총수입 상세", "총지출 상세"]
)

# =========================
# 화면 라우팅
# =========================
if menu == "메인 대시보드":
    st.title("대한민국 국가 재정통계")
    st.subheader("재정수지 (총수입 / 총지출 / 통합 / 관리)")

    line_df = df_base.melt(id_vars="연도", value_vars=["총수입", "총지출"], var_name="지표", value_name="값")
    line_chart = alt.Chart(line_df).mark_line(point=True, strokeWidth=3).encode(
        x=alt.X("연도:O", title="연도"),
        y=alt.Y("값:Q", title="총수입 / 총지출 (LHS, 조 원)"),
        color=alt.Color("지표:N")
    )

    bar_df = df_base.melt(id_vars="연도", value_vars=["통합재정수지", "관리재정수지"], var_name="수지구분", value_name="수지값")
    bar_chart = alt.Chart(bar_df).mark_bar(opacity=0.7).encode(
        x=alt.X("연도:O"),
        y=alt.Y("수지값:Q", scale=alt.Scale(domain=[-200, 200]), title="재정수지 (RHS, 조 원)"),
        color=alt.Color("수지구분:N"),
        xOffset="수지구분:N"
    )

    combined = alt.layer(line_chart, bar_chart).resolve_scale(y="independent").properties(height=500)
    st.altair_chart(combined, use_container_width=True)

elif menu == "총수입 상세":
    st.title("💰 총수입 상세 분석")
    st.markdown("제공된 결산 및 본예산 데이터를 기반으로 대한민국 총수입의 구조를 분석합니다.")

    st.subheader("1. 연도별 총수입 구성 추이")
    df_melted = df_total_detail.melt(id_vars="연도", var_name="수입원", value_name="금액")
    
    stack_chart = alt.Chart(df_melted).mark_bar().encode(
        x=alt.X("연도:O"),
        y=alt.Y("금액:Q", title="금액 (조 원)"),
        color=alt.Color("수입원:N", scale=alt.Scale(scheme='tableau10')),
        tooltip=["연도", "수입원", "금액"]
    ).properties(height=400)
    
    st.altair_chart(stack_chart, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("2. 2025 국세수입 주요 비중")
        pie_chart = alt.Chart(tax_items).mark_arc(innerRadius=50).encode(
            theta=alt.Theta(field="금액", type="quantitative"),
            color=alt.Color(field="항목", type="nominal"),
            tooltip=["항목", "금액"]
        ).properties(height=400)
        st.altair_chart(pie_chart, use_container_width=True)

    with col2:
        st.subheader("3. 2025 총수입 재원별 비중")
        latest_data = df_total_detail.iloc[-1]
        source_data = pd.DataFrame({
            "Source": ["국세수입", "세외수입", "기금수입"],
            "Value": [latest_data["국세수입"], latest_data["세외수입"], latest_data["기금수입"]]
        })
        donut = alt.Chart(source_data).mark_arc(innerRadius=70).encode(
            theta="Value:Q",
            color="Source:N",
            tooltip=["Source", "Value"]
        ).properties(height=400)
        st.altair_chart(donut, use_container_width=True)

    st.subheader("4. 주요 국세 항목(소득·법인·부가세) 추이")
    tax_trend = pd.DataFrame({
        "연도": [2021, 2022, 2023, 2024, 2025],
        "소득세": [114.1, 128.7, 115.8, 117.4, 126.8],
        "법인세": [70.4, 103.6, 80.4, 62.5, 88.3],
        "부가가치세": [71.2, 81.6, 73.8, 82.2, 87.6]
    }).melt(id_vars="연도", var_name="세목", value_name="조원")

    tax_line = alt.Chart(tax_trend).mark_line(point=True).encode(
        x="연도:O",
        y=alt.Y("조원:Q", title="금액 (조 원)"),
        color="세목:N",
        tooltip=["연도", "세목", "조원"]
    ).properties(height=400)
    st.altair_chart(tax_line, use_container_width=True)

elif menu == "국가 재정 기본 개념":
    st.title("📖 국가 재정 기본 개념")
    st.info("재정수지와 국가채무에 대한 상세 설명 섹션입니다.")

elif menu == "총지출 상세":
    st.title("💸 총지출 상세 분석")
    st.info("총지출 관련 상세 데이터 업데이트 대기 중입니다.")

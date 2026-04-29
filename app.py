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
# 데이터 로드 및 전처리
# =========================
@st.cache_data
def load_all_data():
    # [데이터 1] 재정수지 기본 데이터
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

    # [데이터 2] 총수입 상세 요약 (2025 본예산 포함)
    years_ext = list(range(2013, 2026))
    df_total_detail = pd.DataFrame({
        "연도": years_ext,
        "국세수입": [201.9, 205.5, 217.9, 242.6, 265.4, 293.6, 293.5, 285.5, 344.1, 395.9, 344.1, 367.3, 382.4],
        "세외수입": [45.1, 44.5, 45.0, 52.3, 53.0, 55.0, 48.0, 50.0, 54.0, 60.0, 52.0, 55.0, 57.0],
        "기금수입": [150.0, 155.0, 163.0, 175.0, 185.0, 195.0, 210.0, 225.0, 245.0, 260.0, 235.0, 245.0, 272.8]
    })

    # [데이터 3] 2025 국세수입 상세
    tax_2025 = pd.DataFrame({
        "항목": ["소득세", "법인세", "부가가치세", "상속세", "관세", "교통세", "기타"],
        "금액": [126.8, 88.3, 87.6, 14.5, 8.4, 15.1, 41.7]
    })
    tax_2025['비중'] = (tax_2025['금액'] / tax_2025['금액'].sum() * 100).round(1)

    # [데이터 4] 2025 기금수입 상세
    fund_2025 = pd.DataFrame({
        "항목": ["사회보장기여금", "재산수입", "경상이전수입", "융자원금회수", "재화용역판매", "기타"],
        "금액": [96.5, 45.7, 39.6, 37.1, 10.9, 43.0]
    })
    fund_2025['비중'] = (fund_2025['금액'] / fund_2025['금액'].sum() * 100).round(1)

    # [데이터 5] 주요 국세 항목 추이 (2021-2025)
    tax_trend = pd.DataFrame({
        "연도": [2021, 2022, 2023, 2024, 2025],
        "소득세": [114.1, 128.7, 115.8, 117.4, 126.8],
        "법인세": [70.4, 103.6, 80.4, 62.5, 88.3],
        "부가가치세": [71.2, 81.6, 73.8, 82.2, 87.6]
    }).melt(id_vars="연도", var_name="세목", value_name="조원")

    return df_base, df_total_detail, tax_2025, fund_2025, tax_trend

df_base, df_total_detail, tax_2025, fund_2025, tax_trend = load_all_data()

# =========================
# 사이드바
# =========================
menu = st.sidebar.radio("대한민국 국가 재정통계", ["메인 대시보드", "총수입 상세", "총지출 상세"])

# =========================
# 화면 구성: 총수입 상세
# =========================
if menu == "총수입 상세":
    st.title("💰 총수입 상세 분석")

    # 1. 연도별 총수입 구성 추이 (숫자 라벨 추가)
    st.subheader("1. 연도별 총수입 구성 추이 (단위: 조 원)")
    df_melted = df_total_detail.melt(id_vars="연도", var_name="수입원", value_name="금액")
    
    base = alt.Chart(df_melted).encode(x=alt.X("연도:O"))
    bars = base.mark_bar().encode(
        y=alt.Y("금액:Q", stack="zero"),
        color=alt.Color("수입원:N"),
        tooltip=["연도", "수입원", "금액"]
    )
    labels = base.mark_text(dy=5, color='white', baseline='top', fontWeight='bold').encode(
        y=alt.Y("금액:Q", stack="zero"),
        text=alt.Text("금액:Q", format=".1f"),
        detail="수입원:N"
    )
    st.altair_chart((bars + labels).properties(height=500), use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        # 2. 2025 국세수입 주요 비중 (TOP 3 라벨링)
        st.subheader("2. 2025 국세수입 주요 비중")
        tax_2025 = tax_2025.sort_values("금액", ascending=False)
        tax_2025['label'] = tax_2025.apply(lambda x: f"{x['항목']}\n{x['금액']}조({x['비중']}%)" if x.name in tax_2025.head(3).index else "", axis=1)
        
        pie_tax = alt.Chart(tax_2025).mark_arc(outerRadius=120).encode(
            theta=alt.Theta("금액:Q"),
            color=alt.Color("항목:N", legend=alt.Legend(title="세목")),
            tooltip=["항목", "금액", "비중"]
        )
        text_tax = pie_tax.mark_text(radius=150, size=13, fontWeight='bold').encode(text="label:N")
        st.altair_chart((pie_tax + text_tax).properties(height=450), use_container_width=True)

    with col2:
        # 3. 2025 기금수입 주요 비중 (TOP 3 라벨링)
        st.subheader("3. 2025 기금수입 주요 비중")
        fund_2025 = fund_2025.sort_values("금액", ascending=False)
        fund_2025['label'] = fund_2025.apply(lambda x: f"{x['항목']}\n{x['금액']}조({x['비중']}%)" if x.name in fund_2025.head(3).index else "", axis=1)
        
        pie_fund = alt.Chart(fund_2025).mark_arc(outerRadius=120, innerRadius=50).encode(
            theta=alt.Theta("금액:Q"),
            color=alt.Color("항목:N", legend=alt.Legend(title="기금항목")),
            tooltip=["항목", "금액", "비중"]
        )
        text_fund = pie_fund.mark_text(radius=150, size=13, fontWeight='bold').encode(text="label:N")
        st.altair_chart((pie_fund + text_fund).properties(height=450), use_container_width=True)

    # 4. 주요 국세 항목 추이 (포인트 위 숫자 라벨 추가)
    st.subheader("4. 주요 국세 항목(소득·법인·부가세) 추이")
    line_base = alt.Chart(tax_trend).encode(
        x=alt.X("연도:O"),
        y=alt.Y("조원:Q", title="금액 (조 원)"),
        color="세목:N"
    )
    lines = line_base.mark_line(point=True, strokeWidth=3)
    points_labels = line_base.mark_text(dy=-15, fontWeight='bold', size=12).encode(
        text=alt.Text("조원:Q", format=".1f")
    )
    st.altair_chart((lines + points_labels).properties(height=450), use_container_width=True)

elif menu == "메인 대시보드":
    st.title("대한민국 국가 재정통계")
    st.info("메인 요약 지표 화면입니다.")

elif menu == "총지출 상세":
    st.title("💸 총지출 상세 분석")
    st.warning("데이터 업데이트 준비 중입니다.")

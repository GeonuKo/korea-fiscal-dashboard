import pandas as pd
import streamlit as st
import altair as alt

# =========================
# 페이지 설정
# =========================
st.set_page_config(
    page_title="대한민국 국가 재정통계",
    page_icon="📊",
    layout="wide"
)

# =========================
# 데이터 로드 및 전처리
# =========================
@st.cache_data
def load_comprehensive_data():
    # 1. 메인 재정지표 (총수입/총지출/수지)
    years_base = list(range(2011, 2025))
    df_base = pd.DataFrame({
        "연도": years_base,
        "총수입": [323.0, 341.8, 351.9, 356.4, 371.8, 401.8, 430.6, 465.3, 473.1, 478.8, 570.5, 617.8, 573.9, 594.5],
        "총지출": [304.4, 323.3, 337.7, 347.9, 372.0, 384.9, 406.6, 434.1, 485.1, 549.9, 601.0, 682.4, 610.7, 638.0],
        "관리재정수지": [-13.5, -17.4, -21.1, -29.5, -38.0, -22.7, -18.5, -10.6, -54.4, -112.0, -90.6, -117.0, -87.0, -104.8]
    })

    # 2. 12대 분야별 총지출 (제공 데이터)
    # 단위: 조 원
    field_data = {
        "연도": [2022, 2023, 2024, 2025, 2026],
        "보건·복지·고용": [217.7, 226.0, 242.9, 248.7, 269.1],
        "교육": [84.2, 96.3, 89.8, 98.5, 99.9],
        "일반·지방행정": [98.1, 112.2, 110.5, 110.7, 121.4],
        "국방": [54.6, 57.0, 59.4, 61.2, 65.9],
        "R&D": [29.8, 31.1, 26.5, 29.6, 35.5],
        "산업·중소·에너지": [31.3, 26.0, 28.0, 28.2, 31.8],
        "SOC": [28.0, 25.0, 26.4, 25.4, 27.7],
        "농림·수산·식품": [23.7, 24.4, 25.4, 25.9, 28.0]
    }
    df_field = pd.DataFrame(field_data)

    # 3. 회계구분별 지출 (제공 데이터)
    # 단위: 조 원
    df_acc_type = pd.DataFrame({
        "회계연도": [2023, 2024, 2025],
        "일반회계": [369.4, 356.5, 365.3],
        "특별회계": [71.6, 81.7, 82.1],
        "기금": [197.7, 218.4, 225.9]
    })

    # 4. 2023년 소관별(부처별) 결산 TOP 10
    # 단위: 억원 -> 조원 환산
    df_dept = pd.DataFrame({
        "소관명": ["보건복지부", "교육부", "행정안전부", "국토교통부", "국방부", "고용노동부", "기획재정부", "인사혁신처", "과학기술정보통신부", "산업통상자원부"],
        "지출금액": [110.9, 91.5, 72.3, 51.6, 41.0, 33.6, 29.7, 25.2, 19.0, 11.2]
    })

    return df_base, df_field, df_acc_type, df_dept

df_base, df_field, df_acc_type, df_dept = load_comprehensive_data()

# =========================
# 사이드바 메뉴
# =========================
st.sidebar.title("🇰🇷 재정통계 분석")
menu = st.sidebar.radio(
    "메뉴 선택",
    ["메인 대시보드", "총수입 상세", "총지출 상세", "부처별 상세 분석"]
)

# =========================
# 1. 메인 대시보드
# =========================
if menu == "메인 대시보드":
    st.title("📊 대한민국 국가 재정 대시보드")
    
    # 주요 지표 (KPI)
    latest_exp = df_base["총지출"].iloc[-1]
    prev_exp = df_base["총지출"].iloc[-2]
    delta = round(latest_exp - prev_exp, 1)
    
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    col_kpi1.metric("최근 결산 총지출 (2024)", f"{latest_exp} 조원", f"{delta} 조원")
    col_kpi2.metric("관리재정수지", f"{df_base['관리재정수지'].iloc[-1]} 조원", help="국가 재정 건강성을 나타내는 핵심 지표")
    col_kpi3.metric("2026 예산(안)", "727.9 조원")

    st.markdown("---")
    
    # 메인 차트: 총수입 vs 총지출
    st.subheader("연도별 재정 규모 추이")
    base_melted = df_base.melt(id_vars="연도", value_vars=["총수입", "총지출"], var_name="구분", value_name="금액")
    main_chart = alt.Chart(base_melted).mark_line(point=True, strokeWidth=3).encode(
        x=alt.X("연도:O", title="연도"),
        y=alt.Y("금액:Q", title="금액 (조 원)"),
        color=alt.Color("구분:N", scale=alt.Scale(range=['#4C78A8', '#E15759'])),
        tooltip=["연도", "구분", "금액"]
    ).properties(height=450)
    st.altair_chart(main_chart, use_container_width=True)

# =========================
# 2. 총수입 상세 (기존 코드 유지)
# =========================
elif menu == "총수입 상세":
    st.title("💰 총수입 상세 분석")
    st.info("국세수입 및 기금수입 등 세입 구조를 분석합니다.")
    # (이전 단계에서 작성한 총수입 로직 삽입 가능)

# =========================
# 3. 총지출 상세 (신규 업데이트)
# =========================
elif menu == "총지출 상세":
    st.title("💸 총지출 상세 분석")
    st.markdown("제공된 데이터를 바탕으로 **분야별, 회계별** 지출 구조를 심층 분석합니다.")

    # (1) 12대 분야별 추이 분석
    st.subheader("1. 주요 분야별 지출 추이 (2022-2026)")
    field_melted = df_field.melt(id_vars="연도", var_name="분야", value_name="지출액")
    
    field_chart = alt.Chart(field_melted).mark_line(point=True).encode(
        x="연도:O",
        y=alt.Y("지출액:Q", title="금액 (조 원)"),
        color=alt.Color("분야:N", legend=alt.Legend(columns=2, orient='bottom')),
        tooltip=["연도", "분야", "지출액"]
    ).properties(height=500).interactive()
    
    st.altair_chart(field_chart, use_container_width=True)

    st.markdown("---")
    
    col_a, col_b = st.columns(2)

    with col_a:
        # (2) 회계구분별 비중 (2025 본예산 기준)
        st.subheader("2. 회계구분별 지출 비중 (2025)")
        acc_2025 = df_acc_type[df_acc_type["회계연도"] == 2025].iloc[0, 1:]
        acc_df = pd.DataFrame({"회계명": acc_2025.index, "금액": acc_2025.values})
        
        acc_pie = alt.Chart(acc_df).mark_arc(innerRadius=70).encode(
            theta=alt.Theta(field="금액", type="quantitative"),
            color=alt.Color(field="회계명", type="nominal", scale=alt.Scale(scheme='set2')),
            tooltip=["회계명", "금액"]
        ).properties(height=400)
        st.altair_chart(acc_pie, use_container_width=True)

    with col_b:
        # (3) 2026년 예산 요구안 vs 본예산 비교
        st.subheader("3. 2026년 총지출 의사결정")
        compare_data = pd.DataFrame({
            "단계": ["각 부처 요구안", "정부 편성 본예산"],
            "금액": [695.1, 727.9]
        })
        
        comp_bar = alt.Chart(compare_data).mark_bar(size=50).encode(
            x=alt.X("단계:N", axis=alt.Axis(labelAngle=0)),
            y=alt.Y("금액:Q", title="조 원", scale=alt.Scale(domain=[600, 750])),
            color=alt.Color("단계:N", legend=None),
            text=alt.Text("금액:Q", format=".1f")
        ).properties(height=400)
        
        st.altair_chart(comp_bar + comp_bar.mark_text(dy=-10), use_container_width=True)

# =========================
# 4. 부처별 상세 분석 (신규 업데이트)
# =========================
elif menu == "부처별 상세 분석":
    st.title("🏢 소관 부처별 지출 분석")
    st.markdown("어떤 정부 부처가 가장 많은 예산을 집행하는지 확인합니다.")

    # (1) TOP 10 부처 트리맵/바 차트
    st.subheader("2023년 결산 기준 지출 규모 상위 10개 부처")
    
    dept_chart = alt.Chart(df_dept).mark_bar().encode(
        y=alt.Y("소관명:N", sort="-x", title="정부 부처"),
        x=alt.X("지출금액:Q", title="결산 금액 (조 원)"),
        color=alt.Color("지출금액:Q", scale=alt.Scale(scheme='blues')),
        tooltip=["소관명", "지출금액"]
    ).properties(height=500)
    
    st.altair_chart(dept_chart, use_container_width=True)

    # (2) 상세 데이터 테이블
    with st.expander("데이터 전체 보기"):
        st.table(df_dept)

# =========================
# 하단 푸터
# =========================
st.sidebar.markdown("---")
st.sidebar.caption("Data Source: 기획재정부 예결산 시스템 자료 기반")

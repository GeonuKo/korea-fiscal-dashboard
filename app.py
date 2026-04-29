import pandas as pd
import streamlit as st
import altair as alt

# =========================
# 페이지 설정 및 스타일
# =========================
st.set_page_config(
    page_title="대한민국 국가 재정통계 대시보드",
    layout="wide"
)

# =========================
# 데이터 통합 및 전처리
# =========================
@st.cache_data
def get_data():
    years = list(range(2011, 2025))
    
    # 재정수지 및 채무 통합 데이터
    data = {
        "연도": years,
        "총수입": [323.0, 341.8, 351.9, 356.4, 371.8, 401.8, 430.6, 465.3, 473.1, 478.8, 570.5, 617.8, 573.9, 594.5],
        "총지출": [304.4, 323.3, 337.7, 347.9, 372.0, 384.9, 406.6, 434.1, 485.1, 549.9, 601.0, 682.4, 610.7, 638.0],
        "통합재정수지": [18.6, 18.5, 14.2, 8.5, -0.2, 16.9, 24.0, 31.2, -12.0, -71.2, -30.5, -64.6, -36.8, -43.5],
        "관리재정수지": [-13.5, -17.4, -21.1, -29.5, -38.0, -22.7, -18.5, -10.6, -54.4, -112.0, -90.6, -117.0, -87.0, -104.8],
        "국가채무": [420.5, 443.1, 489.8, 533.2, 591.5, 626.9, 660.2, 680.5, 723.2, 846.6, 970.7, 1067.4, 1126.8, 1175.0],
        "GDP대비국가채무": [29.0, 29.5, 31.2, 32.5, 34.0, 34.2, 34.1, 33.9, 35.4, 41.1, 43.7, 45.9, 46.9, 46.0]
    }
    return pd.DataFrame(data)

df = get_data()

# =========================
# 사이드바 구성
# =========================
st.sidebar.title("📊 재정통계 메뉴")
menu = st.sidebar.radio(
    "항목을 선택하세요",
    ["메인 대시보드", "국가 재정 기본 개념", "총수입 상세", "총지출 상세"]
)

st.sidebar.markdown("---")
st.sidebar.caption("출처: 기획재정부 열린재정 (2024년은 예산/전망치 포함)")

# =========================
# 메인 대시보드 화면
# =========================
if menu == "메인 대시보드":
    st.title("🇰🇷 대한민국 국가 재정통계 요약")
    
    # 최신 데이터 Metric 표시
    latest = df.iloc[-1]
    prev = df.iloc[-2]
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("총수입 (2024)", f"{latest['총수입']}조", f"{round(latest['총수입'] - prev['총수입'], 1)}조")
    col2.metric("총지출 (2024)", f"{latest['총지출']}조", f"{round(latest['총지출'] - prev['총지출'], 1)}조")
    col3.metric("관리재정수지", f"{latest['관리재정수지']}조", f"{round(latest['관리재정수지'] - prev['관리재정수지'], 1)}조", delta_color="inverse")
    col4.metric("국가채무 비율", f"{latest['GDP대비국가채무']}%", f"{round(latest['GDP대비국가채무'] - prev['GDP대비국가채무'], 1)}%", delta_color="inverse")

    st.markdown("---")

    # 1. 재정수지 차트
    st.subheader("📍 재정수지 추이 (총수입 vs 총지출)")
    
    lhs_df = df.melt(id_vars="연도", value_vars=["총수입", "총지출"], var_name="지표", value_name="값")
    rhs_df = df.melt(id_vars="연도", value_vars=["통합재정수지", "관리재정수지"], var_name="지표", value_name="값")

    base = alt.Chart(df).encode(x=alt.X("연도:O", title="연도"))

    line_chart = alt.Chart(lhs_df).mark_line(point=True, strokeWidth=3).encode(
        x="연도:O",
        y=alt.Y("값:Q", title="수입/지출 (조 원)"),
        color=alt.Color("지표:N", scale=alt.Scale(domain=["총수입", "총지출"], range=["#1f77b4", "#ff7f0e"])),
        tooltip=["연도", "지표", "값"]
    )

    bar_chart = alt.Chart(rhs_df).mark_bar(opacity=0.4).encode(
        x="연도:O",
        y=alt.Y("값:Q", title="재정수지 (조 원)"),
        color=alt.Color("지표:N", title="수지 구분"),
        tooltip=["연도", "지표", "값"]
    )

    finance_combined = alt.layer(bar_chart, line_chart).resolve_scale(y="independent").properties(height=500)
    st.altair_chart(finance_combined, use_container_width=True)

    # 2. 국가채무 차트
    st.subheader("📍 국가채무 및 GDP 대비 비율")
    
    debt_bar = alt.Chart(df).mark_bar(color="#8884d8", opacity=0.6).encode(
        x="연도:O",
        y=alt.Y("국가채무:Q", title="국가채무 (조 원)"),
        tooltip=["연도", "국가채무"]
    )

    debt_line = alt.Chart(df).mark_line(point=True, color="#ef4444", strokeWidth=3).encode(
        x="연도:O",
        y=alt.Y("GDP대비국가채무:Q", title="GDP 대비 비율 (%)"),
        tooltip=["연도", "GDP대비국가채무"]
    )

    debt_combined = alt.layer(debt_bar, debt_line).resolve_scale(y="independent").properties(height=400)
    st.altair_chart(debt_combined, use_container_width=True)

# =========================
# 국가 재정 기본 개념
# =========================
elif menu == "국가 재정 기본 개념":
    st.title("📖 국가 재정 기본 개념 정리")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("### 1. 통합재정수지")
        st.write("""
        당해 연도의 **모든 수입에서 모든 지출을 뺀 수치**입니다. 
        국가 재정의 전체적인 외형을 파악하는 데 사용됩니다.
        - **수식:** 총수입 - 총지출
        """)
        
    with col2:
        st.success("### 2. 관리재정수지")
        st.write("""
        통합재정수지에서 **사회보장성기금수지**(국민연금, 사학연금 등)를 제외한 수치입니다.
        정부의 **실질적인 재정 상태**를 보여주는 핵심 지표입니다.
        - 대한민국은 현재 국민연금이 흑자이므로, 보통 통합수지보다 관리수지가 더 낮게 나타납니다.
        """)

    st.warning("### 3. 국가채무 (D1)")
    st.write("""
    중앙정부와 지방정부가 직접적인 지급 의무를 가지는 채무입니다. 
    국제 기준에 따라 국공채, 차입금 등이 포함되며, 공기업 부채나 연금충당부채는 포함되지 않습니다.
    """)

# =========================
# 총수입 / 총지출 섹션
# =========================
elif menu == "총수입":
    st.title("💰 총수입 구성 분석")
    st.write("총수입은 **국세수입 + 세외수입 + 기금수입**으로 구성됩니다.")
    st.info("상세 데이터 업데이트 예정 (국세수입 비중 등)")

elif menu == "총지출":
    st.title("💸 총지출 구성 분석")
    st.write("총지출은 **예산 + 기금**으로 구성되며, 보건·복지·고용 분야의 비중이 가장 큽니다.")
    st.info("상세 데이터 업데이트 예정 (분야별 지출 추이 등)")

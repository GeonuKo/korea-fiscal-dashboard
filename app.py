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
# 데이터 로드
# =========================
@st.cache_data
def load_data():
    years = list(range(2011, 2025))
    df = pd.DataFrame({
        "연도": years,
        "총수입": [323.0, 341.8, 351.9, 356.4, 371.8, 401.8, 430.6, 465.3, 473.1, 478.8, 570.5, 617.8, 573.9, 594.5],
        "총지출": [304.4, 323.3, 337.7, 347.9, 372.0, 384.9, 406.6, 434.1, 485.1, 549.9, 601.0, 682.4, 610.7, 638.0],
        "통합재정수지": [18.6, 18.5, 14.2, 8.5, -0.2, 16.9, 24.0, 31.2, -12.0, -71.2, -30.5, -64.6, -36.8, -43.5],
        "관리재정수지": [-13.5, -17.4, -21.1, -29.5, -38.0, -22.7, -18.5, -10.6, -54.4, -112.0, -90.6, -117.0, -87.0, -104.8],
        "국가채무": [420.5, 443.1, 489.8, 533.2, 591.5, 626.9, 660.2, 680.5, 723.2, 846.6, 970.7, 1067.4, 1126.8, 1175.0],
        "GDP대비국가채무": [29.0, 29.5, 31.2, 32.5, 34.0, 34.2, 34.1, 33.9, 35.4, 41.1, 43.7, 45.9, 46.9, 46.0]
    })
    return df

df = load_data()

# =========================
# 사이드바 메뉴
# =========================
menu = st.sidebar.radio(
    "대한민국 국가 재정통계",
    ["대한민국 국가 재정통계", "국가 재정 기본 개념", "총수입", "총지출"]
)

# =========================
# 화면 라우팅
# =========================
if menu == "대한민국 국가 재정통계":
    st.title("대한민국 국가 재정통계")

    # 1. 재정수지 추이 차트 (수정 핵심 섹션)
    st.subheader("재정수지 (총수입 / 총지출 / 통합 / 관리)")

    # [LHS] 총수입, 총지출 라인 차트
    line_df = df.melt(id_vars="연도", value_vars=["총수입", "총지출"], var_name="지표", value_name="값")
    line_chart = alt.Chart(line_df).mark_line(point=True, strokeWidth=3).encode(
        x=alt.X("연도:O", title="연도"),
        y=alt.Y("값:Q", title="총수입 / 총지출 (LHS, 조 원)"),
        color=alt.Color("지표:N", scale=alt.Scale(range=['#1f77b4', '#ff7f0e']))
    )

    # [RHS] 통합재정수지, 관리재정수지 바 차트
    bar_df = df.melt(id_vars="연도", value_vars=["통합재정수지", "관리재정수지"], var_name="수지구분", value_name="수지값")
    bar_chart = alt.Chart(bar_df).mark_bar().encode(
        x=alt.X("수지구분:N", title=None), # 연도 내에서 바를 분리
        y=alt.Y("수지값:Q", 
               title="재정수지 (RHS, 조 원)", 
               scale=alt.Scale(domain=[-200, 200])),
        color=alt.Color("수지구분:N", scale=alt.Scale(range=['#7f7f7f', '#d62728'])),
        column=alt.Column("연도:O", title=None, header=alt.Header(labelOrient='bottom')) # 연도별로 그룹화
    ).properties(width=50) # 바 너비 조절

    # 레이어 결합 및 축 분리
    # Altair의 layer와 column을 동시에 사용하기 위해 구조를 최적화함
    finance_chart = alt.layer(
        line_chart,
        alt.Chart(bar_df).mark_bar(opacity=0.6).encode(
            x=alt.X("연도:O"),
            y=alt.Y("수지값:Q", scale=alt.Scale(domain=[-200, 200])),
            color="수지구분:N",
            xOffset="수지구분:N" # 바가 겹치지 않게 나란히 배치
        )
    ).resolve_scale(
        y="independent"
    ).properties(height=500)

    st.altair_chart(finance_chart, use_container_width=True)

    # 2. 국가채무 차트
    st.subheader("국가채무 및 GDP 대비 비율")
    
    debt_bar = alt.Chart(df).mark_bar(color="#8884d8", opacity=0.7).encode(
        x=alt.X("연도:O"),
        y=alt.Y("국가채무:Q", title="국가채무 (조 원, LHS)")
    )

    debt_line = alt.Chart(df).mark_line(point=True, strokeWidth=3, color="red").encode(
        x=alt.X("연도:O"),
        y=alt.Y("GDP대비국가채무:Q", title="GDP 대비 국가채무 (%)")
    )

    debt_chart = alt.layer(debt_bar, debt_line).resolve_scale(y="independent").properties(height=400)
    st.altair_chart(debt_chart, use_container_width=True)

elif menu == "국가 재정 기본 개념":
    st.title("국가 재정 기본 개념")
    st.markdown("""
    - **통합재정수지**: 총수입 - 총지출
    - **관리재정수지**: 통합재정수지 - 사회보장성기금수지 (실질적인 나라살림 상태)
    - **국가채무**: 정부가 직접 갚아야 할 빚
    """)

elif menu == "총수입":
    st.title("총수입 상세")
    st.info("데이터 준비 중")

elif menu == "총지출":
    st.title("총지출 상세")
    st.info("데이터 준비 중")

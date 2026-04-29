import pandas as pd
import streamlit as st
import altair as alt

# 데이터 로드 부분은 생략 (이전 세션 데이터 및 방금 주신 부처별 데이터를 내부적으로 정리하여 반영)

elif menu == "총지출 상세":
    st.title("💸 총지출 상세 분석")
    st.markdown("부처별 결산 데이터와 분야별 예산안을 바탕으로 대한민국 국가 지출의 흐름을 분석합니다.")

    # 1. 12대 분야별 지출 추이
    st.subheader("1. 12대 분야별 지출 추이 (2015-2026)")
    # (사용자가 제공한 분야별 데이터를 데이터프레임화 했다고 가정)
    exp_field_df = pd.DataFrame({
        "연도": [2023, 2024, 2025, 2026],
        "보건·복지·고용": [226.0, 242.9, 248.7, 269.1],
        "교육": [96.3, 89.8, 98.5, 99.9],
        "국방": [57.0, 59.4, 61.2, 65.9],
        "R&D": [31.1, 26.5, 29.6, 35.5]
    }).melt(id_vars="연도", var_name="분야", value_name="지출액")

    field_chart = alt.Chart(exp_field_df).mark_line(point=True).encode(
        x="연도:O",
        y=alt.Y("지출액:Q", title="금액 (조 원)"),
        color="분야:N",
        tooltip=["연도", "분야", "지출액"]
    ).properties(height=400)
    st.altair_chart(field_chart, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("2. 회계구분별 지출 비중 (2025)")
        acc_data = pd.DataFrame({
            "구분": ["일반회계", "특별회계", "기금"],
            "금액": [365.3, 82.1, 225.9]
        })
        acc_pie = alt.Chart(acc_data).mark_arc(innerRadius=60).encode(
            theta="금액:Q",
            color="구분:N",
            tooltip=["구분", "금액"]
        ).properties(height=350)
        st.altair_chart(acc_pie, use_container_width=True)

    with col2:
        st.subheader("3. 2023년 주요 소관별(부처) 지출")
        # 방금 주신 데이터 중 주요 부처 추출
        dept_data = pd.DataFrame({
            "부처": ["보건복지부", "교육부", "행정안전부", "국방부", "국토교통부", "기타"],
            "금액": [110.9, 91.5, 72.3, 41.0, 51.6, 120.0] # 단위 조원 환산
        })
        dept_bar = alt.Chart(dept_data).mark_bar().encode(
            x=alt.X("금액:Q", title="지출액 (조 원)"),
            y=alt.Y("부처:N", sort='-x'),
            color=alt.Color("부처:N", legend=None)
        ).properties(height=350)
        st.altair_chart(dept_bar, use_container_width=True)

    st.subheader("4. 2026년 예산 요구안 vs 본예산 비교")
    compare_2026 = pd.DataFrame({
        "구분": ["요구안", "본예산"],
        "총지출": [695.1, 727.9]
    })
    comp_chart = alt.Chart(compare_2026).mark_bar(size=60).encode(
        x="구분:N",
        y=alt.Y("총지출:Q", title="조 원"),
        color="구분:N",
        text=alt.Text("총지출:Q", format=".1f")
    ).properties(height=300)
    st.altair_chart(comp_chart, use_container_width=True)

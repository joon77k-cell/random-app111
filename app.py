import streamlit as st
import random

# 웹앱 제목
st.title("📚 시험 대비 공부 시간 추천 프로그램")
st.write("시험까지 남은 기간과 과목별 자신감을 입력하면 공부 시간을 추천해 줍니다!")

# 시험까지 남은 일수 입력
days = st.number_input(
    "시험까지 남은 일수",
    min_value=1,
    max_value=365,
    value=7
)

# 하루 공부 가능 시간 입력
hours = st.number_input(
    "하루 공부 가능 시간",
    min_value=1,
    max_value=24,
    value=5
)

# 교과목 입력
st.subheader("📖 교과목 입력")

subjects_text = st.text_input(
    "공부할 과목을 쉼표(,)로 구분해서 입력하세요.",
    value="국어, 영어, 수학, 과학, 사회"
)

subjects = [
    subject.strip()
    for subject in subjects_text.split(",")
    if subject.strip()
]

# 과목별 자신감 입력
st.subheader("💪 과목별 자신감")

confidence = {}

for subject in subjects:
    confidence[subject] = st.slider(
        f"{subject} 자신감",
        min_value=1,
        max_value=5,
        value=3,
        help="1점은 자신감이 낮음, 5점은 자신감이 높음을 의미합니다."
    )

# 공부 시간 계산 버튼
if st.button("📊 공부 시간 추천받기"):

    if len(subjects) == 0:
        st.warning("교과목을 입력해주세요.")

    else:
        # 전체 공부 가능 시간
        total_hours = days * hours

        # 자신감이 낮을수록 높은 가중치 부여
        weights = {}

        for subject in subjects:
            weights[subject] = 6 - confidence[subject]

        # random 라이브러리를 이용한 무작위 가중치
        random_weights = {}

        for subject in subjects:
            random_weights[subject] = (
                weights[subject] * random.uniform(0.9, 1.1)
            )

        # 가중치 합계
        weight_sum = sum(random_weights.values())

        # 과목별 공부 시간 배분
        study_hours = {}

        for subject in subjects:
            study_hours[subject] = round(
                total_hours *
                random_weights[subject] / weight_sum,
                1
            )

        # 결과 출력
        st.subheader("🎯 과목별 추천 공부 시간")

        for subject, time in study_hours.items():
            st.write(f"{subject}: {time}시간")

        # 막대그래프 출력
        st.subheader("📊 과목별 공부 시간 그래프")

        st.bar_chart(study_hours)

        # 총 공부 시간 출력
        st.success(
            f"총 공부 가능 시간: {total_hours}시간"
        )

        st.info(
            "자신감이 낮은 과목일수록 더 많은 공부 시간이 배정됩니다."
        )

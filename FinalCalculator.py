import math
import streamlit as st



def get_letter_grade(grade: float) -> str:
    """Return a letter grade (with +/-) for a percentage score."""
    if grade >= 93:  return "A"
    elif grade >= 90: return "A−"
    elif grade >= 87: return "B+"
    elif grade >= 83: return "B"
    elif grade >= 80: return "B−"
    elif grade >= 77: return "C+"
    elif grade >= 73: return "C"
    elif grade >= 70: return "C−"
    elif grade >= 67: return "D+"
    elif grade >= 63: return "D"
    elif grade >= 60: return "D−"
    else:             return "F"


def calc_fixed_weight(current: float, desired: float, final_weight: float) -> float:
    
    """Final has a fixed percentage weight in the overall grade.

    current × (1 − w) + final × w = desired
    => final = (desired − current × (1 − w)) / w
    """
    return (desired - current * (1 - final_weight)) / final_weight


def calc_tests_category(
    current: float,
    desired: float,
    tests_weight: float,
    test_scores: list[float],
) -> tuple[float, float, float]:
    """
    Final goes into the tests category.

    current  = other_contribution + avg_tests × w_tests
    desired  = other_contribution + new_avg_tests × w_tests
    new_avg  = (sum_tests + final) / (n + 1)

    => final = (desired − other) / w_tests × (n + 1) − sum_tests

    Returns (needed_score, current_test_avg, projected_test_avg_if_achieved).
    """
    n = len(test_scores)
    sum_t = sum(test_scores)
    avg_t = sum_t / n

    other  = current - avg_t * tests_weight                    # non-test grade contribution
    needed = (desired - other) / tests_weight * (n + 1) - sum_t

    proj_avg = (sum_t + needed) / (n + 1)
    return needed, avg_t, proj_avg


def show_result(
    needed: float,
    desired_grade: float,
    num_questions: int = 0,
    extra_info: str | None = None,
) -> None:
    """Render the result block given a computed needed score."""
    if needed > 100:
        score_text = f"You need a {needed:.1f}% on the final."
    elif needed <= 0:
        score_text = "You need a 0% on the final."
    else:
        score_text = f"You need a {needed:.1f}% ({get_letter_grade(needed)}) on the final."

    if num_questions > 0 and needed <= 100:
        questions_needed = min(math.ceil(needed / 100 * num_questions), num_questions)
        can_miss = num_questions - questions_needed
        score_text += f" That is {questions_needed} out of {num_questions} questions ({can_miss} to miss)."

    if extra_info:
        score_text += f" {extra_info}"

    st.info(score_text)



st.set_page_config(
    page_title="Final Grade Calculator",
    layout="centered",
)

st.title(" Final Grade Calculator")
st.write("Find out exactly what you need to score on your final to get the grade you want.")

st.divider()

col_a, col_b = st.columns(2)

with col_a:
    current_grade = st.number_input(
        "Current Grade (%)",
        min_value=0.0,
        max_value=100.0,
        value=100.0,
        step=1.0,
    )

with col_b:
    desired_grade = st.number_input(
        "Desired Grade (%)",
        min_value=0.0,
        max_value=100.0,
        value=90.0,
        step=1.0,
    )

col_c, col_d = st.columns(2)

with col_c:
    num_questions = st.number_input(
        "Number of Questions on the Final",
        min_value=0,
        max_value=1000,
        value=100,
        step=10,
    )
    if num_questions > 0:
        st.caption(f"Each question is worth **{100 / num_questions:.2f}%**.")

st.divider()
st.subheader("How does your final count?")

final_type = st.radio(
    "Select one:",
    options=[
        "The final has a fixed percentage weight",
        "The final is averaged into my tests category",
    ],
    label_visibility="collapsed",
)

st.write("")



if final_type == "The final has a fixed percentage weight":

    final_weight_pct = st.slider(
        "Final exam weight (%)",
        min_value=1,
        max_value=100,
        value=30,
        format="Percents",
        
    )
    st.caption(
        f"Your completed (non-final) work accounts for the remaining "
        f"**{100 - final_weight_pct}%** of your grade."
    )

    if st.button("Calculate", type="primary", use_container_width=True):
        needed = calc_fixed_weight(current_grade, desired_grade, final_weight_pct / 100)

        st.divider()
        st.subheader(" Results")

        m1, m2, m3 = st.columns(3)
        m1.metric("Current Grade",  f"{current_grade:.1f}%",  get_letter_grade(current_grade))
        m2.metric("Target Grade",   f"{desired_grade:.1f}%",  get_letter_grade(desired_grade))

        if needed > 100:
            m3.metric("Score Needed is above 100%")
        elif needed <= 0:
            m3.metric("Score Needed", "0% ")
        else:
            m3.metric("Score Needed", f"{needed:.1f}%", get_letter_grade(needed))

        show_result(needed, desired_grade, num_questions=int(num_questions))

else:

    tests_weight_pct = st.slider(
        "Tests category weight (%)",
        min_value=1,
        max_value=100,
        value=40,
        format="percent",
    )
    
    

    st.write("")
    st.write("**Previous test scores**")

    num_tests = st.number_input(
        "Number of Tests so far",
        min_value=1,
        max_value=20,
        value=3,
        step=1,
    )


    test_scores: list[float] = []
    num_cols = min(int(num_tests), 5)
    cols = st.columns(num_cols)

    for i in range(int(num_tests)):
        score = cols[i % num_cols].number_input(
            f"Test {i + 1} (%)",
            min_value=0.0,
            max_value=100.0,
            value=100.0,
            step=1.0,
            key=f"test_{i}",
        )
        test_scores.append(score)

    # Live average preview
    if test_scores:
        cur_avg = sum(test_scores) / len(test_scores)
        st.caption(
            f"Current test average: **{cur_avg:.1f}% ({get_letter_grade(cur_avg)})**"
        )

    if st.button("Calculate", type="primary", use_container_width=True):
        needed, cur_avg, proj_avg = calc_tests_category(
            current_grade,
            desired_grade,
            tests_weight_pct / 100,
            test_scores,
        )

        st.divider()
        st.subheader(" Results")

        m1, m2, m3 = st.columns(3)
        m1.metric("Current Grade", f"{current_grade:.1f}%",  get_letter_grade(current_grade))
        m2.metric("Target Grade",  f"{desired_grade:.1f}%",  get_letter_grade(desired_grade))

        if needed > 100:
            m3.metric("Score Needed is above 100")
        elif needed <= 0:
            m3.metric("Score Needed is a 0% so you're already at your goal.")
        else:
            m3.metric("Score Needed", f"{needed:.1f}%", get_letter_grade(needed))

        avg_info = (
            f" This would move your tests average: "
            f"**{cur_avg:.1f}%** → **{proj_avg:.1f}% ({get_letter_grade(proj_avg)})**"
        ) if 0 < needed <= 100 else None

        show_result(needed, desired_grade, num_questions=int(num_questions), extra_info=avg_info)


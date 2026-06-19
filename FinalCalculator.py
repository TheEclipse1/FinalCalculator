import math
import streamlit as st


def letterGrade(grade: float) -> str:
    if grade >= 93:
        return "A"
    elif grade >= 90:
        return "A−"
    elif grade >= 87:
        return "B+"
    elif grade >= 83:
        return "B"
    elif grade >= 80:
        return "B−"
    elif grade >= 77:
        return "C+"
    elif grade >= 73:
        return "C"
    elif grade >= 70:
        return "C−"
    elif grade >= 67:
        return "D+"
    elif grade >= 63:
        return "D"
    elif grade >= 60:
        return "D−"
    else:
        return "F"


def fixedCalc(current: float, desired: float, fWeight: float) -> float:
    return (desired - current * (1 - fWeight)) / fWeight


def testsCalc(
    current: float,
    desired: float,
    tWeight: float,
    scores: list[float],
) -> tuple[float, float, float]:
    n = len(scores)
    total = sum(scores)
    avg = total / n

    other = current - avg * tWeight
    needed = (desired - other) / tWeight * (n + 1) - total

    projAvg = (total + needed) / (n + 1)
    return needed, avg, projAvg


def showResult(
    needed: float,
    target: float,
    numQ: int = 0,
    info: str | None = None,
) -> None:
    if needed > 100:
        text = f"You need a {needed:.1f}% on the final."
    elif needed <= 0:
        text = "You need a 0% on the final."
    else:
        text = f"You need a {needed:.1f}% ({letterGrade(needed)}) on the final."

    if numQ > 0 and needed <= 100:
        qNeeded = min(math.ceil(needed / 100 * numQ), numQ)
        miss = numQ - qNeeded
        text += f" That is {qNeeded} out of {numQ} questions ({miss} to miss)."

    if info:
        text += f" {info}"

    st.info(text)


st.set_page_config(
    page_title="Final Grade Calculator",
    layout="centered",
)

st.title(" Final Grade Calculator")
st.write("Find out exactly what you need to score on your final to get the grade you want.")

st.divider()

colA, colB = st.columns(2)

with colA:
    currentGrade = st.number_input(
        "Current Grade (%)",
        min_value=0.0,
        max_value=100.0,
        value=100.0,
        step=1.0,
    )

with colB:
    desiredGrade = st.number_input(
        "Desired Grade (%)",
        min_value=0.0,
        max_value=100.0,
        value=90.0,
        step=1.0,
    )

colC, colD = st.columns(2)

with colC:
    numQ = st.number_input(
        "Number of Questions on the Final",
        min_value=0,
        max_value=1000,
        value=100,
        step=10,
    )
    if numQ > 0:
        st.caption(f"Each question is worth **{100 / numQ:.2f}%**.")

st.divider()
st.subheader("How does your final count?")

finalType = st.radio(
    "Select one:",
    options=[
        "The final has a fixed percentage weight",
        "The final is averaged into my tests category",
    ],
    label_visibility="collapsed",
)

st.write("")

if finalType == "The final has a fixed percentage weight":
    finalPct = st.slider(
        "Final exam weight (%)",
        min_value=1,
        max_value=100,
        value=30,
        format="Percents",
    )
    st.caption(
        f"Your completed (non-final) work accounts for the remaining "
        f"**{100 - finalPct}%** of your grade."
    )

    if st.button("Calculate", type="primary", use_container_width=True):
        needed = fixedCalc(currentGrade, desiredGrade, finalPct / 100)

        st.divider()
        st.subheader(" Results")

        m1, m2, m3 = st.columns(3)
        m1.metric("Current Grade", f"{currentGrade:.1f}%", letterGrade(currentGrade))
        m2.metric("Target Grade", f"{desiredGrade:.1f}%", letterGrade(desiredGrade))

        if needed > 100:
            m3.metric("Score Needed is above 100%")
        elif needed <= 0:
            m3.metric("Score Needed", "0%")
        else:
            m3.metric("Score Needed", f"{needed:.1f}%", letterGrade(needed))

        showResult(needed, desiredGrade, numQ=int(numQ))

else:
    testsPct = st.slider(
        "Tests category weight (%)",
        min_value=1,
        max_value=100,
        value=40,
        format="percent",
    )

    st.write("")
    st.write("**Previous test scores**")

    numTests = st.number_input(
        "Number of Tests so far",
        min_value=1,
        max_value=20,
        value=3,
        step=1,
    )

    scores: list[float] = []
    numCols = min(int(numTests), 5)
    cols = st.columns(numCols)

    for i in range(int(numTests)):
        score = cols[i % numCols].number_input(
            f"Test {i + 1} (%)",
            min_value=0.0,
            max_value=100.0,
            value=100.0,
            step=1.0,
            key=f"test{i}",
        )
        scores.append(score)

    if scores:
        curAvg = sum(scores) / len(scores)
        st.caption(
            f"Current test average: **{curAvg:.1f}% ({letterGrade(curAvg)})**"
        )

    if st.button("Calculate", type="primary", use_container_width=True):
        needed, curAvg, projAvg = testsCalc(
            currentGrade,
            desiredGrade,
            testsPct / 100,
            scores,
        )

        st.divider()
        st.subheader(" Results")

        m1, m2, m3 = st.columns(3)
        m1.metric("Current Grade", f"{currentGrade:.1f}%", letterGrade(currentGrade))
        m2.metric("Target Grade", f"{desiredGrade:.1f}%", letterGrade(desiredGrade))

        if needed > 100:
            m3.metric("Score Needed is above 100")
        elif needed <= 0:
            m3.metric("Score Needed is a 0% so you're already at your goal.")
        else:
            m3.metric("Score Needed", f"{needed:.1f}%", letterGrade(needed))

        avgInfo = (
            f" This would move your tests average: "
            f"**{curAvg:.1f}%** → **{projAvg:.1f}% ({letterGrade(projAvg)})**"
        ) if 0 < needed <= 100 else None

        showResult(needed, desiredGrade, numQ=int(numQ), info=avgInfo)

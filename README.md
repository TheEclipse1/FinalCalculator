# Final Grade Calculator

Tells you what you need on your final to end up with the grade you want.

## Setup

bashpip install streamlit
streamlit run final_grade_calculator.py

## How to use it

Enter your current grade, your target grade, and optionally how many questions are on the final. Then pick how your final is weighted:


Fixed weight — the final is worth a set percentage of your total grade (e.g. 30%). Use the slider to set it.
Tests category — the final gets averaged in with your other test scores. You'll enter the category weight and your scores so far.


### Hit calculate, and it tells you the score you need. If you entered a question count, it also tells you how many you can miss.

## Math

Fixed weight

final_needed = (desired - current × (1 - w)) / w

### Tests category

other        = current - avg_tests × w_tests
final_needed = (desired - other) / w_tests × (n + 1) - sum_tests

Question count uses ceil so the result never rounds down into a failing score.



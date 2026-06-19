# Final Grade Calculator
# A Streamlit made website to tell you exactly what you need on your final to get the grade you want
## Overview
Final Grade Calculator uses your current grade and your target grade to figure out the exact score you need on your final. It supports two weighting modes and can optionally break your target down by question count so you know how many you can afford to miss.
## How to Use this App
Run the app and enter your current grade and the grade you want.
Optionally enter the number of questions on your final to tell you how many questions you need to get right to pass.
Then pick how your final is weighted; the app offers either
* **Fixed weight** : the final is worth a set percentage of your total grade (e.g. 30%). Use the slider to set it.
* **Tests category** : the final gets averaged in with your other test scores. Enter the category weight and your scores so far.

Hit Calculate and it tells you the score you need.
## Tweaking
# If you want to make something like this for a different grading structure
1. Download the zip file
2. Extract the contents
3. Open your IDE
4. Run
```bash
pip install -r requirements.txt
```
5. Adjust the letter grade scale in `letterGrade` if necessary
6. To add a new weighting mode, add an option to the `finalType` radio and a matching calculation function
7. To build run
```bash
streamlit run final_grade_calculator.py
```
and you should have your own grade calculator! :)

# HELPER FILE, DON'T USE


import data
import csv
from constants import DATA_PATH

with open(DATA_PATH + 'trivia_questions.csv', 'w', encoding='utf-8-sig') as csv_file:
    fieldnames = ['category','sc_reward','source','question_text','image','answers','answer_message']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()

    questions = data.get_trivia_questions_data()
    for question in questions:
        question["answers"] = ";;".join(question["answers"])
        writer.writerow(question)
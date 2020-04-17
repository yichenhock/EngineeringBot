import csv

from constants import DATA_PATH

class TriviaQuestion:
    def __init__(self, data):
        for key, val in data.items():
            setattr(self, key, val)
        self.answers = self.answers.replace("\n", ";;").split(";;")
        self.sc_reward = int(self.sc_reward)


trivia_questions = None

def get_trivia_questions_data():
    data = []
    with open(DATA_PATH+'trivia_questions.csv', mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if row["question_text"] is not "":
                data.append(row)
                line_count += 1
    return data

def get_trivia_questions(cached=False):
    global trivia_questions
    if trivia_questions is None or not cached:
        trivia_questions = []
        for question_data in get_trivia_questions_data():
            trivia_questions.append(TriviaQuestion(question_data))
    return trivia_questions
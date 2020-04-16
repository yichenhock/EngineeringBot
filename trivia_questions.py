import data

class TriviaQuestion:
    def __init__(self, data):
        for key, val in data.items():
            setattr(self, key, val)


trivia_questions = None

def get_trivia_questions(cached=False):
    global trivia_questions
    if trivia_questions is None or not cached:
        trivia_questions = []
        for question_data in data.get_trivia_questions_data():
            trivia_questions.append(TriviaQuestion(question_data))
    return trivia_questions
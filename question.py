import random

class Question:
    answer_symbols = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p"]
    def __init__(self, question_text, category=None, *answers:list, question_img=None):
        """
        question_text: a string
        answers: a list of strings
        question_img: a string
        """
        self.question_text = question_text
        self.question_img = question_img
        random.shuffle(answers)
        self.answers = answers
        self.category = category
    
    def show_question(self):
        """Call this function to display the question"""
        # Show question text
        if self.question_img is not None:
            pass # Show image
        
        for i, answer in self.answers:
            answer_text = "{}. {}".format(Question.answer_symbols[i], answer)
            # Show answer text
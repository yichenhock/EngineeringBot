import json
import os

Q_PATH = "questions/"

def get_question_data_dict():
    data = {}
    data["question_title"] = "Title of question"
    data["question_text"] = "Add question text here"
    data["answers"] = ['list', 'of', 'strings', 'that', 'will', 'be', 'mixed']
    data["difficulty_score"] = 10
    data["category"] = "category name"
    data["image_name"] = ""
    return data

def add_question_to_file(name):
    fp = Q_PATH+name
    questions = load_file(fp)
    questions.append(get_question_data_dict())
    save_file(questions, fp)
    print("Question added. There are now {} questions of this type.".format(len(questions)))

def load_file(filename):
    if os.path.exists(filename):
        with open(filename, "r") as json_file: 
            data = json.load(json_file)
    else:
        data = []
    return data

def save_file(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, sort_keys=True, indent=4)

def main():
    while True:
        option = input("Do you want (a) trivia, or (b) main (tripos) question?   (a/b): ")
        if option == "a":
            add_question_to_file("trivia_questions.json")
        if option == "b":
            add_question_to_file("main_questions.json")

if __name__ == "__main__":
    main()
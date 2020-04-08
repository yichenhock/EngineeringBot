import json
import os

DATA_PATH = "data/"

def get_lecturer_data_dict():
    data = {
        "name": "Lecturer name here",
        "subject": "Subject here",
        "category": "Category here",
        "trivia_messages": ["I'll say one of these things randomly before giving you a trivia question.", "Can you do this trivia question?"],
        "level": "2"
    }
    return data

def get_question_data_dict():
    data = {
        "question_title" : "Title of question",
        "question_text" : "Add question text here",
        "answers" : ['list', 'of', 'strings', 'that', 'will', 'be', 'mixed'],
        "difficulty_score" : 10,
        "category" : "category name",
        "image_name" : ""
    }
    return data

def add_dict_to_list_in_file(dict, name):
    fp = DATA_PATH+name
    data_list = load_file(fp, [])
    data_list.append(dict)
    save_file(data_list, fp)

def get_len_of_list_in_file(name):
    fp = DATA_PATH+name
    data_list = load_file(fp, [])
    return len(data_list)

def load_file(filename,default):
    if os.path.exists(filename):
        with open(filename, "r") as json_file: 
            data = json.load(json_file)
    else:
        data = default
    return data

def save_file(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, sort_keys=True, indent=4)

def main():
    while True:
        option = input("(a) add trivia\n(b) add main (tripos) question\n(c) Add lecturer   \n(Pick a letter): ")
        if option == "a":
            add_dict_to_list_in_file(get_question_data_dict(), "trivia_questions.json")
            print("Question added. There are now {} trivia questions.".format(get_len_of_list_in_file("trivia_questions.json")))
        if option == "b":
            add_dict_to_list_in_file(get_question_data_dict(), "main_questions.json")
            print("Question added. There are now {} main questions.".format(get_len_of_list_in_file("main_questions.json")))
        if option == "c":
            add_dict_to_list_in_file(get_lecturer_data_dict(), "lecturers.json")
            print("Lecturer added. There are now {} lecturers.".format(get_len_of_list_in_file("lecturers.json")))

if __name__ == "__main__":
    main()
"""This is purely a utility file for adding entries to the .json files in the data folder. Don't call any functions from here."""


import json
import os

DATA_PATH = "data/"

class DataAdder:
    def __init__(self, desc, filename, data_generator):
        self.desc = desc
        self.filename = filename
        self.data_generator = data_generator
    def add_data(self):
        fp = DATA_PATH+self.filename+".json"
        data_list = load_file(fp, [])
        data_list.append(self.data_generator())
        save_file(data_list, fp)

def get_lab_dict():
    num = int(input("How many outcomes do you want the lab to have?"))
    outcomes = []
    for _ in range(num):
        outcomes.append(
            {
                "description": "Description",
                "min_sc": 0,
                "max_sc": 10
            }
        )
    return {
        "name": "Name",
        "description": "Description",
        "outcomes": outcomes
    }

def get_lecturer_dict():
    data = {
        "name": "Lecturer name here",
        "subject": "Subject here",
        "category": "Category here",
        "trivia_messages": ["I'll say one of these things randomly before giving you a trivia question.", "Can you do this trivia question?"],
        "level": 2
    }
    return data

def get_question_dict():
    data = {
        "question_title" : "Title of question",
        "question_text" : "Add question text here",
        "answers" : ['list', 'of', 'strings', 'that', 'will', 'be', 'mixed'],
        "difficulty_score" : 10,
        "category" : "category name",
        "image_name" : ""
    }
    return data

def get_item_dict():
    shop_item = input("Is it a shop item? (y/n): ").lower()
    data = {
        "name" : "Item name",
        "emoji" : "",
        "cost" : 100,
        "description" : "Item description",
        "aliases": ["name1","name2","name3"]
    }
    if shop_item == "y":
        data["shop_item"] = True
    return data

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

        options = [
            DataAdder("Add trivia", "trivia_questions", get_question_dict),
            DataAdder("Add main (tripos) questions", "main_questions", get_question_dict), 
            DataAdder("Add lecturer", "lecturers", get_lecturer_dict), 
            DataAdder("Add item", "items", get_item_dict),
            DataAdder("Add lab", "labs", get_lab_dict)
        ]
        for i, option in enumerate(options):
            print("{}) {}".format(i, option.desc))
        option = int(input("(Pick a number): "))
        if isinstance(option, int):
            if option >= 0 and option < len(options):
                options[option].add_data()
                print("Operation completed")

        print("\n")

if __name__ == "__main__":
    main()
import json

QUESTION_PATH = "questions/"

def add_question():
    print("Adding Question:\n\n")
    file_name = input("What is the name of the question file:")
    data = {}
    data["question_text"] = "Add question text here"
    data["answers"] = ['list', 'of', 'strings', 'that', 'will', 'be', 'mixed']
    data["difficulty_score"] = 10
    data["category"] = "category name"
    save_file(data, file_name)


def save_file(data, filename):
    with open(QUESTION_PATH+filename+".txt", "w") as f:
        json.dump(data, f, sort_keys=True, indent=4)

def main():
    while True:
        add_question()


if __name__ == "__main__":
    main()
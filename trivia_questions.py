import csv
from constants import DATA_PATH
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
from os import getenv
from urllib.parse import urlparse
from urllib import parse
import os
import requests
import datetime
load_dotenv()
client_dict = {
  "type": "service_account",
  "project_id": getenv("GSHEET_PROJECT_ID"),
  "private_key_id": getenv("GSHEET_PRIVATE_KEY_ID"),
  "private_key": getenv("GSHEET_PRIVATE_KEY"),
  "client_email": getenv("GSHEET_CLIENT_EMAIL"),
  "client_id": getenv("GSHEET_CLIENT_ID"),
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": getenv("GSHEET_CLIENT_CERT_URL")
}


# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_dict(client_dict, scope)


class TriviaQuestion:
    def __init__(self, data):
        for key, val in data.items():
            setattr(self, key, val)
        self.answers = self.answers.replace("\n", ";;").split(";;")
        self.sc_reward = int(self.sc_reward)
        self.is_multiple_choice = not (self.is_multiple_choice.lower() == "n")
        if self.is_multiple_choice:
            self.correct_answer = self.answers[0]

    def is_correct(self, answer):
        if self.is_multiple_choice:
            return answer == self.correct_answer
        else:
            return answer.lower() in set(a.lower() for a in self.answers)

trivia_questions = None

def get_question_img(img_link):
    # print(img_link)
    if not img_link:
        return None

    query = urlparse(img_link).query
    id = parse.parse_qs(query).get("id")

    if not id:
        return None
    id = id[0]
    destination = "./data/trivia_img/" + id + ".png"
    if os.path.exists(destination):
        return id + ".png"

    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)


    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)
    return id + ".png"

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
def date_from_dict(s):
    if not s.get("Timestamp"):
        return datetime.datetime.now()

    return datetime.datetime.strptime(s.get("Timestamp"),'%m/%d/%Y %H:%M:%S')



def get_trivia_questions_data():
    data = []
    # with open(DATA_PATH+'trivia_questions.csv', mode='r', encoding='utf-8-sig') as csv_file:
    #     csv_reader = csv.DictReader(csv_file)
    #     line_count = 0
    #     for row in csv_reader:
    #         if row["question_text"] is not "":
    #             data.append(row)
    #             print(row)
    #             line_count += 1
    #
    # return data
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1vc7UNW075vrQCtJ2wA4FaNlWeIiDfrggQSFVOOWkiRI/edit?usp=sharing").sheet1

    # Extract and print all of the values
    list_of_hashes = sheet.get_all_records()
    list_of_hashes.sort(key=date_from_dict)
    for rough in list_of_hashes:
        if not rough.get("SC Value"):
            continue
        question = {}
        question["category"] = rough['Pick the category that your question fits best!'].replace(" (dynamics or fluids)", "").replace(" (or Electrical)", "").lower()
        question["sc_reward"] = float(rough["SC Value"])
        question["source"] = rough["Does your question have a source? If so, put it here. (optional)"]
        question["question_text"] = rough['Put your question here!']
        # print("Getting image")
        question["image"] = get_question_img(rough["Upload an image that goes with the question. (optional)"])
        # print("Got image")
        question["is_multiple_choice"] = 'y' if rough['How do players answer your question?'] == "Multiple choice" else 'n'
        question["answers"] = rough.get('What is the correct answer to your question?', '') + rough.get('Type in some correct answers to your question, with each one on a new line.', '') + '\n' +  rough.get('Add a few incorrect answers. (put each one on a new line)', '')
        question["answer_message"] = rough['Add some text that shows up after the player answers the question. (optional)']
        data.append(question)

    return data



def get_trivia_questions(cached=False):
    global trivia_questions
    if trivia_questions is None or not cached:
        trivia_questions = []
        for question_data in get_trivia_questions_data():
            trivia_questions.append(TriviaQuestion(question_data))
    return trivia_questions

import json
import os
import random

import data
from constants import MAX_LECTURER_LEVEL, SC_EMOJI

lecturers = []


class Lecturer():
    def __init__(self, data_dict): 
        for key, value in data_dict.items():
            setattr(self, key, value) # `key` is a string which is the name of the property being set.
            # so if key = 'name', value = 'jeff', the above does self.name = 'jeff'.
    
    def get_random_trivia_message(self):
        return random.choice(self.trivia_messages)

def import_lecturers():
    global lecturers
    lecturers = []
    lecturers_data = data.get_lecturers()
    for i in lecturers_data:
        lecturers.append(Lecturer(i))

def get_by_level(level):
    level = min(level, MAX_LECTURER_LEVEL)
    for lecturer in lecturers:
        if lecturer.level == level:
            return lecturer
    return None

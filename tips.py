import data
import random
from constants import DATA_PATH
_tips = []

def get_random_tip(probability = 1):
    if probability < 1:
        if random.random() > probability:
            return ""
    if not _tips:
        _import_tips()
    return random.choice(_tips)

def _import_tips():
    with open(DATA_PATH+"tips.txt", "r") as f:
        for line in f:
            _tips.append(line.strip())
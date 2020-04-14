import asyncio
import json
import os

from constants import DATA_PATH, MAX_LECTURER_LEVEL

data = {}
_data_files = {}


async def saveloop():
    while True:
        save_data()
        await asyncio.sleep(10)

def load_data(bot):
    global data
    # checks if data file exist, if not, writes an empty dict to it
    if os.path.exists(DATA_PATH+"data.json"):
        with open(DATA_PATH+"data.json", "r") as json_file: 
            data = json.load(json_file)
    else:
        data = {}
    # print(data)
    bot.loop.create_task(saveloop())


def add_data(*keys):
    """Add or insert a data entry."""

    keys, value = keys[:-1], keys[-1]

    current_dict = data
    for key in keys[:-1]:
        key = str(key)
        if not key in current_dict:
            current_dict[key] = {}
        current_dict = current_dict[key]

    key = str(keys[-1])
    if isinstance(current_dict, dict):
        current_dict[key] = value

def get_data(*keys, default_val=None):
    """Get a data entry."""
    current_dict = data
    for key in keys[:-1]:
        key = str(key)
        if not key in current_dict:
            return default_val
        current_dict = current_dict[key]
    
    key = str(keys[-1])
    if isinstance(current_dict, dict):
        return current_dict.get(key, default_val)
    else:
        return default_val

def save_data():
    with open(DATA_PATH+'data.json', 'w') as outfile:
        json.dump(data, outfile, sort_keys=True, indent=4)

def _get_from_filename(filename, default = None):
    """Starts with an underscore to signify this should only be used in this file."""
    if not filename in _data_files:
        if os.path.exists(DATA_PATH+filename+".json"):
            with open(DATA_PATH+filename+".json", "r") as json_file: 
                _data_files[filename] = json.load(json_file)
        else:
            _data_files[filename] = default
    return _data_files[filename]


def get_items():
    return _get_from_filename("items", [])

def get_labs():
    return _get_from_filename("labs", [])

def get_lecturers():
    return _get_from_filename("lecturers", [])

def get_lecturer_from_level(level):
    level = min(level, MAX_LECTURER_LEVEL)
    for lecturer in get_lecturers():
        if int(lecturer["level"]) == level:
            return lecturer

def get_main_questions():
    return _get_from_filename("main_questions", [])

def get_trivia_questions():
    return _get_from_filename("trivia_questions", [])

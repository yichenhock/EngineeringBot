import json
import asyncio
import os

DATA_PATH = "data/"

data = {}

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


def add_data(player_id, data_key, value):
    """Add or insert a data entry into a player's data."""
    player_id = str(player_id)
    data_key = str(data_key)

    if not player_id in data:
        data[player_id] = {}
    data[player_id][data_key] = value
    print(data)

def get_data(player_id, data_key=None, default_val=None):
    """Get a data entry from a specific player."""
    player_id = str(player_id)
    if data_key is not None:
        data_key = str(data_key)

    if not player_id in data:
        return default_val
    
    if data_key is None:
        return data[player_id]
    else:
        return data[player_id].get(data_key, default_val)

def save_data():
    with open(DATA_PATH+'data.json', 'w') as outfile:
        json.dump(data, outfile, sort_keys=True, indent=4)

def _get_from_filename(filename, default = None):
    """Starts with an underscore to signify this should only be used in this file."""
    if os.path.exists(DATA_PATH+filename+".json"):
        with open(DATA_PATH+filename+".json", "r") as json_file: 
            return json.load(json_file)
    else:
        return []

def get_items():
    return _get_from_filename("items", [])

def get_labs():
    return _get_from_filename("labs", [])

def get_lecturers():
    return _get_from_filename("lecturers", [])

def get_main_questions():
    return _get_from_filename("main_questions", [])

def get_trivia_questions():
    return _get_from_filename("trivia_questions", [])

def get_player_item_amount(p_id, item_name):
    return get_data(p_id, "inv", {}).get(item_name, 0)

def set_player_item_amount(p_id, item_name, amount):
    inv = get_data(p_id, "inv", {})
    inv[item_name] = amount
    add_data(p_id, "inv", inv)
import json

def add_data(player_id, data_key, value):
    """Add or insert a data entry into a player's data."""
    player_id = str(player_id)
    data_key = str(data_key)

    if not player_id in data:
        data[player_id] = {}
    data[player_id][data_key] = value
    print(data)

def get_data(player_id, data_key, default_val=None):
    """Get a data entry from a specific player."""
    player_id = str(player_id)
    data_key = str(data_key)

    if not player_id in data:
        return default_val
    return data[player_id].get(data_key, default_val)

def save_data():
    with open(PATH+'data.txt', 'w') as outfile:
        json.dump(data, outfile, sort_keys=True, indent=4)
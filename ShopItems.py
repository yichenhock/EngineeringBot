import parameters
import json
import os

items = []

DATA_PATH = "data/"

class ShopItem():
    def __init__(self, item_dict): 
        self.name = item_dict["name"]
        self.cost = item_dict["cost"]
        self.emoji = item_dict["emoji"]
        self.description = item_dict["description"]
        self.aliases = item_dict["aliases"]

def import_items():
    global items
    items = []
    if os.path.exists(DATA_PATH+"shop_items.json"):
        with open(DATA_PATH+"shop_items.json", "r") as json_file: 
            items_data = json.load(json_file)

        for i in items_data:
            items.append(ShopItem(i))

def get_by_name(name):
    global items
    for i in items:
        if name.lower() == i.name.lower() or name.lower() in i.aliases:
            return i
    return None
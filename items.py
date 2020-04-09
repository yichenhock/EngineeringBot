import parameters
import json
import os
import data

items = []

DATA_PATH = "data/"

class Item():
    def __init__(self, item_dict): 
        self.name = item_dict["name"]
        self.cost = item_dict.get("cost", None)
        self.emoji = item_dict["emoji"]
        self.description = item_dict["description"]
        self.aliases = item_dict["aliases"]
        self.shop_item = item_dict.get("shop_item", False)
    
    def can_be_in_shop(self):
        return self.shop_item
    
    def has_value(self):
        return self.cost != None

def import_items():
    global items
    items = []
    items_data = data.get_items()
    for i in items_data:
        items.append(Item(i))

def get_by_name(name):
    global items
    for i in items:
        if name.lower() == i.name.lower() or name.lower() in i.aliases:
            return i
    return None
import constants
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
        self.type = item_dict.get("type", "standard")
        self.boost = item_dict.get("boost", None)
    
    def can_be_in_shop(self):
        return self.shop_item
    
    def has_value(self):
        return not self.cost is None

    def is_booster(self):
        return not self.boost is None
    
    def get_shop_string(self):
        return '{} **{}** ─ {}{} \n{}\n\n'.format(self.emoji,self.name,constants.SC_EMOJI,self.cost,self.description)

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

def get_player_boost(player_id, category):
    """Get a player boost for a specific category.
    An output of 0 means a 0% bonus, 1 means an 100% boost.
    """
    boost = 0
    for name, amount in data.get_data(player_id, "inv", default_val={}).items():
        item = get_by_name(name)
        if item.is_booster():
            if item.boost.category == category:
                boost += min(item.boost.bonus * amount, item.boost.max_bonus)
    return boost

import json
import os

import data
from constants import SC_EMOJI

items = []


class Item():
    def __init__(self, item_dict): 
        self.name = item_dict["name"]
        self.cost = item_dict.get("cost", None)
        self.emoji = item_dict["emoji"]
        self.description = item_dict["description"]
        self.aliases = item_dict["aliases"]
        self.shop_item = item_dict.get("shop_item", False)
        self.type = item_dict.get("type", "standard")
        self.boost_bonus = item_dict.get("boost", {}).get("bonus", None)
        self.boost_max_bonus = item_dict.get("boost", {}).get("max_bonus", None)
        self.boost_category = item_dict.get("boost", {}).get("category", None)
    
    def can_be_in_shop(self):
        return self.shop_item
    
    def has_value(self):
        return not self.cost is None

    def is_booster(self):
        return not self.boost_bonus is None
    
    def get_shop_string(self):
        return '{} **{}** ─ {}{} \n{}\n\n'.format(self.emoji,self.name,SC_EMOJI,self.cost,self.description)

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


def get_player_boost(player_id, *categories):
    """Get a player boost for a specific category.
    An output of 0 means a 0% bonus, 1 means an 100% boost.
    """
    boost = 0
    for name, amount in data.get_data(player_id, "inv", default_val={}).items():
        item = get_by_name(name)
        if item.is_booster():
            if item.boost_category in categories:
                boost += get_boost_from_item_amount(item, amount)
    return boost


def get_boost_from_item_amount(item, amount):
    """Get the amount of boost a player gets from a specific item."""
    if not item.is_booster():
        return 0
    boost = min(amount * item.boost_bonus, item.boost_max_bonus)
    return boost


def get_player_boost_from_item(player_id, item):
    """Get the amount of boost a player gets from a specific item."""
    if not item.is_booster():
        return 0
    amount = data.get_data(player_id, "inv", item.name, default_val=0)
    boost = min(amount * item.boost_bonus, item.boost_max_bonus)
    return boost

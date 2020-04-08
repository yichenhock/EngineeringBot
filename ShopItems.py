import parameters

PATH = parameters.PATH

class ShopItems():
    def __init__(self, item, cost, description): 
        self.item = item
        self.cost = cost
        self.description = description

    def importItems(self):
        with open(PATH+'ShopItems.txt','r') as f:
            pass
class Inventory: 
    def __init__(self):
        self.items = []
    def add(self, item):
        self.items.append(item)
    def remove(self, item):
        if item in self.items:
            self.items.remove(item)
            return True
        return False
    def get_items(self):
        return self.items

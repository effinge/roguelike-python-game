import random

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = [['#' for _ in range(height)] for _ in range(width)] #двумерный список клеток
        self.objects = [[None for _ in range(height)] for _ in range(width)] #двумерный список объектов

    def get_cell(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[x][y]
        return None

    def set_floor(self, x, y) -> None:
        if 0 <= x < self.width and 0 <= y < self.height:
            self.tiles[x][y] = '.'

    def is_walkable(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[x][y] == '.'
        return False
    
    def place_object(self, x, y, symbol):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.objects[x][y] = symbol
        
    def remove_object(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.objects[x][y] = None

    def generate_empty_map(self):
        for x in range(self.width):
            for y in range(self.height):
                self.tiles[x][y] = '#'
                self.objects[x][y] = None
    
    def get_random_free_cell(self):
        free_cells = [(x, y) for x in range(self.width) for y in range(self.height)
                      if self.is_walkable(x, y) and self.objects[x][y] is None]
        
        return random.choice(free_cells) if free_cells else None
    
    def get_object(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.objects[x][y]
        return None
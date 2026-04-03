import random

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = [['T' for _ in range(height)] for _ in range(width)] #двумерный список клеток
        self.objects = [['O' for _ in range(height)] for _ in range(width)] #двумерный список объектов

    def set_floor(self, x, y) -> None:
        if 0 <= x < self.width and 0 <= y < self.height:
            self.tiles[x][y] = '.'

    def is_walkable(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[x][y] == '.'
        return False
    
    def place_object(self, x, y, symbol: str) -> None:
        if 0 <= x < self.width and 0 <= y < self.height:
            self.objects[x][y] = symbol
        
    def remove_object(self, x, y) -> None:
        if 0 <= x < self.width and 0 <= y < self.height:
            self.objects[x][y] = None

    def generate_empty_map(self) -> None:
        for x in range(self.width):
            for y in range(self.height):
                self.tiles[x][y] = 'T'
                self.objects[x][y] = 'O'
    
    def get_random_free_cell(self) -> tuple | None:
        free_cells = [(x, y) for x in range(self.width) for y in range(self.height)
                      if self.is_walkable(x, y) and self.objects[x][y] is None]
        
        return random.choice(free_cells) if free_cells else None
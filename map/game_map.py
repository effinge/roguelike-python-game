class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = [['T' for _ in range(height)] for _ in range(width)] #двумерный список клеток
        self.objects = [['O' for _ in range(height)] for _ in range(width)] #двумерный список объектов

    def is_walkable(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
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
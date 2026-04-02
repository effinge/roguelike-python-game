class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def is_walkable(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
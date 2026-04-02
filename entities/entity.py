class Entity:
    def __init__(self, x, y, hp, damage, symbol):
        self.x = x
        self.y = y
        self.hp = hp
        self.damage = damage
        self.symbol = symbol
    def move(self,dx,dy):
        new_x = self.x + dx
        new_y = self.y + dy 
        
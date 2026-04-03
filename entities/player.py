from entities.entity import Entity

class Player(Entity):
    def __init__(self, x, y, hp, damage, symbol):
        super().__init__(x, y, hp, damage, "@")
    
import random
from .entity import Entity

class Enemy(Entity):

    def __init__(self, x: int, y: int, name: str = "Гоблин", hp: int = 10, damage: int = 3, symbol: str = "g"):
        super().__init__(x, y, symbol, name, hp, damage)

import random
from .entity import Entity

class Enemy(Entity):

    def __init__(self, x: int, y: int, name: str = "Гоблин", hp: int = 10, damage: int = 3, symbol: str = "g"):
        super().__init__(x, y, symbol, name, hp, damage)

    def take_turn(self, game_map, player):
        if not self.is_alive():
            return
        # Если игрок рядом  атакуем
        if abs(self.x - player.x) <= 1 and abs(self.y - player.y) <= 1:
            damage = self.attack(player)
            print(f" {self.name} атакует вас и наносит {damage} урона!")
            return
        # Случайное движение в 4 стороны
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        dx, dy = random.choice(directions)
        self.move(dx, dy, game_map)
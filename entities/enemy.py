import random
from .entity import Entity

class Enemy(Entity):
    """Класс врага"""

    def __init__(self, x: int, y: int, name: str = "Гоблин", hp: int = 10, damage: int = 3, symbol: str = "g"):
        super().__init__(x, y, hp, damage, symbol)
        self.name = name

    def take_turn(self, game_map, player):
        """Один ход врага"""
        if not self.is_alive():
            return

        # Атака, если игрок рядом
        if abs(self.x - player.x) <= 1 and abs(self.y - player.y) <= 1:
            damage = self.attack(player)
            print(f"{self.name} атакует вас и наносит {damage} урона!")
            return

        # Случайное движение
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        dx, dy = random.choice(directions)
        self.move(dx, dy, game_map)

    def die(self, game_map=None):
        """Враг умирает + удаляется с карты"""
        print(f"{self.name} погиб!")
        self.symbol = "%"                    # можно оставить труп

        if game_map:
            self.remove_from_map(game_map)
            
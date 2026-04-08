import random
from .entity import Entity

class Enemy(Entity):

    def __init__(self, x, y, hp, damage, symbol, name):
        super().__init__(x, y, hp, damage, symbol)
        self.name = name

    def ai_move(self, game_map, player):
        if not self.is_alive():
            return

        if abs(self.x - player.x) <= 1 and abs(self.y - player.y) <= 1:
            damage = self.attack(player)
            return

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        dx, dy = random.choice(directions)
        self.move(dx, dy, game_map)

    def die(self, game_map=None):
        print(f"{self.name} погиб!")

        if game_map:
            self.remove_from_map(game_map)
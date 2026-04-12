import random
from .entity import Entity

class Enemy(Entity):

    def __init__(self, x, y, hp, damage, symbol, name):
        super().__init__(x, y, hp, damage, symbol)
        self.name = name

    def ai_move(self, game_map, player):

        if not self.is_alive():
            return ("blocked",)

        if abs(self.x - player.x) <= 1 and abs(self.y - player.y) <= 1:
            damage = self.attack(player)
            return ("attack", damage)

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        dx, dy = random.choice(directions)

        new_x = self.x + dx
        new_y = self.y + dy

        if not game_map.is_walkable(new_x, new_y):
            return ("move", dx, dy, False)

        if player.x == new_x and player.y == new_y and player.is_alive():
            damage = self.attack(player)
            return ("attack", damage)

        if 0 <= new_x < game_map.width and 0 <= new_y < game_map.height:
            if game_map.objects[new_x][new_y] is not None:
                return ("move", dx, dy, False)

        self.x = new_x
        self.y = new_y
        return ("move", dx, dy, True)

    def die(self, game_map=None):
        if game_map:
            self.remove_from_map(game_map)
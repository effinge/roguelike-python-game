from ui.event_log import EventLog

class Entity:


    def __init__(self, x, y, hp, damage, symbol):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = hp
        self.damage = damage
        self.symbol = symbol
        self.event_log = EventLog()

    def move(self, dx, dy, game_map):
        new_x = self.x + dx
        new_y = self.y + dy

        if game_map.is_walkable(new_x, new_y):
            self.x = new_x
            self.y = new_y
            return True
        return False

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0

    def is_alive(self):
        return self.hp > 0

    def is_dead(self):
        return self.hp <= 0

    def attack(self, target):
        if target and target.is_alive():
            target.take_damage(self.damage)
            return self.damage
        return 0

    def remove_from_map(self, game_map):
            game_map.remove_object(self.x, self.y)
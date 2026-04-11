from .entity import Entity

class Player(Entity):

    def __init__(self, x, y, hp, damage, symbol):
        super().__init__(x, y, hp, damage, symbol)
    
    def move(self, dx, dy, game_map):
        new_x = self.x + dx
        new_y = self.y + dy
        
        if game_map.is_walkable(new_x, new_y):
            self.x = new_x
            self.y = new_y
            return True
        
        return False
        
    

    def handle_input(self, key, game_map):
        dx, dy = 0, 0
        k = key.lower()

        if k in ['w', 'ц']:
            dy = -1
        elif k in ['s', 'ы']:
            dy = 1
        elif k in ['a', 'ф']:
            dx = -1
        elif k in ['d', 'в']:
            dx = 1
        else:
            return False

        return self.move(dx, dy, game_map)

    def attack_target(self, target):
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            damage = self.attack(target)
            print(f"Вы атакуете {target.name} и наносите {damage} урона!")
            return True
        else:
            print("Враг слишком далеко!")
            return False
from entities.entity import Entity

class Player(Entity):
    def __init__(self, x, y, hp, damage, symbol):
        super().__init__(x, y, hp, damage, "@")
    
    def move(self, dx, dy, game_map):
        new_x = self.x + dx
        new_y = self.y + dy
        
        if game_map.is_walkable(new_x, new_y):
            self.x = new_x
            self.y = new_y
            return True
        
        return False
        
    
    def handle_input(self, key: str, game_map) -> bool:
        dx, dy = 0, 0
        k = key.lower()

        if k in ['w', 'ц']:      # вверх
            dy = -1
        elif k in ['s', 'ы']:    # вниз
            dy = 1
        elif k in ['a', 'ф']:    # влево
            dx = -1
        elif k in ['d', 'в']:    # вправо
            dx = 1
        else:
            return False

        # Пытаемся двигаться
        return self.move(dx, dy, game_map)
    
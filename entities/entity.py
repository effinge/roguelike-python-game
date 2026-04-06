class Entity:
    def __init__(self, x: int, y: int, hp: int = 20, damage: int = 5, symbol: str = "@"):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = hp          
        self.damage = damage
        self.symbol = symbol

    def move(self, dx: int, dy: int, game_map) -> bool:
        """Перемещение с проверкой стен"""
        new_x = self.x + dx
        new_y = self.y + dy

        if game_map.is_walkable(new_x, new_y):
            self.x = new_x
            self.y = new_y
            return True
        return False

    def take_damage(self, amount: int):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0

    def is_alive(self) -> bool:
        return self.hp > 0

    def attack(self, target) -> int:
        if target and target.is_alive():
            target.take_damage(self.damage)
            return self.damage
        return 0
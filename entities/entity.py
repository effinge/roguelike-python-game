class Entity:
    def __init__(self, x, y, hp, damage, symbol):
        self.x = x
        self.y = y
        self.hp = hp
        self.damage = damage
        self.symbol = symbol

    def move(self,dx,dy):
        new_x = self.x + dx
        new_y = self.y + dy

    def take_damage(self, amount: int):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0  
    
    def attack(self, target) -> int:
        if target and target.is_alive():
            target.take_damage(self.damage)
            return self.damage
        return 0
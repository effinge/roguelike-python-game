import random
from .entity import Entity

class Enemy(Entity):

    def __init__(self, x, y, hp, damage, symbol, name, vision_radius, ai_type):
        super().__init__(x, y, hp, damage, symbol)
        self.name = name
        self.vision_radius = vision_radius
        self.ai_type = ai_type
        self.state = "idle"
        self.last_seen_player_pos = None

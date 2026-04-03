import json
import random
from .game_map import GameMap

class MapGenerator:
    def __init__(self, config_path):

        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.width = self.config["map_width"]
        self.height = self.config["map_height"]
        self.num_rooms = self.config["num_rooms"]
        self.room_min_size = self.config["room_min_size"]
        self.room_max_size = self.config["room_max_size"]
        self.num_enemies = self.config["num_enemies"]
        self.num_items = self.config["num_items"]
    
    def generate_rooms(self, game_map: GameMap) -> list:
        rooms = []
        max_attempts = 1000

        for _ in range(self.num_rooms):
            for _ in range(max_attempts):
                w = random.randint(self.room_min_size, self.room_max_size)
                h = random.randint(self.room_min_size, self.room_max_size)
                x = random.randint(1, game_map.width - w - 1)
                y = random.randint(1, game_map.height - h - 1)

                new_rect = (x, y, w, h)
                # Проверка пересечения с существующими комнатами
                if not any(self._rectangles_intersect(new_rect, r) for r in rooms):
                    rooms.append(new_rect)
                    self._create_room(game_map, x, y, w, h)
                    break
        return rooms
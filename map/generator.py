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
    
    def create_room(self, game_map: GameMap, x, y, w, h) -> None:
        for i in range(x, x + w):
            for j in range(y, y + h):
                game_map.set_floor(i, j)

    def rectengle_intersect(self, r1: tuple, r2: tuple) -> None:
        x1, y1, w1, h1 = r1
        x2, y2, w2, h2 = r2
        return not(x1 + w1 < x2 or x2 + w2 < x1 or y1 + h1 < y2 or y2 + h2 < y1)

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
                    self.create_room(game_map, x, y, w, h)
                    break
        return rooms    
    def create_horizontal_corridor(self, game_map: GameMap, x1, x2, y) -> None:
        for x in range(min(x1, x2), max(x1, x2) + 1):
    def create_vertical_corridor(self, game_map: GameMap, y1, y2, x) -> None:
        for y in range(min(y1, y2), max(y1, y2) + 1):
            game_map.set_floor(x, y)
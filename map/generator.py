import json
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
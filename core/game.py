import json

from map.game_map import GameMap
from entities.player import Player

class Game:
    def __init__(self):
        self.config = self.load_config()
        
        map_width = self.config["map"]["width"]
        map_height = self.config["map"]["height"]
        
        player_x = self.config["player"]["start_x"]
        player_y = self.config["player"]["start_y"]
        player_hp = self.config["player"]["hp"]
        player_damage = self.config["player"]["damage"]
        
        self.game_map = GameMap(map_width,map_height)
        self.player = Player(player_x,player_y,player_hp,player_damage)
        
        self.is_running = True
        
    def load_config(self):
        with open("config/game_config.json", "r") as file:
            return json.load(file)
        
    def run(self):
        print("test load")
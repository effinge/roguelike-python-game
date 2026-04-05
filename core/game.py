import json

from map.generator import MapGenerator
from entities.player import Player
from ui.renderer import Renderer

class Game:
    def __init__(self):
        self.config = self.load_config()
        
        self.game_map = None
        self.player = None
        self.renderer = Renderer()
        self.is_running = True
        
        self.setup_game()
        
    def load_config(self):
        with open("config/game_config.json", "r") as file:
            return json.load(file)
    
    def find_object(self, symbol):
        for x in range(self.game_map.width):
            for y in range(self.game_map.height):
                if self.game_map.objects[x][y] == symbol:
                    return (x,y)
        return None

    def update_player_on_map(self, old_x, old_y):
        self.game_map.remove_object(old_x, old_y)
        self.game_map.place_object(self.player.x, self.player.y, self.player.symbol)
    
    
    def run(self):
        print("test load")
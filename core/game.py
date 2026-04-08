import json

from map.generator import MapGenerator
from entities.player import Player
from ui.renderer import Renderer
<<<<<<< HEAD
from ui.event_log import EventLog

=======
>>>>>>> main
class Game:
    def __init__(self):
        self.config = self.load_config()
        
        self.game_map = None
        self.player = None
        self.renderer = Renderer()
        self.is_running = True
        self.event_log = EventLog()
        self.setup_game()
        
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
    
    def setup_game(self):
        generator = MapGenerator("config/game_config.json")
        self.game_map = generator.generate()
        
        player_pos = self.find_object("@")
        
        if player_pos is None:
            player_x = self.config["player"]["start_x"]
            player_y = self.config["player"]["start_y"]
        else:
            player_x,player_y = player_pos
            self.game_map.remove_object(player_x, player_y)
        
        self.player = Player(
            player_x,
            player_y,
            self.config["player"]["hp"],
            self.config["player"]["damage"],
            "@"
        )
        
        self.game_map.place_object(self.player.x, self.player.y, self.player.symbol)

    def handle_input(self, command):
        if command == "q":
            self.is_running = False
            return
            
        old_x = self.player.x
        old_y = self.player.y
            
        moved = self.player.handle_input(command,self.game_map)
            
        if moved:
            self.update_player_on_map(old_x, old_y)
<<<<<<< HEAD
            self.event_log.add(f'Игрок перешел в ({self.player.x}, {self.player.y})')
        else:
            self.event_log.add(f'Нельзя пройти сюда')
=======

>>>>>>> main
    def run(self):
        while self.is_running:
            self.renderer.draw(self)
            command = input("\nДействие: ").strip().lower()
            self.handle_input(command)
        print("Игра закончена.")
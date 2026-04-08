import json

from map.generator import MapGenerator
from entities.player import Player
from entities.enemy import Enemy
from ui.renderer import Renderer 
from core.win_conditions import WinConditions
<<<<<<< HEAD
from ui.event_log import EventLog

=======
>>>>>>> main
class Game:
    def __init__(self):
        self.config = self.load_config()
        
        self.game_map = None
        self.player = None
        self.enemies = []
        self.renderer = Renderer()
        self.is_running = True
        self.win_conditions = WinConditions(self)
        
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

    def find_objects(self, symbol):
        found = []
        for x in range(self.game_map.width):
            for y in range(self.game_map.height):
                if self.game_map.objects[x][y] == symbol:
                    found.append((x, y))
        return found

    def update_player_on_map(self, old_x, old_y):
        
        tx, ty = self.player.x, self.player.y
        target_obj = None
        if 0 <= tx < self.game_map.width and 0 <= ty < self.game_map.height:
            target_obj = self.game_map.objects[tx][ty]

        self.game_map.remove_object(old_x, old_y)

        self.game_map.place_object(self.player.x, self.player.y, self.player.symbol)

        return target_obj == '>'

    def run_enemy_turns(self):
        for enemy in list(self.enemies):
            if not enemy.is_alive():
                enemy.remove_from_map(self.game_map)
                self.enemies.remove(enemy)

            self.game_map.remove_object(enemy.x, enemy.y)


            enemy.ai_move(self.game_map, self.player)

            if not enemy.is_alive():
                enemy.remove_from_map(self.game_map)
                self.enemies.remove(enemy)

            self.game_map.place_object(enemy.x, enemy.y, enemy.symbol)
            
            if not self.player.is_alive():
                print("Вы погибли!")
                self.is_running = False
                return
    
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
        
        
        
        goblin_positions = self.find_objects("g")
        goblin_instances = []
        if goblin_positions:
            for x, y in goblin_positions:
                self.game_map.remove_object(x, y)
                gob = Enemy(
                    x,
                    y,
                    self.config["enemies"]["goblin"]["hp"],
                    self.config["enemies"]["goblin"]["damage"],
                    "g",
                    "goblin"
                )
                goblin_instances.append(gob)
                self.game_map.place_object(gob.x, gob.y, gob.symbol)
        else:
            count = self.config.get("generation", {}).get("num_goblins", 1)
            for _ in range(count):
                pos = self.game_map.get_random_free_cell()
                if pos:
                    x, y = pos
                    gob = Enemy(
                        x,
                        y,
                        self.config["enemies"]["goblin"]["hp"],
                        self.config["enemies"]["goblin"]["damage"],
                        "g",
                        "goblin"
                    )
                    goblin_instances.append(gob)
                    self.game_map.place_object(gob.x, gob.y, gob.symbol)

        troll_positions = self.find_objects("t")
        troll_instances = []
        if troll_positions:
            for tx, ty in troll_positions:
                self.game_map.remove_object(tx, ty)
                tr = Enemy(
                    tx,
                    ty,
                    self.config["enemies"]["troll"]["hp"],
                    self.config["enemies"]["troll"]["damage"],
                    "t",
                    "troll"
                )
                troll_instances.append(tr)
                self.game_map.place_object(tr.x, tr.y, tr.symbol)
        else:
            count = self.config.get("generation", {}).get("num_trolls", 0)
            for _ in range(count):
                pos = self.game_map.get_random_free_cell()
                if pos:
                    tx, ty = pos
                    tr = Enemy(
                        tx,
                        ty,
                        self.config["enemies"]["troll"]["hp"],
                        self.config["enemies"]["troll"]["damage"],
                        "t",
                        "troll"
                    )
                    troll_instances.append(tr)
                    self.game_map.place_object(tr.x, tr.y, tr.symbol)
        
        self.enemies.extend(goblin_instances)
        self.enemies.extend(troll_instances)
        
        self.g_enemy = goblin_instances[0] if goblin_instances else None
        self.t_enemy = troll_instances[0] if troll_instances else None
        
        

    def handle_input(self, command):
        if command == "q":
            self.is_running = False
            return
            
        old_x = self.player.x
        old_y = self.player.y
            
        moved = self.player.handle_input(command,self.game_map)

        if moved:
            stepped_on_exit = self.update_player_on_map(old_x, old_y)
            if stepped_on_exit:
                print("Вы выиграли!")
                self.is_running = False
                return

            # после хода игрока выполняем ходы всех врагов
            self.run_enemy_turns()
            # проверить условие победы (например, игрок на выходе) — на всякий случай
            if self.win_conditions.check_win():
                print("Вы выиграли!")
                self.is_running = False
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
            if self.win_conditions.check_win():
                print("Вы выиграли!")
                self.is_running = False
        print("Игра закончена.")
import json
import random

from map.generator import MapGenerator
from entities.player import Player
from entities.enemy import Enemy
from core.game_state import GameState
from systems.visibility_system import VisibilitySystem
from ui.renderer import Renderer
from ui.event_log import EventLog
from ui.inventory import Inventory
from core.win_conditions import WinConditions
from items.item import ItemFactory


class GameFactory:
    def __init__(self):
        self.path = "config/game_config.json"
    @staticmethod
    def load_config(path="config/game_config.json"):
        with open(path, "r") as file:
            config = json.load(file)
        return config
    
    @staticmethod
    def find_object(game_map, symbol):
        for x in range(game_map.width):
            for y in range(game_map.height):
                if game_map.objects[x][y] == symbol:
                    return (x, y)
        return None
    
    @staticmethod
    def find_objects(game_map, symbol):
        positions = []
        for x in range(game_map.width):
            for y in range(game_map.height):
                if game_map.objects[x][y] == symbol:
                    positions.append((x, y))
        return positions
    
    @staticmethod
    def create_enemy(config, x, y, cfg_key, symbol, default_name):
        cfg = config.get("enemies", {}).get(cfg_key, {})
        name = cfg.get("name", default_name)
        hp = cfg.get("hp")
        damage = cfg.get("damage")
        return Enemy(x, y, hp, damage, symbol, name)

    @staticmethod
    def populate_items_map(game_map):
        items_map = {}
        available_items = list(ItemFactory.load_all().values())
        positions = GameFactory.find_objects(game_map, "I")

        if not available_items or not positions:
            return items_map

        for ix, iy in positions:
            chosen = random.choice(available_items)
            items_map[(ix, iy)] = chosen

        return items_map
    
    @staticmethod
    def create_new_game():
        config = GameFactory.load_config()
        generator = MapGenerator("config/game_config.json")
        game_map = generator.generate()

        player_pos = GameFactory.find_object(game_map, "@")
        if player_pos is None:
            player_x = config["player"]["start_x"]
            player_y = config["player"]["start_y"]
        else:
            player_x, player_y = player_pos
            game_map.remove_object(player_x, player_y)

        player = Player(
            player_x,
            player_y,
            config["player"]["hp"],
            config["player"]["damage"],
            "@",
        )
        game_map.place_object(player.x, player.y, player.symbol)

        enemies = []

        goblin_positions = GameFactory.find_objects(game_map, "g")
        if goblin_positions:
            for x, y in goblin_positions:
                game_map.remove_object(x, y)
                gob = GameFactory.create_enemy(config, x, y, "goblin", "g", "goblin")
                enemies.append(gob)
                game_map.place_object(gob.x, gob.y, gob.symbol)

        troll_positions = GameFactory.find_objects(game_map, "t")
        if troll_positions:
            for x, y in troll_positions:
                game_map.remove_object(x, y)
                tr = GameFactory.create_enemy(config, x, y, "troll", "t", "troll")
                enemies.append(tr)
                game_map.place_object(tr.x, tr.y, tr.symbol)

        event_log = EventLog()
        inventory = Inventory()
        renderer = Renderer()
        items_map = GameFactory.populate_items_map(game_map)

        state = GameState(
            config=config,
            game_map=game_map,
            player=player,
            enemies=enemies,
            event_log=event_log,
            inventory=inventory,
            items_map=items_map,
            renderer=renderer,
            win_conditions=None,
            is_running=True,
            tick=float(config.get("tick", 0.5)),
        )

        state.win_conditions = WinConditions(state)
        VisibilitySystem.update(state)
        return state
    
    @staticmethod
    def create_enemy(config, x, y, cfg_key, symbol, default_name):
        cfg = config.get("enemies", {}).get(cfg_key, {})
        name = cfg.get("name", default_name)
        hp = cfg.get("hp")
        damage = cfg.get("damage")

        vision_cfg = config.get("vision", {})

        if cfg_key == "goblin":
            vision_radius = vision_cfg.get("goblin_radius", 5)
            ai_type = "goblin"
        elif cfg_key == "troll":
            vision_radius = vision_cfg.get("troll_radius", 7)
            ai_type = "troll"
        else:
            vision_radius = vision_cfg.get("enemy_radius", 6)
            ai_type = "default"

        return Enemy(
            x,
            y,
            hp,
            damage,
            symbol,
            name,
            vision_radius,
            ai_type,
        )

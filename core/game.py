import json
import random

from map.generator import MapGenerator
from entities.player import Player
from entities.enemy import Enemy
from ui.renderer import Renderer 
from core.win_conditions import WinConditions
from ui.event_log import EventLog
from ui.inventory import Inventory, InventoryUI
from items.item import ItemFactory
class Game:
    def __init__(self):
        self.config = self.load_config()

        self.game_map = None
        self.player = None
        self.enemies = []
        self.event_log = EventLog()
        self.inventory = Inventory()
        self.items_map = {}
        self.renderer = Renderer()
        self.is_running = True
        self.win_conditions = WinConditions(self)

        self.setup_game()

    def load_config(self):
        with open("config/game_config.json", "r", encoding="utf-8") as file:
            return json.load(file)


    def _create_enemy(self, x, y, cfg_key, symbol, default_name) -> Enemy:
        cfg = self.config.get("enemies", {}).get(cfg_key, {})
        name = cfg.get("name", default_name)
        hp = cfg.get("hp")
        damage = cfg.get("damage")
        return Enemy(x, y, hp, damage, symbol, name)

    def _populate_items_map(self):
        available_items = list(ItemFactory.load_all().values())
        positions = self.find_objects("I")
        if not available_items or not positions:
            return
        for (ix, iy) in positions:
            chosen = random.choice(available_items)
            self.items_map[(ix, iy)] = chosen

    # ----------------- map queries -----------------
    def find_object(self, symbol):
        for x in range(self.game_map.width):
            for y in range(self.game_map.height):
                if self.game_map.objects[x][y] == symbol:
                    return (x, y)
        return None

    def find_objects(self, symbol):
        found = []
        for x in range(self.game_map.width):
            for y in range(self.game_map.height):
                if self.game_map.objects[x][y] == symbol:
                    found.append((x, y))
        return found

    def get_enemy_at(self, x, y):
        for e in self.enemies:
            if e.x == x and e.y == y and e.is_alive():
                return e
        return None

    def _symbol_to_item(self, symbol):
        all_items = ItemFactory.load_all()
        for it in all_items.values():
            if getattr(it, 'symbol', None) == symbol:
                return it
        return None

    def _clone_item(self, item):
        if item is None:
            return None
        cls_name = item.__class__.__name__
        if cls_name == 'Weapon':
            return type(item)(getattr(item, 'id', None), getattr(item, 'name', None), getattr(item, 'damage', None), getattr(item, 'symbol', None))
        if cls_name == 'Potion':
            return type(item)(getattr(item, 'id', None), getattr(item, 'name', None), getattr(item, 'properties', None), getattr(item, 'symbol', None))
        try:
            return type(item)(getattr(item, 'id', None), getattr(item, 'name', None), getattr(item, 'symbol', None), getattr(item, 'item_type', None), getattr(item, 'properties', None))
        except Exception:
            return item

    # ----------------- player/map updates -----------------
    def update_player_on_map(self, old_x, old_y):
        # remember what was on the target cell before placing the player
        tx, ty = self.player.x, self.player.y
        target_obj = None
        if 0 <= tx < self.game_map.width and 0 <= ty < self.game_map.height:
            target_obj = self.game_map.objects[tx][ty]

        # restore item symbol on the old cell if an item exists there
        if (old_x, old_y) in getattr(self, "items_map", {}):
            item = self.items_map[(old_x, old_y)]
            symbol = item.symbol if getattr(item, "symbol", None) else "I"
            self.game_map.place_object(old_x, old_y, symbol)
        else:
            self.game_map.remove_object(old_x, old_y)

        # place player symbol on new position
        self.game_map.place_object(self.player.x, self.player.y, self.player.symbol)

        return target_obj == ">"

    def attack_enemy_at(self, x, y):
        for enemy in list(self.enemies):
            if enemy.x == x and enemy.y == y:
                damage = self.player.attack(enemy)
                self.event_log.add(f'Вы атаковали {enemy.name} и нанесли {damage} урона')
                if not enemy.is_alive():
                    self.event_log.add(f'{enemy.name} погиб')
                    enemy.remove_from_map(self.game_map)
                    self.enemies.remove(enemy)
                return True
        return False

    # enemy turns 
    def run_enemy_turns(self):
        for enemy in list(self.enemies):
            if not enemy.is_alive():
                enemy.remove_from_map(self.game_map)
                try:
                    self.enemies.remove(enemy)
                except ValueError:
                    pass
                continue

            # remove old object marker
            self.game_map.remove_object(enemy.x, enemy.y)

            result = enemy.ai_move(self.game_map, self.player)

            if isinstance(result, tuple) and result[0] == "attack":
                self.event_log.add(f'Вас атакует {enemy.name}!')

            # if enemy died during its action, remove it
            if not enemy.is_alive():
                self.event_log.add(f'{enemy.name} погиб')
                enemy.remove_from_map(self.game_map)
                try:
                    self.enemies.remove(enemy)
                except ValueError:
                    pass
                continue

            # place enemy on its (possibly new) position
            self.game_map.place_object(enemy.x, enemy.y, enemy.symbol)

            if not self.player.is_alive():
                self.event_log.add('Игрок погиб!')
                self.is_running = False
                return

    # setup
    def setup_game(self):
        generator = MapGenerator("config/game_config.json")
        self.game_map = generator.generate()

        # player
        player_pos = self.find_object("@")
        if player_pos is None:
            player_x = self.config["player"]["start_x"]
            player_y = self.config["player"]["start_y"]
        else:
            player_x, player_y = player_pos
            self.game_map.remove_object(player_x, player_y)

        self.player = Player(
            player_x,
            player_y,
            self.config["player"]["hp"],
            self.config["player"]["damage"],
            "@",
        )

        self.game_map.place_object(self.player.x, self.player.y, self.player.symbol)

        # enemies from markers or spawn by config
        self.enemies = []
        goblin_positions = self.find_objects("g")
        if goblin_positions:
            for x, y in goblin_positions:
                self.game_map.remove_object(x, y)
                gob = self._create_enemy(x, y, "goblin", "g", "goblin")
                self.enemies.append(gob)
                self.game_map.place_object(gob.x, gob.y, gob.symbol)
        else:
            count = self.config.get("generation", {}).get("num_goblins", 0)
            for _ in range(count):
                cell = self.game_map.get_random_free_cell()
                if cell:
                    x, y = cell
                    gob = self._create_enemy(x, y, "goblin", "g", "goblin")
                    self.enemies.append(gob)
                    self.game_map.place_object(gob.x, gob.y, gob.symbol)

        troll_positions = self.find_objects("t")
        if troll_positions:
            for x, y in troll_positions:
                self.game_map.remove_object(x, y)
                tr = self._create_enemy(x, y, "troll", "t", "troll")
                self.enemies.append(tr)
                self.game_map.place_object(tr.x, tr.y, tr.symbol)
        else:
            count = self.config.get("generation", {}).get("num_trolls", 0)
            for _ in range(count):
                cell = self.game_map.get_random_free_cell()
                if cell:
                    x, y = cell
                    tr = self._create_enemy(x, y, "troll", "t", "troll")
                    self.enemies.append(tr)
                    self.game_map.place_object(tr.x, tr.y, tr.symbol)

        # populate items map for any 'I' markers
        self._populate_items_map()

    # input handling 
    def handle_input(self, command):
        if not command:
            return

        command = command.strip().lower()

        if command == "q":
            self.is_running = False
            return

        if command == "f":
            # attack adjacent enemy
            adj_enemies = [e for e in self.enemies if e.is_alive() and abs(e.x - self.player.x) <= 1 and abs(e.y - self.player.y) <= 1]
            if not adj_enemies:
                self.event_log.add('Врага рядом нет')
                self.run_enemy_turns()
                return

            target = min(adj_enemies, key=lambda e: abs(e.x - self.player.x) + abs(e.y - self.player.y))
            attacked = self.player.attack_target(target)
            if attacked:
                self.event_log.add(f'Вы атакуете {target.name} и наносите {self.player.damage} урона')
                if not target.is_alive():
                    self.event_log.add(f'{target.name} погиб')
                    target.remove_from_map(self.game_map)
                    try:
                        self.enemies.remove(target)
                    except ValueError:
                        pass
            else:
                self.event_log.add('Атака не удалась')

            self.run_enemy_turns()
            return

        if command == 'e':
            pos = (self.player.x, self.player.y)
            item = self.items_map.get(pos)
            if item:
                self.inventory.add(item)
                self.game_map.remove_object(pos[0], pos[1])
                del self.items_map[pos]
                self.event_log.add(f'Вы подобрали {item.name}')
                self.run_enemy_turns()
            else:
                self.event_log.add('Здесь нет предмета')
            return

        if command == 'y':
            InventoryUI.open(self)
            return

        # movement
        old_x = self.player.x
        old_y = self.player.y

        dx, dy = self.player.get_move_delta(command) if hasattr(self.player, 'get_move_delta') else (0, 0)

        if dx == 0 and dy == 0:
            self.event_log.add('Неправильная команда или нет движения')
            return

        target_x = old_x + dx
        target_y = old_y + dy

        enemy = self.get_enemy_at(target_x, target_y)
        if enemy and enemy.is_alive():
            damage = self.player.attack(enemy)
            self.event_log.add(f'Вы атаковали {enemy.name} и нанесли {damage} урона!')
            if not enemy.is_alive():
                self.event_log.add(f'{enemy.name} погиб')
                enemy.remove_from_map(self.game_map)
                try:
                    self.enemies.remove(enemy)
                except ValueError:
                    pass

            self.run_enemy_turns()
            return

        if not self.game_map.is_walkable(target_x, target_y):
            self.event_log.add('Нельзя пройти сюда')
            return

        # check objects on target cell
        if 0 <= target_x < self.game_map.width and 0 <= target_y < self.game_map.height:
            obj = self.game_map.objects[target_x][target_y]
            if obj is not None:
                if obj == '>':
                    # check win without overwriting the exit
                    if self.win_conditions.check_win(target_x, target_y):
                        self.player.x = target_x
                        self.player.y = target_y
                        self.update_player_on_map(old_x, old_y)
                        self.event_log.add(f'Игрок перешел в ({self.player.x}, {self.player.y}) и выиграл!')
                        self.is_running = False
                        return
                    else:
                        self.event_log.add('Клетка занята')
                        return
                item_from_symbol = self._symbol_to_item(obj)
                if item_from_symbol is not None or obj == 'I':
                    # ensure items_map has an item instance at this location so pickup works
                    if (target_x, target_y) not in self.items_map:
                        base_item = item_from_symbol if item_from_symbol is not None else None
                        chosen = self._clone_item(base_item) if base_item is not None else None
                        if chosen is None:
                            # fallback: pick any random item
                            all_items = ItemFactory.load_all()
                            items = list(all_items.values())
                            chosen = self._clone_item(random.choice(items)) if items else None
                        if chosen is not None:
                            self.items_map[(target_x, target_y)] = chosen
                    # allow stepping on item cell
                    pass
                else:
                    self.event_log.add('Клетка занята')
                    return

        moved = self.player.move(dx, dy, self.game_map)

        if moved:
            self.update_player_on_map(old_x, old_y)
            self.event_log.add(f'Игрок переместился в ({self.player.x}, {self.player.y})')
            self.run_enemy_turns()
        else:
            self.event_log.add('Нельзя пройти сюда')

    def run(self):
        while self.is_running:
            self.renderer.draw(self)

            command = input("\nДействие: ").strip().lower()
            self.handle_input(command)

        print("Игра закончена.")
from systems.combat_system import CombatSystem
from systems.enemy_turn_system import EnemyTurnSystem
from systems.item_system import ItemSystem
from systems.map_sync import MapSync
from systems.visibility_system import VisibilitySystem
from ui.inventory import InventoryUI


class CommandHandler:
    def __init__(self, terminal):
        self.terminal = terminal

    def handle(self, command, state):
        if not command:
            return

        command = command.strip().lower()

        if command == "q":
            state.is_running = False
            return

        if command == "f":
            self._handle_attack(state)
            return

        if command == "e":
            acted = ItemSystem.pickup_item(state)
            if acted:
                EnemyTurnSystem.run(state)
            return

        if command == "y":
            self.terminal.restore()
            try:
                InventoryUI.open(state)
            finally:
                self.terminal.enable()
            return

        self._handle_move(command, state)

    def _handle_attack(self, state):
        adj_enemies = [
            e for e in state.enemies
            if e.is_alive() and abs(e.x - state.player.x) <= 1 and abs(e.y - state.player.y) <= 1
        ]

        if not adj_enemies:
            state.event_log.add("Врага рядом нет")
            EnemyTurnSystem.run(state)
            return

        target = min(
            adj_enemies,
            key=lambda e: abs(e.x - state.player.x) + abs(e.y - state.player.y)
        )

        CombatSystem.player_attack(state, target)
        if state.is_running:
            EnemyTurnSystem.run(state)

    def _handle_move(self, command, state):
        old_x = state.player.x
        old_y = state.player.y

        dx, dy = state.player.get_move_delta(command)
        if dx == 0 and dy == 0:
            state.event_log.add("Неправильная команда или нет движения")
            return

        target_x = old_x + dx
        target_y = old_y + dy

        enemy = CombatSystem.get_enemy_at(state, target_x, target_y)
        if enemy and enemy.is_alive():
            CombatSystem.player_attack(state, enemy)
            if state.is_running:
                EnemyTurnSystem.run(state)
            return

        if not state.game_map.is_walkable(target_x, target_y):
            state.event_log.add("Нельзя пройти сюда")
            return

        if 0 <= target_x < state.game_map.width and 0 <= target_y < state.game_map.height:
            obj = state.game_map.objects[target_x][target_y]

            if obj is not None:
                if obj == ">":
                    if state.win_conditions.check_win(target_x, target_y):
                        state.player.x = target_x
                        state.player.y = target_y
                        MapSync.move_player(state, old_x, old_y)
                        state.event_log.add(
                            f"Игрок перешел в ({state.player.x}, {state.player.y}) и выиграл!"
                        )
                        state.is_running = False
                        return
                    else:
                        state.event_log.add("Клетка занята")
                        return

                item_from_symbol = ItemSystem.symbol_to_item(obj)
                if item_from_symbol is not None or obj == "I":
                    ItemSystem.ensure_item_on_position(state, target_x, target_y, obj)
                else:
                    state.event_log.add("Клетка занята")
                    return

        moved = state.player.move(dx, dy, state.game_map)
        if moved:
            MapSync.move_player(state, old_x, old_y)
            VisibilitySystem.update(state)
            state.event_log.add(f"Игрок переместился в ({state.player.x}, {state.player.y})")
            EnemyTurnSystem.run(state)
            
        else:
            state.event_log.add("Нельзя пройти сюда")
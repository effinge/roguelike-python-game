from systems.map_sync import MapSync
from systems.combat_system import CombatSystem


class EnemyTurnSystem:
    @staticmethod
    def run(state):
        for enemy in list(state.enemies):
            if not enemy.is_alive():
                CombatSystem.cleanup_dead_enemy(state, enemy)
                continue

            state.game_map.remove_object(enemy.x, enemy.y)
            result = enemy.ai_move(state.game_map, state.player)

            if isinstance(result, tuple) and result[0] == "attack":
                state.event_log.add(f"Вас атакует {enemy.name}!")

            if not enemy.is_alive():
                CombatSystem.cleanup_dead_enemy(state, enemy)
                continue

            MapSync.place_enemy(state, enemy)

            if not state.player.is_alive():
                state.event_log.add("Игрок погиб!")
                state.is_running = False
                return
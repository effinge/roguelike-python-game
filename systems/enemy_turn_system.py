from systems.map_sync import MapSync
from systems.combat_system import CombatSystem
from systems.enemy_ai import EnemyAI


class EnemyTurnSystem:
    @staticmethod
    def run(state):
        for enemy in list(state.enemies):
            if not enemy.is_alive():
                CombatSystem.cleanup_dead_enemy(state, enemy)
                continue

            old_x, old_y = enemy.x, enemy.y

            MapSync.remove_enemy(state, enemy)

            result = EnemyAI.take_turn(enemy, state)

            if result[0] == "attack":
                damage = result[1]
                state.event_log.add(f"{enemy.name} атакует вас и наносит {damage} урона!")
                if not state.player.is_alive():
                    state.event_log.add("Игрок погиб!")
                    state.is_running = False
                    return

            elif result[0] == "move":
                mode = result[3]
                if mode == "chase":
                    state.event_log.add(f"{enemy.name} заметил вас и преследует!")
                elif mode == "search":
                    state.event_log.add(f"{enemy.name} ищет вас...")

            elif result[0] == "dead":
                CombatSystem.cleanup_dead_enemy(state, enemy)
                continue

            MapSync.place_enemy(state, enemy)
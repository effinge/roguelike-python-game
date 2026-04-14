from systems.map_sync import MapSync

class CombatSystem:
    @staticmethod
    def get_enemy_at(state, x, y):
        for enemy in state.enemies:
            if enemy.x == x and enemy.y == y:
                return enemy
        return None
    
    @staticmethod
    def cleanup_dead_enemy(state, enemy):
        state.event_log.add(f"{enemy.name} погибает!")
        MapSync.remove_enemy(state, enemy)
        state.enemies.remove(enemy)
    
    @staticmethod
    def player_attack(state, target):
        damage = state.player.attack(target)
        state.event_log.add(f"Вы атакуете {target.name} и наносите {damage} урона!")
        if target.is_dead():
            CombatSystem.cleanup_dead_enemy(state, target)
    
    @staticmethod
    def enemy_attack(state, enemy):
        damage = enemy.attack(state.player)
        state.event_log.add(f"{enemy.name} атакует вас и наносит {damage} урона!")
        if not state.player.is_alive():
            state.event_log.add("Вы погибли!")
            state.is_running = False
class MapSync:
    @staticmethod
    def restore_cell(state, x, y):
        if (x, y) in state.items_map:
            item = state.items_map[(x, y)]
            symbol = getattr(item, "symbol", None) or "I"
            state.game_map.place_object(x, y, symbol)
        else:
            state.game_map.remove_object(x, y)
    
    @staticmethod
    def move_player(state, old_x, old_y):
        MapSync.restore_cell(state, old_x, old_y)
        state.game_map.place_object(state.player.x, state.player.y, state.player.symbol)

    @staticmethod
    def remove_enemy(state, enemy):
        MapSync.restore_cell(state, enemy.x, enemy.y)

    @staticmethod
    def place_enemy(state, enemy):
        state.game_map.place_object(enemy.x, enemy.y, enemy.symbol)
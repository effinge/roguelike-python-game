class VisibilitySystem:
    @staticmethod
    def update(state):
        state.visible_tiles.clear()
        
        px = state.player.x
        py = state.player.y
        r = state.vision_radius
        
        for x in range(state.game_map.width):
            for y in range(state.game_map.height):
                dx = x - px
                dy = y - py
                
                if dx * dx + dy * dy <= r * r:
                    state.visible_tiles.add((x, y))
                    state.explored_tiles.add((x, y))
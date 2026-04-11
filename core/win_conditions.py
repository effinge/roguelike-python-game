class WinConditions:
    def __init__(self, game):
        self.game = game

    def check_win(self):
        if not self.game.player:
            return False

        x, y = self.game.player.x, self.game.player.y
        if 0 <= x < self.game.game_map.width and 0 <= y < self.game.game_map.height:
            return self.game.game_map.get_cell(x, y) == '>'
        return False
class WinConditions:
    def __init__(self, game):
        self.game = game

    def check_win(self):
        if not self.game.player:
            return False

        x, y = self.game.player.x, self.game.player.y
        if 0 <= x < self.game.game_map.width and 0 <= y < self.game.game_map.height:
            obj = self.game.game_map.objects[x][y]
            
            if obj == '>':
                return True
            
            return self.game.game_map.get_cell(x, y) == '>'
        return False

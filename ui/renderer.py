class Renderer:
    def clear_screen(self):
        print("\n" * 40)
    
    def draw_map(self, game):
        for y in range(game.game_map.height):
            row = ""
            
            for x in range(game.game_map.width):
                tile_symbol = game.game_map.tiles[x][y]
                object_symbol = game.game_map.objects[x][y]

                if object_symbol is not None:
                    row += object_symbol
                else:
                    row += tile_symbol
                    
            print(row)
    
    def draw_status(self, game):
        print()
        print(f"Здоровье: {game.player.hp}")
        print(f"Урон: {game.player.damage}")
        print(f"Координаты: ({game.player.x}, {game.player.y})")
        
    def draw_help(self):
        print()
        print("Управление:")
        print("w - вверх")
        print("s - вниз")
        print("a - влево")
        print("d - вправо")
        print("q - выход из игры")
    
    def draw(self, game):
        self.clear_screen()
        self.draw_map(game)
        self.draw_status(game)
        self.draw_help()
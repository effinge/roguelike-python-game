class Renderer:
    def clear_screen(self):
        print("\n" * 30)
    
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
        enemies_count = sum(
            column.count("g") + column.count("t")
            for column in game.game_map.objects
        )

        print()
        print(
            f"Здоровье: {game.player.hp} | "
            f"Урон: {game.player.damage} | "
            f"Координаты: ({game.player.x}, {game.player.y}) | "
            f"Число врагов: {enemies_count}"
        )

    def draw_help(self):
        print()
        print("Управление: w - вверх | s - вниз | a - влево | d - вправо | f - атака | q - выход")

    def draw_event_log(self, game):
        print()
        print("Event log:")

        messages = list(reversed(game.event_log.get_messages()))
        visible_messages = messages[:3]

        for event in visible_messages:
            print(f"- {event}")

        for _ in range(3 - len(visible_messages)):
            print()


    def draw_help(self):
        print()
        print("Управление:")
        print("w - вверх")
        print("s - вниз")
        print("a - влево")
        print("d - вправо")
        print("q - выход из игры")
        print("f - атака")
    
    def draw(self, game):
        self.clear_screen()
        self.draw_map(game)
        self.draw_status(game)
        self.draw_event_log(game)
        self.draw_help()

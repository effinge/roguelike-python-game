class Renderer:
    def clear_screen(self):
        print("\n" * 30)

    def get_map_lines(self, game):
        lines = []

        for y in range(game.game_map.height):
            row = ""

            for x in range(game.game_map.width):
                tile_symbol = game.game_map.tiles[x][y]
                object_symbol = game.game_map.objects[x][y]
                row += object_symbol if object_symbol is not None else tile_symbol

            lines.append(row)

        return lines

    def get_sidebar_lines(self, game):
        enemies_count = sum(
            column.count("g") + column.count("t")
            for column in game.game_map.objects
        )

        inventory_items = game.inventory.get_items()
        inventory_text = ", ".join(inventory_items) if inventory_items else "пуст"

        messages = list(reversed(game.event_log.get_messages()))
        visible_messages = messages[:3]

        sidebar_lines = [
            f"Здоровье: {game.player.hp}",
            f"Урон: {game.player.damage}",
            f"Координаты: ({game.player.x}, {game.player.y})",
            f"Число врагов: {enemies_count}",
            f"Инвентарь: {inventory_text}",
            "",
            "Event log:",
        ]

        for event in visible_messages:
            sidebar_lines.append(f"- {event}")

        for _ in range(3 - len(visible_messages)):
            sidebar_lines.append("")

        sidebar_lines.extend(
            [
                "",
                "Управление:",
                "w - вверх",
                "s - вниз",
                "a - влево",
                "d - вправо",
                "f - атака",
                "q - выход",
            ]
        )

        return sidebar_lines

    def draw(self, game):
        self.clear_screen()

        map_lines = self.get_map_lines(game)
        sidebar_lines = self.get_sidebar_lines(game)
        map_width = game.game_map.width
        total_lines = max(len(map_lines), len(sidebar_lines))

        for i in range(total_lines):
            map_line = map_lines[i] if i < len(map_lines) else ""
            sidebar_line = sidebar_lines[i] if i < len(sidebar_lines) else ""
            print(f"{map_line.ljust(map_width + 4)}{sidebar_line}")

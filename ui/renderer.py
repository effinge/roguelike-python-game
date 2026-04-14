import shutil


class Renderer:
    SIDEBAR_WIDTH = 30
    SIDEBAR_GAP = 4
    LOG_LINES = 3
    INVENTORY_LINES = 3

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

    def fit_line(self, text):
        text = str(text)
        if len(text) <= self.SIDEBAR_WIDTH:
            return text
        return text[: self.SIDEBAR_WIDTH - 3] + "..."

    def build_bar(self, label, value, max_value, width=20):
        safe_max = max(1, max_value)
        filled = int((value / safe_max) * width)
        filled = max(0, min(width, filled))
        bar = "|" * filled + "." * (width - filled)
        return f"{label}: {value} [{bar}]"

    def get_status_lines(self, game):
        enemies_count = sum(
            column.count("g") + column.count("t")
            for column in game.game_map.objects
        )

        return [
            "status bar".center(self.SIDEBAR_WIDTH),
            "",
            self.fit_line(self.build_bar("HP", game.player.hp, game.player.max_hp)),
            self.fit_line(f"Damage: {game.player.damage}"),
            self.fit_line(f"Enemies: {enemies_count}"),
        ]

    def get_event_log_lines(self, game):
        messages = list(reversed(game.event_log.get_messages()))
        lines = [
            "event log:".center(self.SIDEBAR_WIDTH),
            "",
        ]

        for event in messages[: self.LOG_LINES]:
            lines.append(self.fit_line(f"- {event}"))

        for _ in range(self.LOG_LINES - min(len(messages), self.LOG_LINES)):
            lines.append("-")

        return lines

    def get_inventory_lines(self, game):
        items = game.inventory.get_items()
        lines = [
            "inventory:".center(self.SIDEBAR_WIDTH),
            "",
        ]

        for index, item in enumerate(items[: self.INVENTORY_LINES], start=1):
            lines.append(self.fit_line(f"{index}. {item}"))

        for index in range(len(items[: self.INVENTORY_LINES]) + 1, self.INVENTORY_LINES + 1):
            lines.append(f"{index}. -")

        return lines

    def get_sidebar_lines(self, game):
        return (
            self.get_status_lines(game)
            + [""]
            + self.get_event_log_lines(game)
            + [""]
            + self.get_inventory_lines(game)
            + [""]
            + [
                "controls:".center(self.SIDEBAR_WIDTH),
                "",
                self.fit_line("w/a/s/d - move"),
                self.fit_line("f - attack"),
                self.fit_line("q - quit"),
            ]
        )

    def draw(self, game):
        self.clear_screen()

        map_lines = self.get_map_lines(game)
        sidebar_lines = self.get_sidebar_lines(game)
        status_lines = self.get_status_lines(game)
        event_log_lines = self.get_event_log_lines(game)
        map_width = game.game_map.width
        content_width = map_width + self.SIDEBAR_GAP + self.SIDEBAR_WIDTH
        terminal_width = shutil.get_terminal_size((120, 30)).columns
        left_padding = " " * max(0, (terminal_width - content_width) // 2)
        map_center_anchor = len(status_lines) + 1 + len(event_log_lines)
        map_top_padding = max(0, map_center_anchor - len(map_lines) // 2)
        total_lines = max(len(sidebar_lines), map_top_padding + len(map_lines))

        for i in range(total_lines):
            map_index = i - map_top_padding
            map_line = map_lines[map_index] if 0 <= map_index < len(map_lines) else ""
            sidebar_line = sidebar_lines[i] if i < len(sidebar_lines) else ""
            print(f"{left_padding}{map_line.ljust(map_width + self.SIDEBAR_GAP)}{sidebar_line}")
        print(f"{left_padding}Coords: ({game.player.x}, {game.player.y})")
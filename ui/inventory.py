class Inventory: 
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

    def remove(self, item):
        if item in self.items:
            self.items.remove(item)
            return True
        return False

    def get_items(self):
        return self.items


import shutil


class InventoryUI:
    
    @staticmethod
    def clear_screen():
        print('\n' * 30)

    @staticmethod
    def open(game):
        inv = game.inventory
        while True:
            InventoryUI.clear_screen()
            items = inv.get_items()

            term = shutil.get_terminal_size((120, 30))
            term_w, term_h = term.columns, term.lines
            content_lines = []
            content_lines.append('Inventory')
            content_lines.append(f'Всего слотов {len(items)}/20')
            content_lines.append('')
            for idx in range(10):
                if idx < len(items):
                    content_lines.append(f'{idx+1}. {items[idx]}')
                else:
                    content_lines.append(f'{idx+1}. -')
            content_lines.append('')
            content_lines.append('Выберите предмет (номер) или нажмите q чтобы выйти')

            content_width = max(len(line) for line in content_lines) + 4
            left_padding = ' ' * max(0, (term_w - content_width) // 2)
            top_padding_lines = max(0, (term_h - len(content_lines)) // 3)

            print('\n' * top_padding_lines)
            for line in content_lines:
                print(f"{left_padding}{line}")

            choice = input(f"{left_padding}> ").strip().lower()
            if choice == 'q':
                break
            if not choice.isdigit():
                continue
            sel = int(choice) - 1
            if sel < 0 or sel >= len(items):
                continue
            item = items[sel]

            while True:
                InventoryUI.clear_screen()
                detail_lines = []
                detail_lines.append(f'Предмет: {item.name}')
                detail_lines.append('')
                detail_lines.extend(item.describe().split('\n'))
                detail_lines.append('')
                detail_lines.append('Доступные действия:')
                detail_lines.append('u - Use (если применимо)')
                detail_lines.append('e - Equip (если оружие)')
                detail_lines.append('d - Drop')
                detail_lines.append('b - Back')

                term = shutil.get_terminal_size((120, 30))
                term_w, term_h = term.columns, term.lines
                content_w = max(len(line) for line in detail_lines) + 4
                left_padding = ' ' * max(0, (term_w - content_w) // 2)
                top_pad = max(0, (term_h - len(detail_lines)) // 3)
                print('\n' * top_pad)
                for ln in detail_lines:
                    print(f"{left_padding}{ln}")
                act = input(f"{left_padding}> ").strip().lower()
                if act == 'b':
                    break
                if act == 'd':
                    inv.remove(item)
                    px, py = game.player.x, game.player.y
                    game.items_map[(px, py)] = item
                    game.game_map.place_object(px, py, item.symbol if getattr(item, 'symbol', None) else 'I')
                    game.event_log.add(f'Вы выбросили {item.name}')
                    break
                if act == 'u':
                    msg = item.apply_to(game.player)
                    if msg:
                        game.event_log.add(msg)
                        inv.remove(item)
                    else:
                        game.event_log.add('Нельзя применить этот предмет')
                    break
                if act == 'e' and hasattr(item, 'equip'):
                    msg = item.equip(game.player)
                    if msg:
                        game.event_log.add(msg)
                    break

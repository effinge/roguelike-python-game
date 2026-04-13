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


class InventoryUI:
    """Простейший полноэкранный консольный UI для инвентаря.

    Использование: InventoryUI.open(game) — остановит основной цикл и
    позволит игроку просматривать предметы и применять/экипировать/выбрасывать их.
    """

    @staticmethod
    def clear_screen():
        print('\n' * 30)

    @staticmethod
    def open(game):
        inv = game.inventory
        while True:
            InventoryUI.clear_screen()
            items = inv.get_items()
            print('Inventory'.center(40))
            print(f'Всего слотов {len(items)}/20')
            print()
            for idx in range(10):
                if idx < len(items):
                    print(f'{idx+1}. {items[idx]}')
                else:
                    print(f'{idx+1}. -')

            print()
            print('Выберите предмет (номер) или нажмите q чтобы выйти')
            choice = input('> ').strip().lower()
            if choice == 'q':
                break
            if not choice.isdigit():
                continue
            sel = int(choice) - 1
            if sel < 0 or sel >= len(items):
                continue
            item = items[sel]

            # show details and actions
            while True:
                InventoryUI.clear_screen()
                print(f'Предмет: {item.name}')
                print()
                print(item.describe())
                print()
                actions = []
                print('Доступные действия:')
                print('u - Use (если применимо)')
                print('e - Equip (если оружие)')
                print('d - Drop')
                print('b - Back')
                act = input('> ').strip().lower()
                if act == 'b':
                    break
                if act == 'd':
                    inv.remove(item)
                    # place item on map at player's position
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
            # after action, return to inventory list
        # inventory closed

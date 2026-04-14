import random
from items.item import ItemFactory


class ItemSystem:
    @staticmethod
    def symbol_to_item(symbol):
        all_items = ItemFactory.load_all()
        for item in all_items.values():
            if getattr(item, "symbol", None) == symbol:
                return item
        return None

    @staticmethod
    def clone_item(item):
        if item is None:
            return None

        cls_name = item.__class__.__name__

        if cls_name == "Weapon":
            return type(item)(
                getattr(item, "id", None),
                getattr(item, "name", None),
                getattr(item, "damage", None),
                getattr(item, "symbol", None),
            )

        if cls_name == "Potion":
            return type(item)(
                getattr(item, "id", None),
                getattr(item, "name", None),
                getattr(item, "properties", None),
                getattr(item, "symbol", None),
            )

        try:
            return type(item)(
                getattr(item, "id", None),
                getattr(item, "name", None),
                getattr(item, "symbol", None),
                getattr(item, "item_type", None),
                getattr(item, "properties", None),
            )
        except Exception:
            return item

    @staticmethod
    def ensure_item_on_position(state, x, y, obj_symbol):
        if (x, y) in state.items_map:
            return

        item_from_symbol = ItemSystem.symbol_to_item(obj_symbol)
        chosen = ItemSystem.clone_item(item_from_symbol)

        if chosen is None:
            all_items = list(ItemFactory.load_all().values())
            if all_items:
                chosen = ItemSystem.clone_item(random.choice(all_items))

        if chosen is not None:
            state.items_map[(x, y)] = chosen

    @staticmethod
    def pickup_item(state):
        pos = (state.player.x, state.player.y)
        item = state.items_map.get(pos)

        if item is None:
            state.event_log.add("Здесь нет предмета")
            return False

        added = state.inventory.add(item)
        if not added:
            state.event_log.add("Инвентарь заполнен")
            return False

        state.game_map.remove_object(pos[0], pos[1])
        del state.items_map[pos]
        state.event_log.add(f"Вы подобрали {item.name}")
        return True
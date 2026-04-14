import json
from pathlib import Path
from typing import Dict, Any


class Item:
    def __init__(self, id: str, name: str, symbol: str | None = None, item_type: str | None = None, properties: Dict[str, Any] | None = None):
        self.id = id
        self.name = name
        self.symbol = symbol
        self.item_type = item_type
        self.properties = properties or {}

    def __str__(self) -> str:
        return self.name

    def describe(self) -> str:
        lines = [self.name]
        for k, v in self.properties.items():
            lines.append(f"{k}: {v}")
        return "\n".join(lines)

    def apply_to(self, entity) -> str | None:
        return None


class Weapon(Item):
    def __init__(self, id, name, damage, symbol=None):
        super().__init__(id=id, name=name, symbol=symbol, item_type="weapon", properties={"damage": damage})
        self.damage = damage

    def __str__(self) -> str:
        return f"{self.name} (atk {self.damage})"

    def equip(self, entity) -> str:
        if hasattr(entity, 'damage'):
            entity.damage += self.damage
            return f"{entity.__class__.__name__} экипировал {self.name}, +{self.damage} урона"
        return f"{self.name} нельзя экипировать"


class Potion(Item):
    def __init__(self, id: str, name: str, properties: Dict[str, Any] | None = None, symbol: str | None = None):
        super().__init__(id=id, name=name, symbol=symbol, item_type='potion', properties=properties)

    def __str__(self) -> str:
        if 'healing_amount' in self.properties:
            return f"{self.name} (+{self.properties['healing_amount']} HP)"
        if 'attack_increase' in self.properties:
            return f"{self.name} (+{self.properties['attack_increase']} ATK)"
        return self.name

    def apply_to(self, entity) -> str | None:
        if 'healing_amount' in self.properties and hasattr(entity, 'hp'):
            amount = int(self.properties['healing_amount'])
            max_hp = getattr(entity, 'max_hp', None)
            if max_hp is not None:
                entity.hp = min(max_hp, entity.hp + amount)
            else:
                entity.hp = entity.hp + amount
            return f"{entity.__class__.__name__} восстановил {amount} HP"
        if 'attack_increase' in self.properties and hasattr(entity, 'damage'):
            inc = int(self.properties['attack_increase'])
            entity.damage += inc
            return f"{entity.__class__.__name__} получил +{inc} к урону"
        return None


class ItemFactory:
    @staticmethod
    def _load_json(path: str) -> Dict[str, Any]:
        p = Path(path)
        if not p.exists():
            return {}
        try:
            return json.loads(p.read_text(encoding='utf-8'))
        except Exception:
            return {}

    @classmethod
    def load_weapons(cls, path: str = "items/weapon_type.json") -> Dict[str, Item]:
        data = cls._load_json(path)
        items: Dict[str, Item] = {}
        for key, defn in data.items():
            name = defn.get('name', key)
            damage = defn.get('damage', 0)
            symbol = defn.get('symbol')
            items[key] = Weapon(id=key, name=name, damage=damage, symbol=symbol)
        return items

    @classmethod
    def load_potions(cls, path: str = "items/posion_type.json") -> Dict[str, Item]:
        data = cls._load_json(path)
        items: Dict[str, Item] = {}
        for category, group in data.items():
            if isinstance(group, dict):
                for key, defn in group.items():
                    name = defn.get('name', key)
                    symbol = defn.get('symbol')
                    props = {k: v for k, v in defn.items() if k not in ('name', 'symbol')}
                    items[key] = Potion(id=key, name=name, symbol=symbol, properties=props)
        return items

    @classmethod
    def load_all(cls, folder: str = "items") -> Dict[str, Item]:
        items: Dict[str, Item] = {}
        items.update(cls.load_weapons(str(Path(folder) / "weapon_type.json")))
        items.update(cls.load_potions(str(Path(folder) / "posion_type.json")))
        return items

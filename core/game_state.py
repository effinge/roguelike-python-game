from dataclasses import dataclass, field
from typing import Dict, List, Any


@dataclass
class GameState:
    config: dict
    game_map: Any
    player: Any
    enemies: List[Any]
    event_log: Any
    inventory: Any
    items_map: Dict[tuple, Any]
    renderer: Any
    win_conditions: Any

    is_running: bool = True
    tick: float = 0.5
    visible_tiles: set = field(default_factory=set)
    explored_tiles: set = field(default_factory=set)
    vision_radius: int = 6
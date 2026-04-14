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
    is_running: bool = True
    win_conditions: Any
    renderer: Any
    tick: float = 0.5
    
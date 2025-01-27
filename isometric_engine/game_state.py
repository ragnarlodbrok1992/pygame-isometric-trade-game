from dataclasses import dataclass
from typing import Tuple

# Clicked tiles
# TODO: infinite chunks??? if so, there need to be another way to represent "nothing" in terms of selection
# GAME_STATE_CLICKED_TILE = (-1, -1)  # -1, -1 means nothing is clicked

# HANDLE_GAME_STATE: GameState | None = None

@dataclass
class GameState:
    clicked_tile: Tuple[int, int] = (-1, -1)


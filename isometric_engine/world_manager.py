from __future__ import annotations

import pygame

import numpy as np
from numpy.typing import NDArray

from .grid import *
from .grid_config import *
from .render_info import *
from .game_state import *


class WorldManager:
    def __init__(self) -> None:
        self.grid_chunk: NDArray[np.int_] = np.full(
            (GRID_CHUNK_ROWS, GRID_CHUNK_COLS),
            int(GridType.WATER),
            dtype=np.integer)

    def resize_grid_chunk(self, rows: int, cols: int) -> None:
        print("Resizing grid chunk!")
        print(f"{self.grid_chunk.shape}")
        self.grid_chunk = np.resize(self.grid_chunk, (rows, cols))
        print(f"{self.grid_chunk.shape}")
        

    def get_tile_from_grid(self, render_info: RenderInfo, game_state: GameState, click_position: pygame.math.Vector2) -> None:
        # 1. Project clicked position to iso projection.
        # 2. Calculate grid bound box in iso projection.
        # 3. Check if click is inside grid bounding box.
        click_pos_v2 = click_position - render_info.cam_offset
        normal_proj_pos_v2 = cast_points_to_normal_v2([click_pos_v2])[0]
        game_state.clicked_tile = normal_proj_pos_v2 // GRID_TILE_SIZE

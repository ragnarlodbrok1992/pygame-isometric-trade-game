import pygame
import numpy as np
from numpy.typing import NDArray
from typing import Tuple

from .isometric_perspective import *
from .grid_config import *
from .render_info import *

GRID_CHUNK = np.full((GRID_CHUNK_ROWS, GRID_CHUNK_COLS), int(GridType.WATER), dtype=np.integer)

def draw_grid_chunk(screen: pygame.surface.Surface, render_info: RenderInfo, grid: NDArray[np.int_]) -> None:
    # Assumptions: origin for now (0, 0)
    rows, cols = grid.shape
    for row in range(rows):
        for col in range(cols):
            color = GRID_COLORS[grid[row, col]]

            top_left = tuple(GRID_TILE_SIZE * np.array((col, row)))
            top_right = tuple(GRID_TILE_SIZE * np.array((col + 1, row)))
            bottom_right = tuple(GRID_TILE_SIZE * np.array((col + 1, row + 1)))
            bottom_left = tuple(GRID_TILE_SIZE * np.array((col, row + 1)))

            points = cast_points_to_isometric([
                top_left,
                top_right,
                bottom_right,
                bottom_left,
                ])

            offset_points(points, render_info)

            # Drawing diamond polygon
            pygame.draw.polygon(
                screen,
                color,
                points
            )

            # Drawing outline of unselected polygon
            pygame.draw.polygon(
                screen,
                GRID_OUTLINE_COLOR[int(GridType.WATER)],
                points,
                width=1
            )
            

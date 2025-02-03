import pygame
import numpy as np
from numpy.typing import NDArray
from typing import Tuple

from .isometric_perspective import *
from .grid_config import *
from .render_info import *
from .game_state import *

GRID_CHUNK: NDArray[np.int_] = np.full((GRID_CHUNK_ROWS, GRID_CHUNK_COLS), int(GridType.WATER), dtype=np.integer)

def resize_grid_chunk(chunk: NDArray[np.int_], new_size_x: int, new_size_y: int) -> NDArray[np.int_]:
    return np.resize(chunk, (new_size_x, new_size_y))

def get_tile_from_grid(grid: NDArray[np.int_], render_info: RenderInfo, game_state: GameState, click_position: pygame.math.Vector2) -> None:
    # 1. Project clicked position to iso projection.
    # 2. Calculate grid bound box in iso projection.
    # 3. Check if click is inside grid bounding box.
    # click_pos_v2 = pygame.math.Vector2(click_position[0] - render_info.cam_offset[0], click_position[1] - render_info.cam_offset[1])
    click_pos_v2 = click_position - render_info.cam_offset
    normal_proj_pos_v2 = cast_points_to_normal_v2([click_pos_v2])[0]
    game_state.clicked_tile = normal_proj_pos_v2 // GRID_TILE_SIZE


def draw_grid_chunk(screen: pygame.surface.Surface, render_info: RenderInfo, game_state: GameState, grid: NDArray[np.int_]) -> None:
    # Assumptions: origin for now (0, 0)
    rows, cols = grid.shape
    x_id, y_id = game_state.clicked_tile
    for row in range(rows):
        for col in range(cols):
            if x_id == col and y_id == row:
                # print("We have something selected!")
                color = GRID_COLORS[255]
            else:
                color = GRID_COLORS[grid[row, col]]

            top_left = pygame.math.Vector2(
                    tuple(GRID_TILE_SIZE * np.array((col, row))))
            top_right = pygame.math.Vector2(
                    tuple(GRID_TILE_SIZE * np.array((col + 1, row))))
            bottom_right = pygame.math.Vector2(
                    tuple(GRID_TILE_SIZE * np.array((col + 1, row + 1))))
            bottom_left = pygame.math.Vector2(
                    tuple(GRID_TILE_SIZE * np.array((col, row + 1))))

            points = cast_points_to_isometric_v2([
                top_left,
                top_right,
                bottom_right,
                bottom_left,
                ])

            offset_points_v2(points, render_info)

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

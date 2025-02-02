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

def get_tile_from_grid(grid: NDArray[np.int_], render_info: RenderInfo, game_state: GameState, click_position: Tuple[int, int]) -> None:
    # 1. Project clicked position to iso projection.
    # 2. Calculate grid bound box in iso projection.
    # 3. Check if click is inside grid bounding box.

    rows, cols = grid.shape
    bounding_box_offsetted = [
       (render_info.cam_offset_x, render_info.cam_offset_y),
       ((rows * GRID_TILE_SIZE) + render_info.cam_offset_x, render_info.cam_offset_y),
       ((rows * GRID_TILE_SIZE) + render_info.cam_offset_x, (cols * GRID_TILE_SIZE) + render_info.cam_offset_y),
       (render_info.cam_offset_x, (cols * GRID_TILE_SIZE) + render_info.cam_offset_y),
           ]

    normal_projection_mouse_pos = [(
            click_position[0] - render_info.cam_offset_x,
            click_position[1] - render_info.cam_offset_y)]
    new_normal_projection_pos = cast_points_to_normal(normal_projection_mouse_pos)[0]

    # GAME_STATE_CLICKED_TILE = (new_normal_projection_pos[0] // GRID_TILE_SIZE, new_normal_projection_pos[1] // GRID_TILE_SIZE)
    game_state.clicked_tile = (new_normal_projection_pos[0] // GRID_TILE_SIZE, new_normal_projection_pos[1] // GRID_TILE_SIZE)
    # FIXME: I have no idea what is actually going on
    # print("Changing state!")
    # print(GAME_STATE_CLICKED_TILE)
    # print(game_state)

def draw_grid_chunk(screen: pygame.surface.Surface, render_info: RenderInfo, game_state: GameState, grid: NDArray[np.int_]) -> None:
    # Assumptions: origin for now (0, 0)
    rows, cols = grid.shape
    # x_id, y_id = GAME_STATE_CLICKED_TILE
    x_id, y_id = game_state.clicked_tile
    # FIXME: This global state is still not working
    # print(hex(id(GAME_STATE_CLICKED_TILE)))
    # print(x_id, y_id)
    for row in range(rows):
        for col in range(cols):
            if x_id == col and y_id == row:
                # print("We have something selected!")
                color = GRID_COLORS[255]
            else:
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
            

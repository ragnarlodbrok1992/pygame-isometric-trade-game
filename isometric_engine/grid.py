import pygame
import numpy as np
from numpy.typing import NDArray
from typing import Tuple

from .isometric_perspective import *
from .grid_config import *
from .render_info import *

GRID_CHUNK = np.full((GRID_CHUNK_ROWS, GRID_CHUNK_COLS), int(GridType.WATER), dtype=np.integer)

def get_tile_from_grid(grid: NDArray[np.int_], render_info: RenderInfo, click_position: Tuple[int, int]) -> Tuple[int, int]:
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
    # print(normal_projection_mouse_pos)
    print(cast_points_to_normal(normal_projection_mouse_pos))

    # bounding_box_offsetted = [
    #     (0, 0),
    #     (rows * GRID_TILE_SIZE, cols * GRID_TILE_SIZE),
    #     (rows * GRID_TILE_SIZE, cols * GRID_TILE_SIZE),
    #     (0, cols * GRID_TILE_SIZE),
    #         ]

    # bounding_box_offsetted = cast_points_to_isometric(bounding_box_offsetted)  # FIXME: change it as reference, don't build new object?
    # offset_points(bounding_box_offsetted, render_info)

    return bounding_box_offsetted

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
            

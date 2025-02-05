import pygame
import numpy as np
from numpy.typing import NDArray
from typing import Tuple

from .isometric_perspective import *
from .grid_config import *
from .render_info import *
from .game_state import *
from .world_manager import *


def draw_grid_chunk(world_manager: WorldManager, screen: pygame.surface.Surface, render_info: RenderInfo, game_state: GameState) -> None:
    # TODO: fix this function - adding WorldManager
    # Assumptions: origin for now (0, 0)
    rows, cols = world_manager.grid_chunk.shape
    x_id, y_id = game_state.clicked_tile
    for row in range(rows):
        for col in range(cols):
            if x_id == col and y_id == row:
                # print("We have something selected!")
                color = GRID_COLORS[255]
            else:
                color = GRID_COLORS[world_manager.grid_chunk[row, col]]

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

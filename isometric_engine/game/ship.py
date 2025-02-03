from __future__ import annotations

import pygame

from pathlib import Path
from typing import List, Tuple
from enum import IntEnum

from ..render_info import *
from ..isometric_perspective import *
from ..grid_config import *
from ..grid import *
from ..iso_math import *

# Directions - this somehow should make sens, I don't know how to give directions with three pieces
# 0  - ship1  - NW
# 1  - ship2  - WNW
# 2  - ship3  - W
# 3  - ship4  - WSW
# 4  - ship5  - SW
# 5  - ship6  - SSW
# 6  - ship7  - S
# 7  - ship8  - SSE
# 8  - ship9  - SE
# 9  - ship10 - ESE
# 10 - ship11 - E
# 11 - ship12 - ENE
# 12 - ship13 - NE
# 13 - ship14 - NNE
# 14 - ship15 - N
# 15 - ship16 - NNW

class Direction(IntEnum):
    NW  = 0
    WNW = 1
    W   = 2
    WSW = 3
    SW  = 4
    SSW = 5
    S   = 6
    SSE = 7
    SE  = 8
    ESE = 9
    E   = 10
    ENE = 11
    NE  = 12
    NNE = 13
    N   = 14
    NNW = 15

    def __add__(self, other: int) -> Direction:
        return Direction((self.value + other) % 16)

    def __sub__(self, other: int) -> Direction:
        return Direction((self.value - other) % 16)

class Ship:
    def __init__(self) -> None:
        self.assets_names_list = [
            'ship1.png',
            'ship2.png',
            'ship3.png',
            'ship4.png',
            'ship5.png',
            'ship6.png',
            'ship7.png',
            'ship8.png',
            'ship9.png',
            'ship10.png',
            'ship11.png',
            'ship12.png',
            'ship13.png',
            'ship14.png',
            'ship15.png',
            'ship16.png',
                ]
        self.sprites: List[pygame.Surface] = []
        self.position = pygame.math.Vector2(0, 0)  # In chunk grid positions
        self.start_position = pygame.math.Vector2(0, 0)
        self.position_to_go = pygame.math.Vector2(0, 0)
        self.direction: Direction = Direction.S
        self.rotating_left: bool = False
        self.rotating_right: bool = False
        self.is_sailing: bool = False
        self.save_start_position: bool = True
        self.rotation_speed: float = 0.125
        self.sail_time: float = 1.0
        self.current_sail_time: float = 0.0

    def load_assets(self, assets_path: Path) -> None:
        # Check if assets are there
        for asset in self.assets_names_list:
            full_asset_path = f"{assets_path}\\{asset}"
            if Path(full_asset_path).exists():
                self.sprites.append(pygame.image.load(full_asset_path))

        # Check if assets are loaded correctly
        assert(len(self.sprites) == 16)

    def rotate_clockwise(self) -> None:
        self.rotating_right = True

    def rotate_counterclockwise(self) -> None:
        self.rotating_left = True

    def _calculate_rotation(self, dt: float) -> None:
        if self.rotating_left or self.rotating_right:
            self.rotation_speed -= dt
            if self.rotation_speed < 0.0:
                # Do the rotation
                if self.rotating_right:
                    self.direction -= 1
                    if not self.direction % 2 == 1:
                        self.rotating_right = False
                elif self.rotating_left:
                    self.direction += 1
                    if not self.direction % 2 == 1:
                        self.rotating_left = False
                self.rotation_speed = 0.250

    def try_to_go_forward(self) -> None:
        if self.is_sailing:
            return

        possible_position = pygame.math.Vector2(0, 0)
        match self.direction:
            case Direction.N:
                possible_position = self.position + (0, -1)
            case Direction.E:
                possible_position = self.position + (1, 0)
            case Direction.S:
                possible_position = self.position + (0, 1)
            case Direction.W:
                possible_position = self.position + (-1, 0)
            case Direction.NE:
                possible_position = self.position + (1, -1)
            case Direction.NW:
                possible_position = self.position + (-1, -1)
            case Direction.SE:
                possible_position = self.position + (1, 1)
            case Direction.SW:
                possible_position = self.position + (-1, 1)
            case _:
                # TODO: log this in console? Shouldn't happen, but player can press UP while ship is rotating
                pass

        if possible_position != pygame.math.Vector2(0, 0):
            x_ind, y_ind = GRID_CHUNK.shape
            if 0 <= possible_position.x < x_ind and 0 <= possible_position.y < y_ind:
                self.is_sailing = True
                self.position_to_go = possible_position

    def _sail(self, old_position: pygame.math.Vector2, new_position: pygame.math.Vector2, dt: float) -> None:
        self.save_start_position = False

        self.current_sail_time += dt
        sail_vector = new_position - old_position
        percent_there = self.current_sail_time / self.sail_time
        lerped_position = lerp_vec2(new_position, old_position, percent_there)
        self.position = lerped_position
        if self.current_sail_time > self.sail_time:
            self.is_sailing = False
            self.save_start_position = True
            self.current_sail_time = 0.0
            self.position = pygame.math.Vector2(
                    round(self.position.x),
                    round(self.position.y))

    def render_ship(self, screen: pygame.Surface, render_info: RenderInfo, dt: float) -> None:
        self._calculate_rotation(dt)

        if self.is_sailing:
            if self.save_start_position:
                self.start_position = self.position
            self._sail(self.position_to_go, self.start_position, dt)

        # Translate self.position to screen isometric perspective coordinates
        # Take grid_tile_size into account
        step: int = GRID_TILE_SIZE // 2
        sprite_width = self.sprites[self.direction].get_width()
        sprite_height = self.sprites[self.direction].get_height()
        sprite_width_half = sprite_width // 2
        sprite_height_half = sprite_height // 2 + (GRID_TILE_SIZE // 4)  # Making it a little bit of center since the sprite is
        sprite_offsetting = pygame.math.Vector2(sprite_width_half, sprite_height_half)

        screen_position = pygame.math.Vector2(((step) + (GRID_TILE_SIZE * self.position[0]), (step) + (GRID_TILE_SIZE * self.position[1])))

        position_casted = cast_points_to_isometric_v2([screen_position])
        offset_points_v2(position_casted, render_info)
        position = pygame.math.Vector2(position_casted[0])

        position = position - sprite_offsetting
        
        screen.blit(self.sprites[self.direction], position)

        if render_info.debug_render:
            # Debug - bounding rect
            rect = pygame.Rect(position, (sprite_width, sprite_height))
            # Debug - bounding rect cross for the center of the sprite
            pygame.draw.rect(screen, (255, 255, 255), rect, width=1)
            top_left = pygame.math.Vector2(position[0], position[1])
            top_right = pygame.math.Vector2(position[0] + sprite_width, position[1])
            bottom_left = pygame.math.Vector2(position[0], position[1] + sprite_height)
            bottom_right = pygame.math.Vector2(position[0] + sprite_width, position[1] + sprite_height)
            pygame.draw.line(screen, (255, 0, 255), top_left, bottom_right)
            pygame.draw.line(screen, (255, 0, 255), top_right, bottom_left)


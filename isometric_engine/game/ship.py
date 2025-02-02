import pygame
from pathlib import Path
from typing import List, Tuple

from ..render_info import *
from ..isometric_perspective import *
from ..grid_config import *

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
        self.position: Tuple[int, int] = (0, 0)  # In chunk grid positions
        self.direction: int = 6

    def load_assets(self, assets_path: Path) -> None:
        # Check if assets are there
        # print(assets_path)
        for asset in self.assets_names_list:
            full_asset_path = f"{assets_path}\\{asset}"
            # print(full_asset_path, Path(full_asset_path).exists())
            if Path(full_asset_path).exists():
                self.sprites.append(pygame.image.load(full_asset_path))

        # Check if assets are loaded correctly
        assert(len(self.sprites) == 16)

    def render_ship(self, screen: pygame.Surface, render_info: RenderInfo) -> None:
        # Translate self.position to screen isometric perspective coordinates
        # Take grid_tile_size into account
        step: int = GRID_TILE_SIZE // 2
        sprite_width = self.sprites[self.direction].get_width()
        sprite_height = self.sprites[self.direction].get_height()
        sprite_width_half = sprite_width // 2
        sprite_height_half = sprite_height // 2 + (GRID_TILE_SIZE // 4)  # Making it a little bit of center since the sprite is

        screen_position = (
                (step) + (GRID_TILE_SIZE * self.position[0]),
                (step) + (GRID_TILE_SIZE * self.position[1]),
                )

        position_casted = cast_points_to_isometric([screen_position])
        offset_points(position_casted, render_info)
        position: Tuple[int, int] = position_casted[0]
        position = (position[0] - sprite_width_half, position[1] - sprite_height_half)
        
        screen.blit(self.sprites[self.direction], position)

        if render_info.debug_render:
            # Debug - bounding rect
            rect = pygame.Rect(position, (sprite_width, sprite_height))
            # Debug - bounding rect cross for the center of the sprite
            pygame.draw.rect(screen, (255, 255, 255), rect, width=1)
            top_left = (position[0], position[1])
            top_right = (position[0] + sprite_width, position[1])
            bottom_left = (position[0], position[1] + sprite_height)
            bottom_right = (position[0] + sprite_width, position[1] + sprite_height)
            pygame.draw.line(screen, (255, 0, 255), top_left, bottom_right)
            pygame.draw.line(screen, (255, 0, 255), top_right, bottom_left)


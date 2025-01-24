from enum import Enum

GRID_TILE_WIDTH = 64
GRID_TILE_HEIGHT = 32

# Some different grid types - enum
class GridType(Enum):
    VOID = 0  # Testing purposes
    WATER = 1
    LAND = 2

GRID_COLORS = {
    0: (0, 0, 0),  # VOID is black for now
    1: (35, 79, 130),  # WATER color
    2: (47, 89, 39),  # LAND color
        }

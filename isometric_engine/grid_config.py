from enum import IntEnum

GRID_TILE_SIZE = 32

# This isometric grid assumes that: 
# North --> TopRight
# South --> BottomLeft
# West --> TopLeft
# East --> BottomRight

GRID_CHUNK_COLS = 10  # COLS go South --> North
GRID_CHUNK_ROWS = 10  # ROWS go West --> East

# Some different grid types - enum
class GridType(IntEnum):
    VOID = 0  # Testing purposes
    WATER = 1
    LAND = 2

GRID_OUTLINE_COLOR = (138, 186, 48)

GRID_COLORS = {
    0: (0, 0, 0),  # VOID is black for now
    1: (35, 79, 130),  # WATER color
    2: (47, 89, 39),  # LAND color
        }

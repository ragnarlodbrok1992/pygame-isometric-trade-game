import pygame

from typing import List

CNTRL_ENGINE_RUNNING = True

# ----> X
# |
# |
# v Y

CNTRL_2D_CAM_OFFSET_X = 0
CNTRL_2D_CAM_OFFSET_Y = 0

MOUSE_BUTTONS = (False, False, False)
MOUSE_SELECTION_UI = False
MOUSE_SELECTION_GAME_AREA = False
MOUSE_DRAGGING = False
MOUSE_DRAGGING_FRAME_DISTANCE = pygame.math.Vector2(0, 0)
MOUSE_DRAGGING_HISTORY: List[pygame.math.Vector2] = [pygame.math.Vector2(-1, -1), pygame.math.Vector2(-1, -1)]  # Keeping current and last frame mouse positions to calculate drag vector
MOUSE_FRAME_SWITCH = 0  # Keeps truck of buffer index where we put stuff - we calculate it using % 2


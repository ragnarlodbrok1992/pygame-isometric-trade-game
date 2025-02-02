from .control import *

from dataclasses import dataclass

@dataclass
class RenderInfo:
    cam_offset_x: int = CNTRL_2D_CAM_OFFSET_X
    cam_offset_y: int = CNTRL_2D_CAM_OFFSET_Y

    debug_render: bool = False

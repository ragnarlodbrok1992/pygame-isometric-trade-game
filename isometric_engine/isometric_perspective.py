import pygame

import numpy as np

from typing import List, Tuple
from numpy.typing import NDArray
from .render_info import RenderInfo

PROJECTION_MATRIX: NDArray[np.float32] = np.ndarray((2, 2), dtype=np.float32)
REVERSE_PROJECTION_MATRIX: NDArray[np.float32] = np.ndarray((2, 2), dtype=np.float32)

PROJECTION_MATRIX = np.array(
        (( 1, 0.5),
         (-1, 0.5)),
    dtype=np.float32)
REVERSE_PROJECTION_MATRIX = np.array(
        (( 0.5, -0.5),
         ( 1,  1)),
    dtype=np.float32)

def cast_points_to_isometric_v2(points: List[pygame.math.Vector2]) -> List[pygame.math.Vector2]:
    temp_points = []

    for point in points:
        iso_point = np.array(point, dtype=np.float32) @ PROJECTION_MATRIX
        temp_points.append(pygame.math.Vector2(tuple(iso_point)))

    return temp_points

def offset_points_v2(points: List[pygame.math.Vector2], render_info: RenderInfo) -> None:
    for x in range(len(points)):
        points[x] = points[x] + render_info.cam_offset

def cast_points_to_normal_v2(points: List[pygame.math.Vector2]) -> List[pygame.math.Vector2]:
    temp_points = []
    for point in points:
        normal_point = np.array(point, dtype=np.float32) @ REVERSE_PROJECTION_MATRIX
        temp_points.append(pygame.math.Vector2(tuple(normal_point)))

    return temp_points


import numpy as np
from typing import List, Tuple
from numpy.typing import NDArray
from .render_info import RenderInfo

PROJECTION_MATRIX: NDArray[np.float32] = np.ndarray((2, 2), dtype=np.float32)

PROJECTION_MATRIX = np.array(
        (( 1, 0.5),
         (-1, 0.5)),
    dtype=np.float32)

def cast_points_to_isometric(points: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    temp_points = []

    for point in points:
        point_array = np.array(point, dtype=np.float32)
        iso_point = point_array @ PROJECTION_MATRIX  # numpy matrix multiplication
        temp_points.append((int(iso_point[0]), int(iso_point[1])))

    return temp_points

def offset_points(points: List[Tuple[int, int]], render_info: RenderInfo) -> None:
    for x in range(len(points)):
        points[x] = (points[x][0] + render_info.cam_offset_x, points[x][1] + render_info.cam_offset_y)


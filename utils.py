import time
from typing import Any
import numpy as np
import cv2


def get_cv2_perspective_transform(src: cv2.Mat, dst: cv2.Mat) -> Any:
    return cv2.getPerspectiveTransform(src, dst)


def current_ms() -> int:
    return round(time.time() * 1000)


def calculate_coordinates(bg_size: tuple[int, int], obj_size: tuple[int, int]) -> tuple[tuple[int, int], tuple[int, int]]:
    bg_w, bg_h = bg_size
    obj_w, obj_h = obj_size
    x_range = (0, int(bg_w - obj_w))
    y_range = (0, int(bg_h - obj_h))
    return (x_range, y_range)


def get_pil_perspective_transform(src, dst):
    matrix = []
    for p1, p2 in zip(dst, src):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0,
                       -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1,
                       -p2[1]*p1[0], -p2[1]*p1[1]])
    A = np.matrix(matrix, dtype=np.float)
    B = np.array(src).reshape(8)
    res = np.dot(np.linalg.inv(A.T * A) * A.T, B)
    return np.array(res).reshape(8)

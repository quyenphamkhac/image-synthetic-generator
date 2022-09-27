import time
import numpy


def current_ms() -> int:
    return round(time.time() * 1000)


def calculate_coordinates(bg_size: tuple[int, int], obj_size: tuple[int, int]) -> tuple[tuple[int, int], tuple[int, int]]:
    bg_x, bg_y = bg_size
    obj_x, obj_y = obj_size
    x_range = (int(obj_x / 2), int(bg_x - obj_x / 2))
    y_range = (int(obj_y / 2), int(bg_y - obj_y / 2))
    return (x_range, y_range)


def find_coeffs(pa, pb):
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

    A = numpy.matrix(matrix, dtype=numpy.float)
    B = numpy.array(pb).reshape(8)

    res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
    return numpy.array(res).reshape(8)

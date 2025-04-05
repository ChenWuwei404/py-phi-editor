from typing import Callable
import numba

import numpy
import pygame

from math import sin, cos, pi, pow, sqrt, atan2

RADIUS = 1000
BORDER_COLOR = numpy.array((255, 255, 255), dtype=numpy.uint8)
A = 1

pygame.init()
screen = pygame.display.set_mode((RADIUS, )*2)


img = numpy.zeros((RADIUS, RADIUS, 3), dtype=numpy.uint8)


# def border_alpha(x: int, y: int, r: int) -> float:
#     point_distance = sqrt(x**2 + y**2)
#     angle = atan2(y, x)
#     line_distance = (1 + sin(2*angle)**2*0.09)*RADIUS
#     # line_distance = (1 + sin(2*angle)**2**1.2*0.15)*RADIUS
#     return max(1-abs(line_distance-1 - point_distance), 0)

# border_alpha_array = numpy.vectorize(border_alpha, excluded=['r'])

# img = numpy.array([[(border_alpha(i, j, RADIUS) * 255, )*3 for i in range(RADIUS)] for j in range(RADIUS)])

@numba.njit
def draw_border(img: numpy.ndarray, radius: int):
    for x in range(RADIUS):
        for y in range(RADIUS):
            point_distance = sqrt(x**2 + y**2)

            angle = atan2(y, x)
            line_distance = (1 + sin(2*angle)**2*0.09)*RADIUS
            # line_distance = (1 + sin(2*angle)**2**1.2*0.15)*RADIUS

            # if point_distance < line_distance:
            #     img[x, y] = BORDER_COLOR
            img[x, y] = max(1-abs(line_distance-1 - point_distance), 0) * 255

draw_border(img, RADIUS)
# mapping = numpy.array([[[i, j] for i in range(RADIUS)] for j in range(RADIUS)])
# print(mapping.shape)

# img = border_alpha_array(mapping[:, 0], mapping[:, 1], RADIUS) * 255

# for x in range(RADIUS):
#     for y in range(RADIUS):
#         point_distance = sqrt(x**2 + y**2)

#         angle = atan2(y, x)
#         line_distance = (1 + sin(2*angle)**2*0.09)*RADIUS
#         # line_distance = (1 + sin(2*angle)**2**1.2*0.15)*RADIUS

#         # if point_distance < line_distance:
#         #     img[x, y] = BORDER_COLOR
#         img[x, y] = max(1-abs(line_distance-1 - point_distance), 0) * 255


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    screen.fill((0, 0, 0))
    screen.blit(pygame.surfarray.make_surface(img), (0, 0))
    pygame.display.flip()
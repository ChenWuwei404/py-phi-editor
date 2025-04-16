import numpy, numba
import math

from pygame import Surface, Color, Rect, surfarray, draw

from math import sin, sqrt, atan2, ceil

LEFT = 0
RIGHT = 1

TOP = 0
BOTTOM = 2

@numba.jit()
def draw_border(img: numpy.ndarray, radius: int, fill_color: numpy.ndarray, border_color: numpy.ndarray, border_width: float):
    mx, my, mp = img.shape
    for x in range(min(mx, radius)):
        for y in range(min(my, radius)):
            point_distance = sqrt(x**2 + y**2)

            angle = atan2(y, x)
            line_distance = (1 + sin(2*angle)**2*0.09)*radius
            # line_distance = (1 + sin(2*angle)**2**1.2*0.15)*radius

            half_width = border_width/2 + 0.5

            delta = line_distance-half_width - point_distance
            line_alpha = min(max(half_width - abs(delta), 0), 1)

            if delta > 0:
                img[x, y] = (1 - line_alpha) * fill_color + line_alpha * border_color
                # alpha[x, y] = 255
            else:
                img[x, y] = (1 - line_alpha) * img[x, y] + line_alpha * border_color
                # alpha[x, y] = (1 - line_alpha) * alpha[x, y] + line_alpha * 255

@numba.jit()
def draw_solid(img: numpy.ndarray, radius: int, fill_color: numpy.ndarray):
    mx, my, mp = img.shape
    for x in range(min(mx, radius)):
        for y in range(min(my, radius)):
            point_distance = sqrt(x**2 + y**2)

            angle = atan2(y, x)
            line_distance = (1 + sin(2*angle)**2*0.09)*radius
            # line_distance = (1 + sin(2*angle)**2**1.2*0.15)*radius

            delta = line_distance - point_distance
            solid_alpha = min(max(delta, 0), 1)

            img[x, y] = (1 - solid_alpha) * img[x, y] + solid_alpha * fill_color

def corner(
        surface: Surface,
        center_x: int,
        center_y: int,
        direction: int,
        radius: int,
        fill_color: Color,
        border_color: Color,
        border_width: float = 1,
    ):
    """
    Parameters
    ----------
    surface: pygame.Surface, the surface to draw on

    center: tuple[int, int], the center of the corner

    direction: int, `RIGHT | BOTTOM` for example, to draw a bottom right corner

    fill_color: pygame.Color, the color of the fill

    border_color: pygame.Color, the color of the border

    border_width: int, the width of the border

    radius: int, the radius of the corner, if 0, the corner will be a rectangle

    """

    outer_x = center_x + radius if direction&RIGHT else center_x - radius
    outer_y = center_y + radius if direction&BOTTOM else center_y - radius

    rect_x = min(center_x, outer_x)
    rect_y = min(center_y, outer_y)
    rect_w = abs(center_x - outer_x)
    rect_h = abs(center_y - outer_y)

    try:
        corner_surface = surface.subsurface(rect_x, rect_y, rect_w, rect_h)
    except:
        w = min(surface.get_width() - rect_x, rect_w)
        h = min(surface.get_height() - rect_y, rect_h)
        if w > 0 and h > 0 and rect_x >= 0 and rect_y >= 0:
            corner_surface = surface.subsurface(rect_x, rect_y, w, h)
        else:
            return

    corner_array = surfarray.pixels3d(corner_surface)
    # alpha_array = surfarray.pixels_alpha(corner_surface)

    if not direction&RIGHT:
        corner_array = corner_array[::-1, :]
        # alpha_array = alpha_array[::-1, :]
    if not direction&BOTTOM:
        corner_array = corner_array[:, ::-1]
        # alpha_array = alpha_array[:, ::-1]

    if border_width == 1:
        border_width = 1.1

    if border_width:
        draw_border(corner_array, radius, numpy.array(fill_color[:3]), numpy.array(border_color[:3]), border_width)
    else:
        draw_solid(corner_array, radius, numpy.array(fill_color[:3]))

def rect(
        surface: Surface,
        fill_color: Color,
        border_color: Color,
        rect: Rect | tuple[int, int, int, int],
        border_width: int = 1,
        radius: int = 0,
    ):
    radius = int(radius*1.5)
    if radius:
        surface.lock()
        x, y, w, h = rect
        if border_width:
            corner(surface, x+w-radius, y+h-radius, RIGHT|BOTTOM, radius, fill_color, border_color, border_width)
            corner(surface, x+w-radius, y+radius, RIGHT|TOP, radius, fill_color, border_color, border_width)
            corner(surface, x+radius, y+h-radius, LEFT|BOTTOM, radius, fill_color, border_color, border_width)
            corner(surface, x+radius, y+radius, LEFT|TOP, radius, fill_color, border_color, border_width)
        else:
            corner(surface, x+w-radius, y+h-radius, RIGHT|BOTTOM, radius, fill_color, fill_color, border_width)
            corner(surface, x+w-radius, y+radius, RIGHT|TOP, radius, fill_color, fill_color, border_width)
            corner(surface, x+radius, y+h-radius, LEFT|BOTTOM, radius, fill_color, fill_color, border_width)
            corner(surface, x+radius, y+radius, LEFT|TOP, radius, fill_color, fill_color, border_width)

        rect = Rect(rect)
        draw.rect(surface, fill_color, rect.inflate(-2*radius, 0))
        draw.rect(surface, fill_color, (x, y+radius, radius, h-2*radius))
        draw.rect(surface, fill_color, (x+w-radius, y+radius, radius, h-2*radius))
        # surface.fill(fill_color, rect.inflate(-2*radius, 0))
        # surface.fill(fill_color, rect.inflate(0, -2*radius))
        if border_width:
            draw.rect(surface, border_color, (x, y+radius, border_width, h-2*radius))
            draw.rect(surface, border_color, (x+w-border_width, y+radius, border_width, h-2*radius))
            draw.rect(surface, border_color, (x+radius, y, w-2*radius, border_width))
            draw.rect(surface, border_color, (x+radius, y+h-border_width, w-2*radius, border_width))
            # surface.fill(border_color, (x, y+radius, border_width, h-2*radius))
            # surface.fill(border_color, (x+w-border_width, y+radius, border_width, h-2*radius))
            # surface.fill(border_color, (x+radius, y, w-2*radius, border_width))
            # surface.fill(border_color, (x+radius, y+h-border_width, w-2*radius, border_width))
        surface.unlock()

    
if __name__ == '__main__':
    import pygame
    from pygame import Color

    pygame.init()

    img = pygame.Surface((128, 128), flags=pygame.SRCALPHA)
    img.fill((255, 0, 0, 64))

    rect(img, Color(0, 128, 0), Color(255, 255, 255), (0, 0, 50, 50), 1, 10)

    screen = pygame.display.set_mode((1000, 1000))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill((0, 0, 0))
        screen.blit(img, (0, 0))
        pygame.display.update()

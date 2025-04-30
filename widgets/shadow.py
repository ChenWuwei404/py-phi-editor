from typing import Union
from .widget import Widget

from pygame import Surface, Color, transform
from pygame import SRCALPHA

class Shadow(Widget):
    def __init__(self, parent: Union['Widget', None]=None) -> None:
        super().__init__()
        self.shadow_color = Color(0, 0, 0, 128)
        self.shadow_offset_x = 0
        self.shadow_offset_y = 10
        self.shadow_radius = 32

    def draw_shadow(self, canvas: Surface):
        if not self.visible:
            return
        shadow_surface = Surface((self.width + self.shadow_radius * 2, self.height + self.shadow_radius * 2), SRCALPHA)
        shadow_surface.fill(self.shadow_color, (self.shadow_radius, self.shadow_radius, self.width, self.height))
        shadow_surface = transform.box_blur(shadow_surface, self.shadow_radius)
        canvas.blit(shadow_surface, (self.x - self.shadow_radius - self.shadow_offset_x, self.y - self.shadow_radius - self.shadow_offset_y))

    def draw(self, canvas: Surface):
        if self.visible:
            self.draw_shadow(canvas)
        return super().draw(canvas)
from pygame import Surface, draw

from .background_base import BackgroundBase, DynamicBackgroundBase
from .border_base import BorderBase

from .widget import Widget

class Card(BackgroundBase, BorderBase):
    def __init__(self, parent: Widget | None = None):
        super().__init__(parent)
        self.border_radius = 8

    def draw_background(self, canvas: Surface):
        draw.rect(canvas, self.background_color, self.rect, border_radius=self.border_radius)

    def draw_border(self, canvas: Surface):
        if self.border_width > 0:
            rect = self.rect.inflate(-self.border_width, -self.border_width)
            draw.rect(canvas, self.border_color_normal, rect, self.border_width, border_radius=self.border_radius)

class DynamicCard(Card, DynamicBackgroundBase):
    pass


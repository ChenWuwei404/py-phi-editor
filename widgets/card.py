from pygame import Surface, draw

from .background_base import BackgroundBase, DynamicBackgroundBase
from .border_base import BorderBase

from .widget import Widget

from numpy_renderer import painter

class Card(BackgroundBase, BorderBase):
    def __init__(self, parent: Widget | None = None):
        super().__init__(parent)
        self.border_radius = 8

    def draw_self(self, canvas: Surface):
        painter.rect(canvas, self.background_color, self.border_color_normal, self.rect, self.border_width, self.border_radius)

class DynamicCard(Card, DynamicBackgroundBase):
    pass


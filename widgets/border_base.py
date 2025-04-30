from pygame import Color, Surface, draw

from .widget import Widget

class BorderBase(Widget):
    def __init__(self, parent: Widget | None = None):
        super().__init__(parent)
        self.border_width = 1

        self.border_color_normal = Color((128, 128, 128))

    @property
    def border_color(self) -> Color:
        return self.border_color_normal

    def draw_border(self, canvas: Surface):
        if self.border_width > 0:
            rect = self.rect.inflate(self.border_width, self.border_width)
            draw.rect(canvas, self.border_color, rect, self.border_width)
from pygame import Color, Surface

from .widget import Widget

class ForegroundBase(Widget):
    def __init__(self, parent: Widget | None = None):
        super().__init__(parent)
        self.foreground_color_normal = Color(255, 255, 255)

    def draw_foreground(self, canvas: Surface):
        canvas.fill(self.foreground_color, self.visual_rect) if self.foreground_color.a else None

    @property
    def foreground_color(self) -> Color:
        return self.foreground_color_normal

class DynamicForegroundBase(ForegroundBase):
    def __init__(self, parent: Widget | None = None):
        super().__init__(parent)
        self.foreground_color_hover = Color(128, 128, 128)

    @property
    def foreground_color(self) -> Color:
        return self.foreground_color_hover if self.hover else self.foreground_color_normal
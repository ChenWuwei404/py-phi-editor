from pygame import Color, Surface

from .widget import Widget

class BackgroundBase(Widget):
    def __init__(self, parent: Widget | None = None):
        super().__init__(parent)
        self.background_color_normal = Color(24, 24, 24)

    def draw_background(self, canvas: Surface):
        canvas.fill(self.background_color, self.visual_rect)

    @property
    def background_color(self) -> Color:
        return self.background_color_normal

class DynamicBackgroundBase(BackgroundBase):
    def __init__(self, parent: Widget | None = None):
        super().__init__(parent)
        self.background_color_hover = Color(45, 46, 46)

    @property
    def background_color(self) -> Color:
        return self.background_color_hover if self.hover else self.background_color_normal
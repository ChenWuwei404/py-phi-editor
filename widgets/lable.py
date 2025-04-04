from pygame import Surface, Color
from .widget import Widget

from pygame.font import Font, SysFont, get_init

if not get_init():
    from pygame.font import init
    init()



DEFAULT_FONT = SysFont("cmdysj", 14)
# DEFAULT_FONT = Font()

class Lable(Widget):
    def __init__(self, text: str, parent: Widget | None = None):
        super().__init__(parent)
        self.font = DEFAULT_FONT
        self.set_text(text)
        self.color = Color((255, 255, 255))

    def text_render(self) -> Surface:
        text_surface = self.font.render(self.text, True, self.color)
        return text_surface.subsurface(0, 0, text_surface.width, int(text_surface.height*0.8))
    
    def draw_text(self, canvas: Surface):
        canvas.blit(self.text_render(), (self.x, self.y))

    def draw_self(self, canvas: Surface):
        self.draw_text(canvas)

    def set_text(self, text: str):
        self.text = text
        self.min_width, self.min_height = self.font.size(text)
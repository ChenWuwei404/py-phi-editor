from .widget import Widget
from .pinned import Pinned
from .card import Card
from .layout import VBoxLayout
from .padding import Padding
from .label import SubTitle
from .shadow import Shadow

from .button import Button

from pygame import Event, Surface, draw, Color

PADDING = 8

class RightClickMenu(Pinned, Card, Shadow):
    def __init__(self, position: tuple[int, int], parent=None):
        super().__init__(position, parent)
        self.set_layout(VBoxLayout())
        self.set_content_align(0)
        self.set_padding(Padding(PADDING))
        self.set_spacing(0)
        self.background_color_normal = Color(24, 24, 24)
        self.ease_in = 0

    def update(self):
        self.min_width = max(self.min_width, 200)
        [child.set_width(-1) for child in self.get_children()]
        self.ease_in += (1-self.ease_in)*0.1
        return super().update()
    
    
class MenuSeparator(Widget):
    def __init__(self, parent: RightClickMenu | None = None):
        super().__init__(parent)
        self.set_size(-1, 2*PADDING+1)

    def get_parent(self) -> RightClickMenu:
        parent = super().get_parent()
        if isinstance(parent, RightClickMenu):
            return parent
        else:
            raise ValueError("Parent of VSeparator must be RightClickMenu")

    def draw(self, canvas: Surface):
        parent = self.get_parent()
        canvas = canvas.get_parent()
        draw.line(canvas, parent.border_color_normal, (parent.x, parent.y+parent.padding.top + self.y+PADDING), (parent.x+parent.width-2, parent.y+parent.padding.top + self.y+PADDING), 1)


class RightClickButton(Button):
    def __init__(self, text: str, parent: Widget | None = None):
        super().__init__(text, parent)
        self.border_width = 0
        self.set_height(32)
        self.border_radius = 4
        self.background_color_normal = Color(0, 0, 0, 0)

    def draw_text(self, canvas: Surface):
        text_surface = super().text_render()
        text_rect = text_surface.get_rect(center=self.content_rect.center)
        canvas.blit(text_surface, (self.padding.left, text_rect.y))

    def get_parent(self) -> RightClickMenu:
        parent = super().get_parent()
        if isinstance(parent, RightClickMenu):
            return parent
        else:
            raise ValueError("Parent of VSeparator must be RightClickMenu")

class OnceRightClickButton(RightClickButton):
    def mouseLeftPressed(self, event: Event):
        super().mouseLeftPressed(event)
        self.get_parent().get_parent().remove_pinned_child(self.get_parent())

class RightClickMenuTitle(SubTitle):
    def __init__(self, text: str, parent: Widget | None = None):
        super().__init__(text, parent)
        self.set_height(32)
        self.set_padding(Padding(PADDING))

    def draw_text(self, canvas: Surface):
        text_surface = super().text_render()
        text_rect = text_surface.get_rect(center=self.content_rect.center)
        canvas.blit(text_surface, (0, text_rect.y))
from .widget import Widget
from .pinned import Pinned
from .card import Card
from .layout import VBoxLayout
from .padding import Padding

from .button import Button

from pygame import Event, Surface, draw

class RightClickMenu(Pinned, Card):
    def __init__(self, position: tuple[int, int], parent=None):
        super().__init__(position, parent)
        self.set_layout(VBoxLayout())
        self.set_content_align(0)
        self.set_padding(Padding(8))
        self.set_spacing(8)
        self.ease_in = 0

    def update(self):
        self.ease_in += (1-self.ease_in)*0.1
        return super().update()
    
    
class MenuSeparator(Widget):
    def __init__(self, parent: RightClickMenu | None = None):
        super().__init__(parent)
        self.set_size(-1, 1)

    def get_parent(self) -> RightClickMenu:
        parent = super().get_parent()
        if isinstance(parent, RightClickMenu):
            return parent
        else:
            raise ValueError("Parent of VSeparator must be RightClickMenu")

    def draw(self, canvas: Surface):
        parent = self.get_parent()
        canvas = canvas.get_parent()
        draw.line(canvas, parent.border_color_normal, (parent.x, parent.y+parent.padding.top + self.y), (parent.x+parent.width-2, parent.y+parent.padding.top + self.y), 1)


class RightClickButton(Button):
    def __init__(self, text: str, parent: Widget | None = None):
        super().__init__(text, parent)
        self.border_width = 0
        self.set_height(32)

    def get_parent(self) -> RightClickMenu:
        parent = super().get_parent()
        if isinstance(parent, RightClickMenu):
            return parent
        else:
            raise ValueError("Parent of VSeparator must be RightClickMenu")

class OneTimeRightClickButton(RightClickButton):
    def mouseLeftPressed(self, event: Event):
        super().mouseLeftPressed(event)
        self.get_parent().get_parent().remove_pinned_child(self.get_parent())
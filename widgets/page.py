from .widget import Widget
from .padding import Padding

from pygame import Surface

class Page(Widget):
    def __init__(self, screen: Surface, parent = None):
        super().__init__(parent)
        self.screen = screen
        self.set_padding(Padding(0))

        self.pinned_children: list[Widget] = []

    def update(self):
        super().update()
        self.set_size(*self.screen.size)
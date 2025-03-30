from widget import Widget

from pygame import Surface

class Page(Widget):
    def __init__(self, screen: Surface, parent = None):
        super().__init__(parent)
        self.screen = screen

        self.pinned_children: list[Widget] = []

    def update(self):
        super().update()
        self.set_size(*self.screen.size)
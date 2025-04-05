from .widget import Widget
from .padding import Padding

from pygame import Surface, Event, MOUSEBUTTONDOWN, mouse

class Page(Widget):
    def __init__(self, screen: Surface, parent = None):
        super().__init__(parent)
        self.screen = screen
        self.set_padding(Padding(0))

        self.pinned_children: list[Widget] = []

    def add_pinned_child(self, child: Widget):
        self.pinned_children.append(child)
        child.set_parent(self)

    def remove_pinned_child(self, child: Widget):
        self.pinned_children.remove(child)
        child.set_parent(None)

    def get_childern(self) -> list[Widget]:
        return super().get_childern() + self.pinned_children

    def update(self):
        self.set_size(*self.screen.size)
        super().update()

    def process_event(self, event: Event):
        if self.pinned_children and event.type == MOUSEBUTTONDOWN:
            if not self.pinned_children[-1].absolute_rect.collidepoint(event.pos):
                self.pinned_children.pop()
                return
        super().process_event(event)

    def mousePressed(self, event: Event):
        self.pinned_children.clear()

    # def mouseLeftPressed(self, event: Event):
    #     self.pinned_children.pop() if self.pinned_children else None
    #     if self.pinned_children:
    #         if self.pinned_children[-1].absolute_rect.collidepoint(event.pos):
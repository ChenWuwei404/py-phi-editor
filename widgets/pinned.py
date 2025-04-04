from .widget import Widget
from .page import Page
from typing import Union

class Pinned(Widget):
    def __init__(self, position: tuple[int, int], parent = None):
        super().__init__(parent)
        self.set_pos(*position)
            
    def get_parent(self) -> Page:
        parent = super().get_parent()
        if isinstance(parent, Page):
            return parent
        else:
            raise ValueError("Parent of VSeparator must be Page")
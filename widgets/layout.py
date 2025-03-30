from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    from widget import Widget

class WLayout:
    def __init__(self) -> None:
        self.parent: Union['Widget', None] = None

    def update(self):
        pass

class HBoxLayout(WLayout):
    def update(self):
        if self.parent is None:
            return
        parent = self.parent

        x = 0
        max_line_height = 0
        total_height = 0
        
        for i in range(len(parent.children)):
            parent.children[i].set_pos(x, total_height)
            max_line_height = max(max_line_height, parent.children[i].height)
            x += parent.children[i].width + (parent.spacing if i < len(parent.children) - 1 else 0)
            if i < len(parent.children) - 1 and x + parent.children[i+1].width > parent.content_width:
                x = 0
                total_height += max_line_height + parent.spacing
                max_line_height = 0
        total_height += max_line_height

        # for child in parent.children:
        #     child.set_pos(x, total_height)
        #     max_line_height = max(max_line_height, child.height)
        #     x += child.width + parent.spacing
        #     if x + child.width > parent.content_width:
        #         x = 0
        #         total_height += max_line_height + parent.spacing
        #         max_line_height = 0
        # total_height += max_line_height

        parent.min_height = total_height + parent.padding.top + parent.padding.bottom
        parent.min_width = parent.padding.left + parent.padding.right

class VBoxLayout(WLayout):
    def update(self):
        if self.parent is None:
            return
        parent = self.parent

        y = 0
        max_col_width = 0

        for child in parent.children:
            child.max_width = parent.content_width
            child.set_pos((parent.content_width-child.width)//2, y)
            max_col_width = max(max_col_width, child.width)
            y += child.height + parent.spacing
        y -= parent.spacing
        parent.min_width = max_col_width + parent.padding.left + parent.padding.right
        parent.min_height = y + parent.padding.top + parent.padding.bottom
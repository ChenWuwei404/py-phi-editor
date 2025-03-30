from typing import Union
from pygame import Event, Surface, Rect
from pygame.constants import MOUSEMOTION

from .padding import Padding
from .layout import WLayout


class Widget:
    def __init__(self, parent: Union['Widget', None]=None):
        self.parent = parent
        self.children: list['Widget'] = []
        self.visible = True
        self.enabled = True


        self.x = 0
        self.y = 0


        self.setted_width = 0
        self.setted_height = 0

        self.min_width = 0
        self.min_height = 0

        self.max_width = 0
        self.max_height = 0

        self.padding = Padding(16)
        self.spacing = 16

        self.focus = False
        self.hover = False

        self.layout = WLayout()
        self.content_align = 1  # 0 left, 1 center, 2 right


    @property
    def width(self) -> int:
        if self.setted_width > 0:
            return self.setted_width
        elif self.setted_width == -1 and self.max_width > self.min_width:
            return self.max_width
        else:
            return self.min_width

    @property
    def height(self) -> int:
        if self.setted_height > 0:
            return self.setted_height
        elif self.setted_height == -1 and self.max_height > self.min_height:
            return self.max_height
        else:
            return self.min_height
        
    @property
    def rect(self) -> Rect:
        return Rect(self.x, self.y, self.width, self.height)

    @property
    def absolute_x(self) -> int:
        return self.x + (self.parent.absolute_x + self.parent.padding.left if self.parent else 0)
    
    @property
    def absolute_y(self) -> int:
        return self.y + (self.parent.absolute_y + self.parent.padding.top if self.parent else 0)
        
    @property
    def absolute_rect(self) -> Rect:
        return Rect(self.absolute_x, self.absolute_y, self.width, self.height)

    @property
    def content_width(self) -> int:
        return max(0, self.width - self.padding.left - self.padding.right)

    @property
    def content_height(self) -> int:
        return max(0, self.height - self.padding.top - self.padding.bottom)

    @property
    def content_rect(self) -> Rect:
        return Rect(self.x + self.padding.left, self.y + self.padding.top, self.content_width, self.content_height)
    


    def add_child(self, child: 'Widget'):
        self.children.append(child)
        child.parent = self

    def remove_child(self, child: 'Widget'):
        self.children.remove(child)
        child.parent = None

    def set_visible(self, visible: bool = True):
        self.visible = visible

    def set_enabled(self, enabled: bool = True):
        self.enabled = enabled



    def set_focus(self, focus: bool = False):
        if self.parent and focus:
            self.get_root().clear_focus()
        self.focus = focus

    def get_root(self) -> 'Widget':
        if self.parent:
            return self.parent.get_root()
        else:
            return self

    def clear_focus(self):
        self.focus = False
        [child.clear_focus() for child in self.children]

    def set_x(self, x: int):
        self.x = x

    def set_y(self, y: int):
        self.y = y

    def set_pos(self, x: int, y: int):
        self.set_x(x)
        self.set_y(y)

    def set_width(self, width: int):
        self.setted_width = width

    def set_height(self, height: int):
        self.setted_height = height

    def set_size(self, width: int, height: int):
        self.set_width(width)
        self.set_height(height)

    def get_pos(self) -> tuple[int, int]:
        return self.x, self.y

    def get_size(self) -> tuple[int, int]:
        return self.width, self.height
    
    def set_layout(self, layout: WLayout):
        layout.parent = self
        self.layout = layout

    def set_padding(self, padding: Padding):
        self.padding = padding

    def set_spacing(self, spacing: int):
        self.spacing = spacing

    def set_content_align(self, align: int):
        self.content_align = align


    def draw(self, canvas: Surface):
        self.draw_self(canvas)
        self.draw_children(canvas)

    def draw_self(self, canvas: Surface):
        self.draw_background(canvas)
        self.draw_border(canvas)

    def draw_background(self, canvas: Surface):
        pass

    def draw_border(self, canvas: Surface):
        pass

    def draw_children(self, canvas: Surface):
        if self.children:
            try:
                canvas = canvas.subsurface(self.content_rect)
            except:
                x, y = self.content_rect.topleft
                canvas = canvas.subsurface((x, y, canvas.get_width()-x, canvas.get_height()-y))
            [child.draw(canvas) for child in self.children if child.visible]

    def update(self):
        self.layout.update()
        [child.update() for child in self.children if child.visible]

    def process_event(self, event: Event):
        if event.type == MOUSEMOTION:
            self.hover = self.absolute_rect.collidepoint(event.pos)
            [child.process_event(event) for child in self.children if child.visible and child.enabled]

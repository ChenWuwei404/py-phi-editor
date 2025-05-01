from typing import Union, TYPE_CHECKING
from pygame import Event, Surface, Rect, mouse
from pygame.constants import *  # type: ignore

from .padding import Padding

from .layout import Layout
from .trigger import Trigger

if TYPE_CHECKING:
    from .page import Page


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

        self.max_width_layout = 0
        self.max_height_layout = 0

        self.padding = Padding(16)
        self.spacing = 16

        self.focus = False
        self.hover = False

        self.layout = Layout()
        self.content_align = 1  # 0 left, 1 center, 2 right

        self.left_pressed = Trigger()
        self.left_released = Trigger()

        self.right_pressed = Trigger()
        self.right_released = Trigger()

        self.mouse_enter = Trigger()
        self.mouse_leave = Trigger()
        
    @property
    def max_width(self) -> int:
        if self.max_width_layout:
            return self.max_width_layout
        else:
            return self.parent.max_width if self.parent else 0
        
    @property
    def max_height(self) -> int:
        if self.max_height_layout:
            return self.max_height_layout
        else:
            return self.parent.max_height if self.parent else 0

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
    
    def set_parent(self, parent: Union['Widget', None]=None):
        self.parent = parent

    def get_parent(self) -> 'Widget':
        if self.parent:
            return self.parent
        else:
            raise ValueError('Widget has no parent')

    def add_child(self, child: 'Widget'):
        self.children.append(child)
        child.set_parent(self)

    def remove_child(self, child: 'Widget'):
        self.children.remove(child)
        child.set_parent(None)

    def get_children(self) -> list['Widget']:
        return self.children

    def set_visible(self, visible: bool = True):
        self.visible = visible

    def set_enabled(self, enabled: bool = True):
        self.enabled = enabled



    def set_focus(self, focus: bool = False):
        if self.parent and focus:
            self.get_root().clear_focus()
        self.focus = focus

    def get_root(self) -> 'Page':
        if self.parent:
            return self.parent.get_root()
        else:
            if self.parent == None:
                return self  # type: ignore
            else:
                raise ValueError('Widget has no parent')

    def clear_focus(self):
        self.focus = False
        [child.clear_focus() for child in self.get_children()]

    def set_x(self, x: int):
        self.x = x

    def set_y(self, y: int):
        self.y = y

    def set_pos(self, x: int, y: int):
        self.set_x(x)
        self.set_y(y)

    def set_width(self, width: float):
        self.setted_width = int(width)

    def set_height(self, height: float):
        self.setted_height = int(height)

    def set_size(self, width: float, height: float):
        self.set_width(width)
        self.set_height(height)

    def get_pos(self) -> tuple[int, int]:
        return self.x, self.y

    def get_size(self) -> tuple[int, int]:
        return self.width, self.height
    
    def set_layout(self, layout: Layout):
        layout.parent = self
        self.layout = layout

    def set_padding(self, padding: Padding):
        self.padding = padding

    def set_spacing(self, spacing: int):
        self.spacing = spacing

    def set_content_align(self, align: int):
        self.content_align = align


    @property
    def visual_rect(self) -> Rect:
        return self.rect

    def draw(self, canvas: Surface):
        """
        Drawing order:
        - `draw_background()`
        - `draw_content()`
          - `draw_children()`
          - `draw_foreground()`
        - `draw_shape()`
          - `draw_border()`
        
        """
        self.draw_background(canvas)
        self.draw_content(canvas)
        self.draw_shape(canvas)

    def draw_content(self, canvas: Surface):
        self.draw_children(canvas)
        self.draw_foreground(canvas)

    def draw_foreground(self, canvas: Surface):
        pass

    def draw_shape(self, canvas: Surface):
        self.draw_border(canvas)

    def draw_background(self, canvas: Surface):
        pass

    def draw_border(self, canvas: Surface):
        pass

    def get_subsurface(self, canvas: Surface) -> Surface | None:
        return canvas.subsurface(self.content_rect.clip(canvas.get_rect())) if self.content_rect.colliderect(canvas.get_rect()) else None

    def draw_children(self, canvas: Surface):
        if self.get_children():
            sub_canvas = self.get_subsurface(canvas)
            [child.draw(sub_canvas) for child in self.get_children() if child.visible] if sub_canvas else None

    def update(self):
        self.layout.update()
        [child.update() for child in self.get_children() if child.visible]

    def process_event(self, event: Event):
        if event.type == MOUSEMOTION:
            if self.absolute_rect.collidepoint(mouse.get_pos()):
                self.mouseEnter(event) if self.hover else None
                self.hover = True
            else:
                self.mouseLeave(event) if self.hover else None
                self.hover = False
            [child.process_event(event) for child in self.get_children() if child.visible and child.enabled]

        if event.type in {MOUSEBUTTONDOWN, MOUSEBUTTONUP}:
            for child in reversed(self.get_children()):
                if child.visible and child.enabled and child.absolute_rect.collidepoint(event.pos):
                    child.process_event(event)
                    return

            if event.type == MOUSEBUTTONDOWN:
                self.mousePressed(event)
                if self.absolute_rect.collidepoint(event.pos):
                    if event.button == 1:
                        self.mouseLeftPressed(event)
                    elif event.button == 3:
                        self.mouseRightPressed(event)
            elif event.type == MOUSEBUTTONUP:
                self.mouseReleased(event)
                if self.absolute_rect.collidepoint(event.pos):
                    if event.button == 1:
                        self.mouseLeftReleased(event)
                    elif event.button == 3:
                        self.mouseRightReleased(event)

    def mousePressed(self, event: Event):
        pass

    def mouseReleased(self, event: Event):
        pass

    def mouseLeftPressed(self, event: Event):
        self.left_pressed(event)

    def mouseLeftReleased(self, event: Event):
        self.left_released(event)

    def mouseRightPressed(self, event: Event):
        self.right_pressed(event)

    def mouseRightReleased(self, event: Event):
        self.right_released(event)

    def keyPressed(self, event: Event):
        pass

    def keyReleased(self, event: Event):
        pass

    def textEdit(self, event: Event):
        pass

    def textInput(self, event: Event):
        pass

    def mouseWheel(self, event: Event):
        pass

    def mouseEnter(self, event: Event):
        self.mouse_enter(event)

    def mouseLeave(self, event: Event):
        self.mouse_leave(event)

    # def __del__(self):
    #     self.parent = None
    #     self.children = []
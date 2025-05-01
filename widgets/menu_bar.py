from .background_base import BackgroundBase
from .layout import HBoxLayout
from .padding import Padding
from .button import Button

from pygame import Surface, Color, draw, Rect

from numpy_renderer import painter

class MenuBar(BackgroundBase):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.background_color_normal = Color(32, 32, 32)
        self.set_width(-1)
        self.set_layout(HBoxLayout())
        self.set_padding(Padding(0))
        self.set_spacing(0)

class MenuBarButton(Button):
    def __init__(self, text, parent = None):
        super().__init__(text, parent)
        self.background_color_normal = Color(0, 0, 0, 0)
        self.background_color_hover = Color(46, 46, 46)
        self.border_width = 0

        self.set_height(32)
        self.set_padding(Padding(8))

    @property
    def visual_rect(self) -> Rect:
        return self.rect.inflate(-self.padding.left, -self.padding.top)

    def update(self):
        super().update()
        self.color = Color(255, 255, 255) if self.hover else Color(128, 128, 128)


if __name__ == '__main__':
    import pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)

    menu = MenuBar()
    menu.set_size(-1, 32)
    button1 = MenuBarButton("File")
    button2 = MenuBarButton("Edit")
    button3 = MenuBarButton("View-g")
    button4 = MenuBarButton("Help")
    menu.add_child(button1)
    menu.add_child(button2)
    menu.add_child(button3)
    menu.add_child(button4)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEMOTION:
                menu.process_event(event)
        screen.fill((0, 0, 0))
        menu.max_width_layout = screen.get_width()
        menu.update()
        menu.draw(screen)
        pygame.display.update()
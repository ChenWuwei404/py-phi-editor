from pygame import Surface, Event
from .background_base import BackgroundBase
from .card import Card, DynamicCard
from .label import Label

from .widget import Widget

class Button(Label, DynamicCard):
    def __init__(self, text: str, parent: Widget | None = None):
        super(DynamicCard, self).__init__(parent)
        super().__init__(text, parent)
        self.set_height(48)

    def draw_text(self, canvas: Surface):
        text_surface = super().text_render()
        text_rect = text_surface.get_rect(center=self.content_rect.center)
        canvas.blit(text_surface, text_rect)

    def set_text(self, text: str):
        self.text = text
        self.min_width, self.min_height = self.font.size(text)
        self.min_width += self.padding.left + self.padding.right
        self.min_height += self.padding.top + self.padding.bottom


if __name__ == '__main__':
    import pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    card = Button("Hello World", None)
    card.set_pos(50, 50)
    # card.set_size(200, 100)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEMOTION:
                card.process_event(event)
        screen.fill((0, 0, 0))
        card.draw(screen)
        pygame.display.update()
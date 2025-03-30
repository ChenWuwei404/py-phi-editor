from button import Button
from card import Card

from widget import Widget

from layout import HBoxLayout, VBoxLayout



import pygame
pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
b1 = Button("Test Button 1")
b2 = Button("Test Button 02")
b3 = Button("Test Button 00003")
b4 = Button("Test Button")
b5 = Button("Test Button")



l = Card()
l.set_size(*screen.size)
l.add_child(b1)
l.add_child(b2)
l.add_child(b3)
l.add_child(b4)
l.add_child(b5)

l.set_layout(HBoxLayout())

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEMOTION:
            l.process_event(event)
    screen.fill((0, 0, 0))
    l.set_size(-1, 0)
    l.max_width = screen.get_width()
    l.update()
    l.draw(screen)
    pygame.display.flip()
    print(clock.get_fps())
    clock.tick()
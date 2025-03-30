import pygame

pygame.init()

from widgets import *

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("PyPhiEditor")
pygame.display.set_icon(pygame.image.load(r'./resource/phi.png'))


clock = pygame.time.Clock()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    

    clock.tick(60)
    pygame.display.update()

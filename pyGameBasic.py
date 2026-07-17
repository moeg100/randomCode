import pygame
import os

import sys

pygame.init()


size = w, h, = 500, 300

screen = pygame.display.set_mode(size)

rect = pygame.draw.rect(screen, "Green", (100, 100, 100, 100), 6)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
    
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (231, 55, 21), (100, 150, 200, 100))
    target_rect = pygame.Rect(400, 150, 200, 100)
    pygame.draw.rect(screen, (66, 111, 232), target_rect, width=5)
    
    pygame.display.flip()




pygame.quit()
sys.exit()

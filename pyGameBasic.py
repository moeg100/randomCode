import pygame
import os
import random as rd
import pygame.gfxdraw
import sys

pygame.init()


size = w, h, = 500, 300

screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()

dt = 0




player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

running = True
while running:

    numRandom = rd.randint(1, 255)
    numRandom2 = rd.randint(1, 255)
    numRandom3 = rd.randint(1, 255)
    #print(numRandom)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
    
    screen.fill((122, 52, 67))


    # Render start here

    pygame.draw.rect(screen, (231, 55, 21), (200, 150, 200, 100))
    target_rect = pygame.Rect(200, 50, 200, 100)
    pygame.draw.rect(screen, (66, 111, 232), target_rect, width=3)

    pygame.draw.circle(screen, (numRandom, numRandom2, numRandom3), player_pos, 40)

    pygame.gfxdraw.pixel(screen, 209, 140, (numRandom, numRandom2, numRandom3))
s


    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt


    if target_rect.collidepoint(player_pos):
        print("something is colliding")
    print(player_pos)

    pygame.display.flip()
    dt = clock.tick(30) / 10000



pygame.quit()
sys.exit()

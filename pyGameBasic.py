import pygame
import os
import random as rd
import pygame.gfxdraw
import sys

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 500, 300
PLAYER_SPEED = 300
RECT_POS = (200, 150)
RECT_SIZE = (200, 100)
FPS = 30
BG_COLOR = (122, 52, 67)
RECT_COLOR = (231, 55, 21)
TARGET_COLOR = (66, 111, 232)


size = SCREEN_WIDTH, SCREEN_HEIGHT

screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()

dt = 0




player_pos = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
target_rect = pygame.Rect(200, 50, 200, 100)


running = True
while running:

    numRandom = rd.randint(1, 255)
    numRandom2 = rd.randint(1, 255)
    numRandom3 = rd.randint(1, 255)
    #print(numRandom)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
    
    screen.fill(BG_COLOR)


    # Render start here

    pygame.draw.rect(screen, RECT_COLOR, (200, 150, 200, 100))
    pygame.draw.rect(screen, TARGET_COLOR, target_rect, width=3)

    pygame.draw.circle(screen, (numRandom, numRandom2, numRandom3), player_pos, 40)

    pygame.gfxdraw.pixel(screen, 209, 140, (numRandom, numRandom2, numRandom3))


    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        player_pos.y -= PLAYER_SPEED * dt
    if keys[pygame.K_s]:
        player_pos.y += PLAYER_SPEED * dt
    if keys[pygame.K_a]:
        player_pos.x -= PLAYER_SPEED * dt
    if keys[pygame.K_d]:
        player_pos.x += PLAYER_SPEED * dt


    player_pos.x = max(40, min(SCREEN_WIDTH - 40, player_pos.x))
    player_pos.y = max(40, min(SCREEN_HEIGHT - 40, player_pos.y))

    if target_rect.collidepoint(player_pos):
        print("something is colliding")
    print(player_pos)

    pygame.display.flip()

    dt = clock.tick(FPS) / 1000



pygame.quit()
sys.exit()

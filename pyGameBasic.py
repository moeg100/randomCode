import pygame
import random as rd
import sys

import math as mth

pygame.init()

# Constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 300
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

PLAYER_SPEED = 300
FPS = 60

RECT_POS = (200, 150)
RECT_SIZE = (200, 100)

BG_COLOR = (122, 52, 67)
RECT_COLOR = (231, 55, 21)
TARGET_COLOR = (66, 111, 232)

BALL_RADIUS = 20
GRAVITY = 0.5
BOUNCE = -0.8
GROUND_Y = 300


# The main display
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
dt = 0

pixel_surface = pygame.Surface(SCREEN_SIZE)

# Ball 1
ball_one = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

# Ball 2 with gravity
ball_two = pygame.Vector2(300, 200)
ball_velocity_y = 0


print(ball_one)

# Target rectangle
target_rect = pygame.Rect(200, 50, 200, 100)


running = True

def keyEvent():
    keys = pygame.key.get_pressed()


    if keys[pygame.K_q]:
        sys.exit()

    if keys[pygame.K_SPACE]:
        global ball_velocity_y
        ball_velocity_y -= GRAVITY

    if keys[pygame.K_w]:
        ball_one.y -= PLAYER_SPEED * dt

    if keys[pygame.K_s]:
        ball_one.y += PLAYER_SPEED * dt

    if keys[pygame.K_a]:
        ball_one.x -= PLAYER_SPEED * dt
        ball_two.x -= PLAYER_SPEED * dt


    if keys[pygame.K_d]:
        ball_one.x += PLAYER_SPEED * dt
        ball_two.x += PLAYER_SPEED * dt

    if keys[pygame.K_r]:
    	ball_two.x = 250
    	ball_two.y = 250


while running:

    random_r = rd.randint(1, 255)
    random_g = rd.randint(1, 255)
    random_b = rd.randint(1, 255)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw random pixels
    random_pixel_x = rd.randint(0, SCREEN_WIDTH - 1)
    random_pixel_y = rd.randint(0, SCREEN_HEIGHT - 1)

    # This draws the pixels color
    random_color = (
            rd.randint(0, 255),
            rd.randint(0, 255),
            rd.randint(0, 255),
        )

    pixel_surface.set_at((random_pixel_x, random_pixel_y), random_color)

    screen.blit(pixel_surface, (0, 0))


    # The two rectangles
    pygame.draw.rect(screen, RECT_COLOR, (*RECT_POS, *RECT_SIZE))
    pygame.draw.rect(screen, TARGET_COLOR, target_rect, width=3)


    # Circle 1
    pygame.draw.circle(
        screen,
        (random_r, random_g, random_b),
        ball_one,
        BALL_RADIUS,
    )

    # Ball physics
    ball_velocity_y += GRAVITY
    ball_two.y += ball_velocity_y

    if ball_two.y + BALL_RADIUS >= GROUND_Y:
        ball_two.y = GROUND_Y - BALL_RADIUS
        ball_velocity_y *= BOUNCE

    #distance = mth.sqrt((ball_two.x - ball_one.x)**2 + (ball_two.y - ball_one.y)**2)
    distance = (ball_two.x - ball_one.x)**2 + (ball_two.y - ball_one.y)**2

    #print(distance)

    distanceToMove = BALL_RADIUS *2 - mth.sqrt(distance)
    print(distanceToMove)

    angle = (mth.atan2(ball_two.y-ball_one.y, ball_two.x-ball_one.x))
    #print(angle)



    """
    if distance <= (BALL_RADIUS*2)**2:
        print("COLLISION") #detecting collision
        ball_two.x += mth.cos(angle) * distanceToMove
        ball_two.y += mth.sin(angle) * distanceToMove
    """
    if not (distanceToMove < 0):
    	print("COLLISION")
    	ball_two.x += mth.cos(angle) * distanceToMove
    	ball_two.y += mth.sin(angle) * distanceToMove

    # Circle 2
    pygame.draw.circle(
        screen,
        (255, 250, 50),
        (ball_two.x, int(ball_two.y)),
        BALL_RADIUS,
    )

    pygame.draw.line(
        screen,
        (255, 255, 255),
        (0, GROUND_Y),
        (SCREEN_WIDTH, GROUND_Y),
        3,
    )

    keyEvent()

    ball_one.x = max(BALL_RADIUS, min(SCREEN_WIDTH - BALL_RADIUS, ball_one.x))
    ball_one.y = max(BALL_RADIUS, min(SCREEN_HEIGHT - BALL_RADIUS, ball_one.y))

    if target_rect.collidepoint(ball_one):
        print("Something is colliding.")

    pygame.display.flip()

    dt = clock.tick(FPS) / 1000

pygame.quit()
sys.exit()

import pygame
import random as rd
import sys

pygame.init()

# Constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 300
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

PLAYER_SPEED = 300
FPS = 30

RECT_POS = (200, 150)
RECT_SIZE = (200, 100)

BG_COLOR = (122, 52, 67)
RECT_COLOR = (231, 55, 21)
TARGET_COLOR = (66, 111, 232)

BALL_RADIUS = 30
GRAVITY = 0.5
BOUNCE = -0.8
GROUND_Y = 300

# Display
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
dt = 0

pixel_surface = pygame.Surface(SCREEN_SIZE)

# Player
player_pos = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

# Target
target_rect = pygame.Rect(200, 50, 200, 100)

# Ball
ball_x = 300
ball_y = 100
ball_velocity_y = 0

running = True

while running:

    random_r = rd.randint(1, 255)
    random_g = rd.randint(1, 255)
    random_b = rd.randint(1, 255)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw random pixels
    for _ in range(10):
        random_pixel_x = rd.randint(0, SCREEN_WIDTH - 1)
        random_pixel_y = rd.randint(0, SCREEN_HEIGHT - 1)

        random_color = (
            rd.randint(0, 255),
            rd.randint(0, 255),
            rd.randint(0, 255),
        )

        pixel_surface.set_at((random_pixel_x, random_pixel_y), random_color)

    screen.blit(pixel_surface, (0, 0))

    pygame.draw.rect(screen, RECT_COLOR, (*RECT_POS, *RECT_SIZE))
    pygame.draw.rect(screen, TARGET_COLOR, target_rect, width=3)

    pygame.draw.circle(
        screen,
        (random_r, random_g, random_b),
        player_pos,
        40,
    )

    # Ball physics
    ball_velocity_y += GRAVITY
    ball_y += ball_velocity_y

    if ball_y + BALL_RADIUS >= GROUND_Y:
        ball_y = GROUND_Y - BALL_RADIUS
        ball_velocity_y *= BOUNCE

    pygame.draw.circle(
        screen,
        (255, 250, 50),
        (ball_x, int(ball_y)),
        BALL_RADIUS,
    )

    pygame.draw.line(
        screen,
        (255, 255, 255),
        (0, GROUND_Y),
        (SCREEN_WIDTH, GROUND_Y),
        3,
    )

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        player_pos.y -= PLAYER_SPEED * dt
        ball_velocity_y -= GRAVITY

    if keys[pygame.K_s]:
        player_pos.y += PLAYER_SPEED * dt

    if keys[pygame.K_a]:
        player_pos.x -= PLAYER_SPEED * dt

    if keys[pygame.K_d]:
        player_pos.x += PLAYER_SPEED * dt

    player_pos.x = max(40, min(SCREEN_WIDTH - 40, player_pos.x))
    player_pos.y = max(40, min(SCREEN_HEIGHT - 40, player_pos.y))

    if target_rect.collidepoint(player_pos):
        print("Something is colliding.")

    pygame.display.flip()

    dt = clock.tick(FPS) / 1000

pygame.quit()
sys.exit()

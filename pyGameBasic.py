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

BG_COLOR = (0, 0, 0)
RECT_COLOR = (231, 55, 21)
TARGET_COLOR = (66, 111, 232)

BALL_RADIUS = 5
GRAVITY = 0.5
BOUNCE = -0.8

SMALL_TRIANGLE = [[100,150],[120,150],[110,175]]
ROTATION_SPEED = 1
TRIANGLE_ORIGIN = [rd.randint(100, 200), rd.randint(100, 200)]

# The main display
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
dt = 0

pixel_surface = pygame.Surface(SCREEN_SIZE)

# Ball 1
ball_one = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
ball_velocity_one = 0
# Ball 2 with gravity
ball_two = pygame.Vector2(SCREEN_WIDTH / 4, SCREEN_HEIGHT / 4)
ball_velocity_two = 0




# Target rectangle
target_rect = pygame.Rect(200, 50, *RECT_SIZE)


running = True

def circleRectCollide(circle, radius, rectangle):
    x = max(rectangle.left, min(circle.x, rectangle.right))
    y = max(rectangle.top, min(circle.y, rectangle.bottom))

    closest_point = pygame.Vector2(x, y)
    delta = circle - closest_point
    #print(f"DELTA : {delta}")
    distance = delta.length()


    is_colliding = distance <= radius

    # normal from rect toward circle center (needed for push-out)
    if distance != 0:
        normal = delta / distance
    else:
        normal = pygame.Vector2(0, -1)  # arbitrary fallback (corner case)

    return is_colliding, distance, normal

def erase_pixels_under_ball(surface, ball_pos, radius, bg_color):
    bx, by = int(ball_pos.x), int(ball_pos.y)

    for x in range(bx - radius, bx + radius + 1):
        for y in range(by - radius, by + radius + 1):
            if 0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT:
                if (x - bx) ** 2 + (y - by) ** 2 <= radius ** 2:
                    if surface.get_at((x, y))[:3] != bg_color:
                        surface.set_at((x, y), bg_color)
                        
          
def triangle_area(triangle_pos):
    ax, ay = int(triangle_pos[0][0]), int(triangle_pos[0][1])
    bx, by = int(triangle_pos[1][0]), int(triangle_pos[1][1])
    cx, cy = int(triangle_pos[2][0]), int(triangle_pos[2][1])
    
    area = 0.5 * abs(ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    
    return area
                  
def erase_pixels_under_triangle(surface, triangle_pos, bg_color):
    ax, ay = triangle_pos[0]
    bx, by = triangle_pos[1]
    cx, cy = triangle_pos[2]


    min_x = max(0, int(min(ax, bx, cx)))
    max_x = min(SCREEN_WIDTH - 1, int(max(ax, bx, cx)))
    min_y = max(0, int(min(ay, by, cy)))
    max_y = min(SCREEN_HEIGHT - 1, int(max(ay, by, cy)))


    total_area = triangle_area(triangle_pos)
    
    if total_area == 0:
        return


    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):

            p = [[x, y], triangle_pos[1], triangle_pos[2]]
            p2 = [triangle_pos[0], [x, y], triangle_pos[2]]
            p3 = [triangle_pos[0], triangle_pos[1], [x, y]]
            
            sub_area_sum = triangle_area(p) + triangle_area(p2) + triangle_area(p3)
            

            if abs(sub_area_sum - total_area) < 0.1:
                if surface.get_at((x, y))[:3] != bg_color:
                    surface.set_at((x, y), bg_color)

def rotate(angle, point, origin):
    x = ((point[0] - origin[0]) * mth.cos(angle) - (point[1] - origin[1]) * mth.sin(angle)) + origin[0]
    y = ((point[0] - origin[0]) * mth.sin(angle) + (point[1] - origin[1]) * mth.cos(angle)) + origin[1]

    point[0], point[1] = x, y

def keyEvent():
    global TRIANGLE_ORIGIN
    keys = pygame.key.get_pressed()

    if keys[pygame.K_q]:
        sys.exit()

    if keys[pygame.K_SPACE]:
        global ball_velocity_two
        ball_velocity_two -= GRAVITY

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
        
    if keys[pygame.K_l]:
        triangle_angle = -ROTATION_SPEED*0.03
        for point in SMALL_TRIANGLE:
            rotate(triangle_angle, point, origin=TRIANGLE_ORIGIN)
     
    if keys[pygame.K_n]:
        TRIANGLE_ORIGIN = [rd.randint(110, 250), rd.randint(125, 250)]



while running:

    random_r = rd.randint(1, 255)
    random_g = rd.randint(1, 255)
    random_b = rd.randint(1, 255)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # Draw random pixels if left mouse pressed
    if pygame.mouse.get_pressed()[0] == True:
        mousePixel_X = rd.randint(0, SCREEN_WIDTH - 1)
        mousePixel_Y = rd.randint(0, SCREEN_HEIGHT - 1)

    # Draw pixels based on mouse position
    else:
    	mousePixel_X, mousePixel_Y = pygame.mouse.get_pos()


    # This draws the pixels color
    random_color = (
        rd.randint(0, 255),
        rd.randint(0, 255),
        rd.randint(0, 255),
    )

    pixel_surface.set_at((mousePixel_X, mousePixel_Y), random_color)

    screen.blit(pixel_surface, (0, 0))

    # The two rectangles
    pygame.draw.rect(screen, RECT_COLOR, (*RECT_POS, *RECT_SIZE))
    pygame.draw.rect(screen, TARGET_COLOR, target_rect)

    # Circle 1
    pygame.draw.circle(
        screen,
        (random_r, random_g, random_b),
        ball_one,
        BALL_RADIUS,
    )

    # Ball physics

    # ball_velocity_one += GRAVITY
    # ball_one.y += ball_velocity_one

    ball_velocity_two += GRAVITY
    ball_two.y += ball_velocity_two

    # if ball_one.y + BALL_RADIUS >= SCREEN_HEIGHT:
    #     ball_one.y = SCREEN_HEIGHT - BALL_RADIUS
    #     ball_velocity_one *= BOUNCE

    if ball_two.y + BALL_RADIUS >= SCREEN_HEIGHT:
        ball_two.y = SCREEN_HEIGHT - BALL_RADIUS
        ball_velocity_two *= BOUNCE

    # distance = mth.sqrt((ball_two.x - ball_one.x)**2 + (ball_two.y - ball_one.y)**2)
    distance = (ball_two.x - ball_one.x) ** 2 + (ball_two.y - ball_one.y) ** 2

    # print(distance)

    distanceToMove = BALL_RADIUS * 2 - mth.sqrt(distance)
    # print(distanceToMove)

    angle = mth.atan2(ball_two.y - ball_one.y, ball_two.x - ball_one.x)

    """
    if distance <= (BALL_RADIUS*2)**2:
        print("COLLISION") #detecting collision
        ball_two.x += mth.cos(angle) * distanceToMove
        ball_two.y += mth.sin(angle) * distanceToMove
    """
    if not (distanceToMove < 0):
        # print("COLLISION")
        ball_two.x += mth.cos(angle) * distanceToMove
        ball_two.y += mth.sin(angle) * distanceToMove

    # Circle 2
    pygame.draw.circle(
        screen,
        (255, 250, 50),
        (ball_two.x, int(ball_two.y)),
        BALL_RADIUS,
    )

    keyEvent()
    erase_pixels_under_ball(pixel_surface, ball_two, BALL_RADIUS, BG_COLOR)
    erase_pixels_under_ball(pixel_surface, ball_one, BALL_RADIUS, BG_COLOR)

    ball_one.x = max(BALL_RADIUS, min(SCREEN_WIDTH - BALL_RADIUS, ball_one.x))
    ball_one.y = max(BALL_RADIUS, min(SCREEN_HEIGHT - BALL_RADIUS, ball_one.y))
    ball_two.x = max(BALL_RADIUS, min(SCREEN_WIDTH - BALL_RADIUS, ball_two.x))
    ball_two.y = max(BALL_RADIUS, min(SCREEN_HEIGHT - BALL_RADIUS, ball_two.y))

    #is_colliding = circleRectCollide(ball_one, BALL_RADIUS, target_rect)
    is_colliding_one, distance, normal = circleRectCollide(ball_one, BALL_RADIUS, target_rect)
    is_colliding_two, distance2, normal2 = circleRectCollide(ball_two, BALL_RADIUS, target_rect)
    #print(is_colliding)




    if is_colliding_one:
        penetration = BALL_RADIUS - distance
        ball_one += normal * penetration

    if is_colliding_two:
        penetration_2 = BALL_RADIUS - distance2
        ball_two += normal2 * penetration_2



    pygame.draw.polygon(screen, (0, 255, 255), SMALL_TRIANGLE)
    erase_pixels_under_triangle(pixel_surface, SMALL_TRIANGLE, BG_COLOR)



    pygame.display.flip()

    dt = clock.tick(FPS) / 1000

pygame.quit()
sys.exit()

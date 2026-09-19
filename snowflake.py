import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math as mth



pg.init()

window_size = (800, 400)


screen = pg.display.set_mode(window_size, DOUBLEBUF | OPENGL)
pg.display.set_caption("Snowflake")



# Define the area of the window that OpenGL can draw into
glViewport(0, 0, window_size[0], window_size[1])

# Set up the projection: how your coordinates map to the screen
glMatrixMode(GL_PROJECTION)
glLoadIdentity()

glOrtho(
    -1.0, 1.0,    # left, right
    -0.5, 0.5,    # bottom, top
    -1.0, 1.0     # near, far
)

# Set up object/camera transformations
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()



def drawLine(a, b, c):
    glBegin(GL_LINES)
    glColor3f(*c)
    glVertex2fv(a)
    glVertex2fv(b)
    glEnd()


def kockSnowflake(p1, p2, depth=1):

    if depth > 0:

        q1_x, q1_y = (2*p1[0] + p2[0]) / 3,  (2*p1[1] + p2[1]) / 3
        q2_x, q2_y = (2*p2[0] + p1[0]) / 3,  (2*p2[1] + p1[1]) / 3
    
        dy = p2[1] - p1[1]
        dx = p2[0] - p1[0]

        L = mth.sqrt(dx**2 + dy**2) / 3

        theta = mth.atan2(dy, dx)

        angle = theta + mth.pi / 3

        x_peak = q1_x + L * mth.cos(angle)
        y_peak = q1_y + L * mth.sin(angle)

        q1 = (q1_x, q1_y)
        q2 = (q2_x, q2_y)

        peak = (x_peak, y_peak)


        kockSnowflake(p1, q1, depth - 1)
        kockSnowflake(q1, peak, depth - 1)
        kockSnowflake(peak, q2, depth - 1)
        kockSnowflake(q2, p2, depth - 1)

    else:
        drawLine(p1, p2, (1.0, 0.0, 0.0))

    #print("I guess it mean I stop here or reached the depth ")
clock = pg.time.Clock()
timeElapsed = 0.0
depth = 4

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()


    glClearColor(0.10, 0.15, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    current_depth = int((timeElapsed / 1000) % depth) + 1
    kockSnowflake((-0.5, 0.0), (0.5, 0.0), current_depth)

    pg.display.flip()  
    dt = clock.tick(60)/8
    timeElapsed += dt





import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *



pg.init()

window_size = (1080, 720)


screen = pg.display.set_mode(window_size, DOUBLEBUF | OPENGL)
pg.display.set_caption("Triangle")


def triangleDraw(a, b, c, d):
    glBegin(GL_TRIANGLES)
    glColor3f(*d)
    glVertex2fv(a)
    glVertex2fv(b)
    glVertex2fv(c)
    glEnd()


def recursiveTriangle(a, b, c, depth):
    vertex0 = [0, 0]
    vertex1 = [0, 0]
    vertex2 = [0, 0]
    j = 0
    if depth > 0:
        while(j < 2):
            vertex0[j] = (a[j] + b[j]) / 2
            vertex1[j] = (a[j] + c[j]) / 2 
            vertex2[j] = (b[j] + c[j]) / 2
            j += 1
        recursiveTriangle(a, vertex0, vertex1, depth - 1)
        recursiveTriangle(b, vertex2, vertex0, depth - 1)
        recursiveTriangle(c, vertex1, vertex2, depth - 1)
    else:
        triangleDraw(a, b, c, (1.0, 0.0, 0.0))


clock = pg.time.Clock()
timeElapsed = 0.0
depth = 4
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()


    #glClearColor(0.10, 0.15, 0.0, 1.0)
    glClearColor(0, 0, 0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    current_depth = int((timeElapsed / 1000) % depth) + 1
    recursiveTriangle((0.0, 0.5), (0.5, -0.5), (-0.5, -0.5), current_depth)

    

    #triangleDraw((0.0, 0.5), (0.5, -0.5), (-0.5, -0.5), (1.0, 0.5, 0.25))
    #triangleDraw((-0.25, 0), (0.25, 0), (0, -0.5),(0.6, 0.25, 0.111))

    pg.display.flip()
    dt = clock.tick(60)/8
    timeElapsed += dt





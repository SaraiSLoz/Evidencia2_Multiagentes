import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
import math
from OpenGL.GLU import gluPerspective

def draw_cylinder(radius, height, sides):
    angle = (2.0 * math.pi) / sides

    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0.0, 0.0, height)  # Vértice superior del cilindro
    for i in range(sides + 1):
        x = radius * math.cos(i * angle)
        y = radius * math.sin(i * angle)
        glVertex3f(x, y, 0.0)
    glEnd()

    glBegin(GL_QUAD_STRIP)
    for i in range(sides + 1):
        x = radius * math.cos(i * angle)
        y = radius * math.sin(i * angle)
        glVertex3f(x, y, 0.0)
        glVertex3f(x, y, height)
    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glColor3f(1, 0, 0)  # Color del cilindro (rojo en este caso)
        draw_cylinder(1, 3, 20)  # Llama a la función para dibujar el cilindro
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()

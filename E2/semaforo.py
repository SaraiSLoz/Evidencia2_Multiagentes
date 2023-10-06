import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
import math

class Semaforo:
    def __init__(self, x, y, z, radius, height, sides):
        self.x = x  # Coordenada x
        self.y = y  # Coordenada y
        self.z = z  # Coordenada z
        self.radius = radius
        self.height = height
        self.sides = sides

    def half_cylinder(self, radius, height, sides):
        angle = (2.0 * math.pi) / sides

        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(0.0, 0.0, height)  # Vértice superior del cilindro
        lados = int((sides + 1) * 0.6)
        for i in range(lados):
            x = radius * math.cos(i * angle)
            y = radius * math.sin(i * angle)
            glVertex3f(x, y, 0.0)
        glEnd()

        glBegin(GL_QUAD_STRIP)
        for i in range(lados):
            x = radius * math.cos(i * angle)
            y = radius * math.sin(i * angle)
            glVertex3f(x, y, 0.0)
            glVertex3f(x, y, height)
        glEnd()

    def cylinder(self, radius, height, sides):
        angle = (2.0 * math.pi) / sides

        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(0.0, 0.0, height)  # Vértice superior del cilindro
        lados = int(sides + 1)
        for i in range(lados):
            x = radius * math.cos(i * angle)
            y = radius * math.sin(i * angle)
            glVertex3f(x, y, 0.0)
        glEnd()

        glBegin(GL_QUAD_STRIP)
        for i in range(lados):
            x = radius * math.cos(i * angle)
            y = radius * math.sin(i * angle)
            glVertex3f(x, y, 0.0)
            glVertex3f(x, y, height)
        glEnd()

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)  # Translada el semáforo a las coordenadas especificadas
        glColor3f(0.5, 0.5, 0.5)
        glRotate(-90, 1, 0, 0)
        self.half_cylinder(self.radius, self.height + 5, self.sides)  # Llama a la función para dibujar la parte superior
        glColor3f(0, 0.5, 0)
        self.cylinder(self.radius * 0.75, self.height, self.sides)  # Llama a la función para dibujar el poste
        glPopMatrix()

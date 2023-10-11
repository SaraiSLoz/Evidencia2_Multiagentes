import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
import math

class Arbol:
    def __init__(self, x, y, z, r, h):
        self.x = x  # Coordenada x
        self.y = y  # Coordenada y
        self.z = z  # Coordenada z (altura)
        self.radius = r
        self.height = h

    def draw(self):
        glPushMatrix()
        glTranslate(self.x, self.y, self.z)  # Translada el árbol a las coordenadas especificadas
        glRotatef(-90, 1, 0, 0)
        glColor3f(0, 0.5, 0)  # Color verde para el tronco

        # Dibuja el tronco del árbol (un cono personalizado)
        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(0, 0, 0)  # Vértice en la base del cono
        for i in range(360):
            x1 = self.radius * math.sin(math.radians(i))
            y1 = self.radius * math.cos(math.radians(i))
            glVertex3f(x1, y1, 0)  # Vértices de la base del cono
        glEnd()

        glBegin(GL_TRIANGLES)
        for i in range(360):
            x1 = self.radius * math.sin(math.radians(i))
            y1 = self.radius * math.cos(math.radians(i))
            x2 = self.radius * math.sin(math.radians(i + 1))
            y2 = self.radius * math.cos(math.radians(i + 1))

            # Vértices de los lados del cono
            glVertex3f(x1, y1, 0)
            glVertex3f(x2, y2, 0)
            glVertex3f(0, 0, self.height)  # Vértices de la punta del cono
        glEnd()

        glPopMatrix()

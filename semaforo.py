import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
import math

class Semaforo:
    def __init__(self, x, y, z, radius, height, sides, color):
        self.x = x  # Coordenada x
        self.y = y  # Coordenada y
        self.z = z  # Coordenada z
        self.color = color
        self.radius = radius
        self.height = height
        self.sides = sides
        


    def update(self, color):
            self.color = color
        
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

        
    def configure_material(self):
            if self.color == "Red":
                glColor3f(1.0, 0.0, 0.0)  # Rojo
                glMaterialfv(GL_FRONT, GL_DIFFUSE, (1.0, 0.0, 0.0, 1.0))
            elif self.color == "Yellow":
                glColor3f(1.0, 1.0, 0.0)  # Amarillo
                glMaterialfv(GL_FRONT, GL_DIFFUSE, (1.0, 1.0, 0.0, 1.0))
            elif self.color == "Green":
                glColor3f(0.0, 1.0, 0.0)  # Verde
                glMaterialfv(GL_FRONT, GL_DIFFUSE, (0.0, 1.0, 0.0, 1.0))

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glRotate(-90, 1, 0, 0)
        self.configure_material()
        self.half_cylinder(self.radius, self.height + 5, self.sides)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
        self.cylinder(self.radius * 0.75, self.height, self.sides)
        glPopMatrix()
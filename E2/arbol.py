import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
import math
from objloader import OBJ


class Arbol:
    def __init__(self, obj_filename, x, y, z):
        self.obj = OBJ(obj_filename, swapyz=True)
        self.Position = [x, y, z]

    def draw(self):
        glPushMatrix()

        # Aplica la rotación alrededor del eje Y
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        # Rota alrededor del eje Y    math.degrees(angle)
        glRotatef(0, 0, 1, 0)
        glScaled(1.5, 1.5, 1.5)  # Escala el carro (ajusta según sea necesario)

        # Renderiza el objeto .obj del carro
        self.obj.render()

        glPopMatrix()

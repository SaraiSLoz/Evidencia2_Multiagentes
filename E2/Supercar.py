import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import math
from objloader import OBJ

class Car:
    def __init__(self, obj_filename, dim, vel):
        self.obj = OBJ(obj_filename, swapyz=True)
        self.DimBoard = dim
        self.Position = [random.uniform(-dim, dim), 20, random.uniform(-dim, dim)]
        self.Direction = [random.uniform(-1, 1), 0, random.uniform(-1, 1)]
        self.normalize(self.Direction)
        self.scale(self.Direction, vel)

    def update(self):
        new_position = [self.Position[0] + self.Direction[0], self.Position[1], self.Position[2] + self.Direction[2]]

        # Verifica si la nueva posición está dentro del borde del plano
        if -self.DimBoard < new_position[0] < self.DimBoard and -self.DimBoard < new_position[2] < self.DimBoard:
            self.Position = new_position
        else:
            # El carro ha colisionado con el borde del plano, cambia de dirección en un ángulo de 90 grados
            # Calcula la nueva dirección en función de la dirección actual
            temp_x = self.Direction[0]
            self.Direction[0] = -self.Direction[2]
            self.Direction[2] = temp_x

    def draw(self):
        glPushMatrix()

        # Calcula el ángulo de rotación en radianes basado en la dirección de movimiento
        angle = math.atan2(self.Direction[2], self.Direction[0])

        # Aplica la rotación alrededor del eje Y
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        glRotatef(0, 0, 1, 0)  # Rota alrededor del eje Y    math.degrees(angle)
        glScaled(7, 7, 7)  # Escala el carro (ajusta según sea necesario)

        # Renderiza el objeto .obj del carro
        self.obj.render()

        glPopMatrix()


    def normalize(self, v):
        length = math.sqrt(v[0] ** 2 + v[2] ** 2)
        if length != 0:
            v[0] /= length
            v[2] /= length

    def scale(self, v, s):
        v[0] *= s
        v[2] *= s
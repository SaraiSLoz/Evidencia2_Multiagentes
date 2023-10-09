import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import math
from objloader import OBJ

class Car:
    def __init__(self, obj_filename, posx,posz, vel):
        self.obj = OBJ(obj_filename, swapyz=True)
        self.Position = [posx, 20, posz]

    def update(self,x,z):
        new_pos = [x,20,z]
        self.Position = new_pos

    def draw(self):
        glPushMatrix()

        # Calcula el ángulo de rotación en radianes basado en la dirección de movimiento


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

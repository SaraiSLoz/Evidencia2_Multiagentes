import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import math
from objloader import OBJ

class Car:
    def __init__(self, obj_filename, posx, posz, vel, color):
        self.obj = OBJ(obj_filename, swapyz=True)
        self.Position = [posx, 20, posz]
        self.color = color
        self.rotation_angle = 0.0  # Ángulo de rotación inicial

    def update(self, x, z, color):
        new_pos = [x, 5, z]
        self.Position = new_pos
        self.color = color
        
  
    def draw(self):
        glPushMatrix()
        # Aplica la rotación alrededor del eje Y
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        #glRotatef(0, 0, 1, 0)  # Rota alrededor del eje Y    math.degrees(angle)
        glScaled(7, 7, 7)  # Escala el carro (ajusta según sea necesario)
        # Aplica la rotación alrededor del eje Y basada en el color
        
        if self.color == "Blue" or self.color == "Black":
            glRotatef(-90.0, 0, 1, 0)  # Girar 90 grados hacia la izquierda
        
        elif self.color == "Purple" or self.color == "Gray":
            glRotatef(90.0, 0, 1, 0)  

        

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

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import math
from arbol import Arbol
from Supercar import Car
from semaforo import Semaforo
from edificio import Edificio
from faroles import Farol
# Variables del juego
screen_width = 500
screen_height = 500
FOVY = 60.0
ZNEAR = 0.01
ZFAR = 900.0
EYE_X = 300.0
EYE_Y = 200.0
EYE_Z = 300.0
CENTER_X = 0
CENTER_Y = 0
CENTER_Z = 0
UP_X = 0
UP_Y = 1
UP_Z = 0
X_MIN = -500
X_MAX = 500
Y_MIN = -500
Y_MAX = 500
Z_MIN = -500
Z_MAX = 500
DimBoard = 200
plane_x = 0
plane_z = 0
plane_speed = 5 

pygame.init()
Cars = []
nCars = 5
Arboles = []
narbol = 6
Semaforos = []
nsemaforos = 3
Edificios = []
nedificio = 1
Faroles = []
nfaroles = 3
def Axis():
    glShadeModel(GL_FLAT)
    glLineWidth(3.0)
    glColor3f(1.0, 0.0, 0.0)  # X axis in red
    glBegin(GL_LINES)
    glVertex3f(X_MIN, 0.0, 0.0)
    glVertex3f(X_MAX, 0.0, 0.0)
    glEnd()

    glColor3f(0.0, 1.0, 0.0)  # Y axis in green
    glBegin(GL_LINES)
    glVertex3f(0.0, Y_MIN, 0.0)
    glVertex3f(0.0, Y_MAX, 0.0)
    glEnd()

    glColor3f(0.0, 0.0, 1.0)  # Z axis in blue
    glBegin(GL_LINES)
    glVertex3f(0.0, 0.0, Z_MIN)
    glVertex3f(0.0, 0.0, Z_MAX)
    glEnd()

    glLineWidth(1.0)

def Init():
    screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL: Cars")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, screen_width / screen_height, ZNEAR, ZFAR)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)
    glClearColor(0, 0, 0, 0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    x1 = -200
    z1 = 0
    for i in range(narbol):
        Arboles.append(Arbol(x1,0,z1,10,40))
        x1 += 30
    x2 = 30
    z2 = 0
    for i in range(narbol):
        Arboles.append(Arbol(x2,0,z2,10,40))
        x2 += 30
    Semaforos.append(Semaforo(15.8,0,-2.6,5.0, 50.0, 20))
    Semaforos.append(Semaforo(13.6,0,6.5,5.0, 50.0, 20))
    Semaforos.append(Semaforo(26.5,0,7,5.0, 50.0, 20))
    
    Edificios.append(Edificio("house/Tower-HouseDesign.obj",0,0,230))
    Edificios.append(Edificio("house/Tower-HouseDesign.obj",0,0,-230))
    Edificios.append(Edificio("house/Tower-HouseDesign.obj",100,0,-230))
    Edificios.append(Edificio("house/Tower-HouseDesign.obj",-100,0,-230))
    
    Faroles.append(Farol("Streetlight_LowRes.obj",30,0,20))
    Faroles.append(Farol("Streetlight_LowRes.obj",60,0,20))
    Faroles.append(Farol("Streetlight_LowRes.obj",-30,0,20))
    Faroles.append(Farol("Streetlight_LowRes.obj",-60,0,20))
    
    #Streetlight_LowRes
    for i in range(nCars):
        Cars.append(Car("Car.obj", DimBoard, 1.0))  # Reemplaza "Car.obj" con la ruta de tu archivo .obj

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Axis()

    # Cambia el color del plano a gris claro
    glColor3f(0.9, 0.9, 0.9)  # Gris claro

    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)  # Coordenadas de textura para el vértice 1
    glVertex3d(-DimBoard, 0, -DimBoard)

    glTexCoord2f(1, 0)  # Coordenadas de textura para el vértice 2
    glVertex3d(-DimBoard, 0, DimBoard)

    glTexCoord2f(1, 1)  # Coordenadas de textura para el vértice 3
    glVertex3d(DimBoard, 0, DimBoard)

    glTexCoord2f(0, 1)  # Coordenadas de textura para el vértice 4
    glVertex3d(DimBoard, 0, -DimBoard)
    glEnd()

    glDisable(GL_TEXTURE_2D)  # Deshabilita la textura
    for semaforo in Semaforos:
        semaforo.draw()
    for arbol in Arboles:
        arbol.draw()
    for edificio in Edificios:
        edificio.draw()
    for faroles in Faroles:
        faroles.draw()
    for car in Cars:
        car.draw()
        car.update()
    

def main():
    global EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z
    angle = math.radians(45)  # Inicializamos el ángulo de rotación a 45 grados en radianes

    radius = 400  # Radio para la rotación
    Init()
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    EYE_Y += plane_speed
                    CENTER_Y += plane_speed
                elif event.key == pygame.K_s:
                    EYE_Y -= plane_speed
                    CENTER_Y -= plane_speed
                elif event.key == pygame.K_a:
                    angle += plane_speed / 10  # Aumentar el ángulo de rotación
                elif event.key == pygame.K_d:
                    angle -= plane_speed / 40  # Disminuir el ángulo de rotación

        # Calculamos las nuevas coordenadas de la cámara
        EYE_X = CENTER_X + radius * math.cos(angle)
        EYE_Z = CENTER_Z + radius * math.sin(angle)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)

        display()

        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()
if __name__ == "__main__":
    main()

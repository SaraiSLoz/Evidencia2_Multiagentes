import requests
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
from Textures import Texture
# Variables del juego

URL_BASE = "http://127.0.0.1:5000"
r = requests.post(URL_BASE + "/games", allow_redirects=False)
LOCATION = r.headers["Location"]
lista = r.json()
print(lista)
factor = 20
screen_width = 900
screen_height = 900
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
DimBoard = 280
plane_x = 0
plane_z = 0
plane_speed = 5

pygame.init()
Cars = {}
nCars = 5
Arboles = []
narbol = 8
Semaforos = {}
nsemaforos = 3
Edificios = []
nedificio = 1
Faroles = []
nfaroles = 3
textures = []


def add_cars(id_car, x, y, color):
    car = Car("Car.obj", x, y, 1.0, color)
    Cars[id_car] = car


def delete_cars(car_id):
    if car_id in Cars:
        del Cars[car_id]


# def Axis():
#     glShadeModel(GL_FLAT)
#     glLineWidth(3.0)
#     glColor3f(1.0, 0.0, 0.0)  # X axis in red
#     glBegin(GL_LINES)
#     glVertex3f(X_MIN, 0.0, 0.0)
#     glVertex3f(X_MAX, 0.0, 0.0)
#     glEnd()

#     glColor3f(0.0, 1.0, 0.0)  # Y axis in green
#     glBegin(GL_LINES)
#     glVertex3f(0.0, Y_MIN, 0.0)
#     glVertex3f(0.0, Y_MAX, 0.0)
#     glEnd()

#     glColor3f(0.0, 0.0, 1.0)  # Z axis in blue
#     glBegin(GL_LINES)
#     glVertex3f(0.0, 0.0, Z_MIN)
#     glVertex3f(0.0, 0.0, Z_MAX)
#     glEnd()

#     glLineWidth(1.0)


def Init():
    screen = pygame.display.set_mode(
        (screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL: Cars")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, screen_width / screen_height, ZNEAR, ZFAR)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X,
              CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)
    glClearColor(0, 0, 0, 0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    x1 = -200
    z1 = 0

    tree_coordinates = [
        (-200, 0, 200),
        (-150, 0, 200),
        (-100, 0, 200),
        (-50, 0, 200),
        (-200, 0, 160),
        (-150, 0, 160),
        (-100, 0, 160),
        (-50, 0, 160),
        (-200, 0, 120),
        (-150, 0, 120),
        (-100, 0, 120),
        (-50, 0, 120),
        (-200, 0, 80),
        (-150, 0, 80),
        (-100, 0, 80),
        (-50, 0, 80)
    ]

    # Agregar los árboles usando las coordenadas especificadas
    for coords in tree_coordinates:
        Arboles.append(
            Arbol(*coords, 8, 35))
    for agent in lista[1]:
        Semaforos[agent["id"]] = Semaforo(
            agent["x"]*15-190, 0, agent["z"]*50-260, 5.0, 50.0, 20, agent.get("color"))
    for agent in lista[0]:
        car = Car("Car.obj", agent["x"], agent["z"], 1.0, agent.get("color"))
        Cars[agent["id"]] = car

      # Definir y cargar las texturas
    textures.append(Texture("pasto.bmp"))
    textures.append(Texture("textura2.bmp"))
    textures.append(Texture("textura22.bmp"))
    textures.append(Texture("calle.bmp"))
    textures.append(Texture("nubes.bmp"))

    Edificios.append(Edificio("house/Tower-HouseDesign.obj", 30, 8, 230))
    Edificios.append(Edificio("house/Tower-HouseDesign.obj", 130, 8, 120))
    Edificios.append(Edificio("house/Tower-HouseDesign.obj", 160, 8, 120))
    Edificios.append(Edificio("house/Tower-HouseDesign.obj", 190, 8, 120))

    Faroles.append(Farol("Streetlight_LowRes.obj", 110, 4, -65))
    Faroles.append(Farol("Streetlight_LowRes.obj", 160, 4, -65))
    Faroles.append(Farol("Streetlight_LowRes.obj", 210, 4, -65))
    Faroles.append(Farol("Streetlight_LowRes.obj", 260, 4, -65))
    Faroles.append(Farol("Streetlight_LowRes.obj", -50, 4, -65))
    Faroles.append(Farol("Streetlight_LowRes.obj", -100, 4, -65))
    Faroles.append(Farol("Streetlight_LowRes.obj", -150, 4, -65))
    Faroles.append(Farol("Streetlight_LowRes.obj", -200, 4, -65))

    # Streetlight_LowRes


def display():

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # Axis()
    glClearColor(0.529, 0.807, 0.92, 0)  # RGB para azul cielo

    # Enable texture
    glEnable(GL_TEXTURE_2D)

    # Render the ground plane with grass texture
    # Assuming textures[0] is the grass texture
    glBindTexture(GL_TEXTURE_2D, textures[0].id)

    glMaterialfv(GL_FRONT, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))

    glColor(1, 1, 1)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3d(-DimBoard, 0, -DimBoard)

    glTexCoord2f(0, 1)
    glVertex3d(-DimBoard, 0, DimBoard)

    glTexCoord2f(1, 1)
    glVertex3d(DimBoard, 0, DimBoard)

    glTexCoord2f(1, 0)
    glVertex3d(DimBoard, 0, -DimBoard)
    glEnd()

    # Render a section of the ground plane with road texture (slightly elevated)
    # Assuming textures[1] is the road texture
    glBindTexture(GL_TEXTURE_2D, textures[2].id)
    glColor(1, 1, 1)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    # Adjust the y-coordinate to elevate the road
    glVertex3d(0, 1, -80)
    glTexCoord2f(0, 1)
    glVertex3d(0, 1, 200)
    glTexCoord2f(1, 1)
    glVertex3d(55, 1, 200)
    glTexCoord2f(1, 0)
    glVertex3d(55, 1, -80)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, textures[1].id)
    glColor(1, 1, 1)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    # Adjust the y-coordinate to elevate the road
    glVertex3d(-DimBoard, 2, -50)
    glTexCoord2f(0, 1)
    glVertex3d(-DimBoard, 2, 50)
    glTexCoord2f(1, 1)
    glVertex3d(DimBoard, 2, 50)
    glTexCoord2f(1, 0)
    glVertex3d(DimBoard, 2, -50)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, textures[1].id)
    glColor(1, 1, 1)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    # Adjust the y-coordinate to elevate the road
    glVertex3d(-DimBoard, 1, -180)
    glTexCoord2f(0, 1)
    glVertex3d(-DimBoard, 1, -80)
    glTexCoord2f(1, 1)
    glVertex3d(DimBoard, 1, -80)
    glTexCoord2f(1, 0)
    glVertex3d(DimBoard, 1, -180)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, textures[3].id)
    glColor(1, 1, 1)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glEnd()
    # glBindTexture(GL_TEXTURE_2D, textures[1].id)
    # glColor(1, 1, 1)
    # glBegin(GL_QUADS)
    # glTexCoord2f(0, 0)
    # # Adjust the y-coordinate to elevate the road
    # glVertex3d(0, 1, 0)
    # glTexCoord2f(0, 1)
    # glVertex3d(-10, 1, 70)
    # glTexCoord2f(1, 1)
    # glVertex3d(0, 1, 0)
    # glTexCoord2f(1, 0)
    # glVertex3d(10, 1, -70)
    # glEnd()

    glDisable(GL_TEXTURE_2D)  # Disable texture for other objects

    # Render the buildings (without texture, using gray color)
    glColor(0.5, 0.5, 0.5)  # Set gray color for buildings

    light_position = (0.0, 0.0, 50.0, 1.0)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    for semaforo in Semaforos.values():
        semaforo.draw()

    for edificio in Edificios:
        edificio.draw()

    # Render other objects (trees, streetlights, cars)
    for arbol in Arboles:
        glColor(1, 1, 1)  # Set white color for other objects
        arbol.draw()
    for faroles in Faroles:
        faroles.draw()
    response = requests.get(URL_BASE + LOCATION)
    lista = response.json()

    for Car in Cars.values():
        Car.draw()

    car_agents = lista[0]

    for agent in car_agents:
        car_id = agent["id"]
        car_color = agent.get("color")

        if car_id in Cars:
            Cars[car_id].update(agent["x"]*15-190,
                                agent["z"]*50-260, car_color)
        elif car_color != "Orange":
            delete_cars(car_id)
        else:
            add_cars(car_id, agent["x"], agent["z"], agent.get("color"))

    for agent in lista[1]:
        semaforo_id = agent["id"]

        if semaforo_id in Semaforos:
            Semaforos[semaforo_id].update(agent.get("color"))
        else:
            continue


def main():
    global EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z
    # Inicializamos el ángulo de rotación a 45 grados en radianes
    angle = math.radians(45)

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
        gluLookAt(EYE_X, EYE_Y, EYE_Z, CENTER_X,
                  CENTER_Y, CENTER_Z, UP_X, UP_Y, UP_Z)

        display()

        pygame.display.flip()
        pygame.time.wait(100)
    pygame.quit()


if __name__ == "__main__":
    main()

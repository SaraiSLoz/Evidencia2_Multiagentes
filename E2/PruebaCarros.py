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

    for agent in lista[1]:
        Semaforos[agent["id"]] = Semaforo(
            agent["x"]*15-190, 0, agent["z"]*50-260, 5.0, 50.0, 20, agent.get("color"))
    for agent in lista[0]:
        car = Car("Car.obj",
                  agent["x"], agent["z"], 1.0, agent.get("color"))
        Cars[agent["id"]] = car

      # Definir y cargar las texturas
    textures.append(Texture("piso.bmp"))
    textures.append(Texture("textura2.bmp"))
    textures.append(Texture("textura22.bmp"))
    textures.append(Texture("calle.bmp"))
    textures.append(Texture("nubes.bmp"))

    Edificios.append(Edificio("house/Tower-HouseDesign.obj", 30, 8, 230))
    Edificios.append(Edificio("house/Tower-HouseDesign.obj", 130, 8, 120))
    Edificios.append(Edificio("house/Tower-HouseDesign.obj", 160, 8, 120))
    Edificios.append(Edificio("house/Tower-HouseDesign.obj", 190, 8, 120))
    Edificios.append(Edificio("house/Tower-HouseDesign.obj", -190, 8, -220))
    Edificios.append(Edificio("house/Tower-HouseDesign.obj", -130, 8, -220))
    Edificios.append(Edificio("house/Tower-HouseDesign.obj", -70, 8, -220))
    Edificios.append(Edificio("house/Tower-HouseDesign.obj", -10, 8, -220))

    Edificios.append(Edificio("house/Tower-HouseDesign.obj", 50, 8, -220))
    Edificios.append(Edificio("house/Tower-HouseDesign.obj", 110, 8, -220))
    Edificios.append(Edificio("house/Tower-HouseDesign.obj", 170, 8, -220))

    Faroles.append(Farol("Streetlight_LowRes.obj", 110, 4, -65))
    Faroles.append(Farol("Streetlight_LowRes.obj", 160, 4, -65))
    Faroles.append(Farol("Streetlight_LowRes.obj", 210, 4, -65))
    Faroles.append(Farol("Streetlight_LowRes.obj", 260, 4, -65))
    Faroles.append(Farol("Streetlight_LowRes.obj", -50, 4, -65))
    Faroles.append(Farol("Streetlight_LowRes.obj", -100, 4, -65))
    Faroles.append(Farol("Streetlight_LowRes.obj", -150, 4, -65))
    Faroles.append(Farol("Streetlight_LowRes.obj", -200, 4, -65))

    Arboles.append(Arbol("ChristmasTree.obj", -200, 4, 200))
    Arboles.append(Arbol("ChristmasTree.obj", -150, 4, 200))
    Arboles.append(Arbol("ChristmasTree.obj", -100, 4, 200))
    Arboles.append(Arbol("ChristmasTree.obj", -50, 4, 200))
    Arboles.append(Arbol("ChristmasTree.obj", -200, 4, 160))
    Arboles.append(Arbol("ChristmasTree.obj", -150, 4, 160))
    Arboles.append(Arbol("ChristmasTree.obj", -100, 4, 160))
    Arboles.append(Arbol("ChristmasTree.obj", -50, 4, 160))
    Arboles.append(Arbol("ChristmasTree.obj", -200, 4, 120))
    Arboles.append(Arbol("ChristmasTree.obj", -150, 4, 120))
    Arboles.append(Arbol("ChristmasTree.obj", -100, 4, 120))
    Arboles.append(Arbol("ChristmasTree.obj", -50, 4, 120))
    Arboles.append(Arbol("ChristmasTree.obj", -200, 4, 80))
    Arboles.append(Arbol("ChristmasTree.obj", -150, 4, 80))
    Arboles.append(Arbol("ChristmasTree.obj", -100, 4, 80))
    Arboles.append(Arbol("ChristmasTree.obj", -50, 4, 80))


def display():

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.529, 0.807, 0.92, 0)  # RGB para azul cielo

    glEnable(GL_TEXTURE_2D)

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

    glBindTexture(GL_TEXTURE_2D, textures[2].id)
    glColor(1, 1, 1)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
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

    glDisable(GL_TEXTURE_2D)
    glColor(0.5, 0.5, 0.5)

    light_position = (0.0, 0.0, 50.0, 1.0)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    for semaforo in Semaforos.values():
        semaforo.draw()

    for edificio in Edificios:
        edificio.draw()

    for arbol in Arboles:
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

    for agent in lista[1]:
        semaforo_id = agent["id"]

        if semaforo_id in Semaforos:
            Semaforos[semaforo_id].update(agent.get("color"))
        else:
            continue


def play_sound(sound_file):
    pygame.mixer.init()
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play(loops=10)


def main():
    global EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z
    # Inicializamos el ángulo de rotación a 45 grados en radianes
    angle = math.radians(45)
    play_sound("LightTrafficSoundEffect.mp3")

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

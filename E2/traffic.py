import numpy as np
import random
from mesa import Agent, Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation
from mesa.visualization.ModularVisualization import ModularServer
import time

from SimpleContinuousModule import SimpleCanvas



class Car(Agent):
    def __init__(self, model: Model, color, pos, speed, decision, choice):
        super().__init__(model.next_id(), model)  # Asigna un ID único automáticamente
        self.color = color
        self.pos = pos
        self.speed = speed
        self.decision = decision
        self.counter = 0
        self.eliminado = False  # Agregamos la bandera de eliminado
        self.choice = choice

    def step(self):
        new_pos = self.pos + \
            np.array([0.5 * self.speed[0], 0.5 * self.speed[1]])
        self.model.space.move_agent(self, new_pos)

    def update_choice(self, new):
        self.choice = new


class Circle(Agent):
    def __init__(self, unique_id, model, x, y, radius):
        super().__init__(unique_id, model)
        self.x = x
        self.y = y
        self.radius = radius
        color = "Green", "Yellow", "Red"
        self.color = color  # Inicialmente azul

    def change_color(self):
        # Cambia el color del círculo
        if self.color == "Green":
            self.color = "Yellow"
        elif self.color == "Yellow":
            self.color = "Red"
        elif self.color == "Red":
            self.color = "Green"

    def get_circle_portrayal(self):
        return {
            "Shape": "circle",
            "x": self.x / 25,  # Normalizar las posiciones
            "y": self.y / 10,
            "r": self.radius,
            "Filled": "true",
            "Color": self.color
        }


def car_draw(agent):
    color = agent.color
    w = 0.034
    h = 0.02
    if color == "Blue":
        w = 0.034
        h = 0.02
    elif color == "Black":
        w = 0.034
        h = 0.02
    elif color == "Purple":
        w = 0.034
        h = 0.02
    elif color == "Gray":
        w = 0.034
        h = 0.02
    elif color == "Green":
        w = 0.02
        h = 0.034
    elif color == "Orange":
        w = 0.02
        h = 0.034
    return {"Shape": "rect", "w": w, "h": h, "Filled": "true", "Color": color}


def maintain_distance_x(agent, blue_agents, desired_distance_x, current_position_x):
    for blue_agent in blue_agents:
        if blue_agent.pos[0] > current_position_x:
            distance_x = blue_agent.pos[0] - current_position_x
            if distance_x < desired_distance_x:
                agent.speed = np.array([0.0, 0.0])
                break
    else:
        agent.speed = np.array([1.0, 0.0])


def maintain_distance_x2(agent, purple_agents, desired_distance_x, current_position_x):
    for purple_agent in purple_agents:
        if purple_agent.pos[0] < current_position_x:
            distance = current_position_x - purple_agent.pos[0]
            if distance < desired_distance_x:
                agent.speed = np.array([0.0, 0.0])
                break
    else:
        agent.speed = np.array([-1.0, 0.0])


class Street(Model):
    def __init__(self):
        super().__init__()
        self.space = ContinuousSpace(25, 10, True)
        self.schedule = RandomActivation(self)
        # Inicializar el tiempo de último cambio
        self.last_color_change_time = time.time()
        self.step_count = 0  # Contador de pasos
        # Supongamos que la distancia de separación deseada es de 5 unidades
        distancia_separacion = 3

        # Generar 4 posiciones iniciales aleatorias con la distancia de separación deseada
        posiciones_iniciales_x = np.random.choice(
            np.arange(0, 26, distancia_separacion), 8, replace=False)
        # Todas las posiciones iniciales en y serán 2.5
        posiciones_iniciales_y = np.full(4, 2.5)
        cont = 0
        for px, py in zip(posiciones_iniciales_x, posiciones_iniciales_y):
            if cont <= 3:
                car = Car(self, "Purple", np.array([px, py]), np.array(
                    [-1.0, 0.0]), random.choice([1, 2,3, 4]), 1)
            else:
                car = Car(self, "Purple", np.array([px, py]), np.array(
                    [-1.0, 0.0]), random.choice([1, 2,3, 4]), 0)
            self.space.place_agent(car, car.pos)
            self.schedule.add(car)
            cont += 1
         # First horizontal line (moving left)
        cont = 0
        for px, py in zip(posiciones_iniciales_x, posiciones_iniciales_y):
            if cont <= 3:
                car = Car(self, "Gray", np.array([px, 3]), np.array(
                    [-1.0, 0.0]), random.choice([1, 2,3, 4]), 1)

            else:
                car = Car(self, "Gray", np.array([px, 3]), np.array(
                    [-1.0, 0.0]), random.choice([1, 2,3, 4]), 0)
            self.space.place_agent(car, car.pos)
            self.schedule.add(car)
            cont += 1

        cont = 0
        # Second horizontal line (moving right)
        for px, py in zip(posiciones_iniciales_x, posiciones_iniciales_y):
            if cont <= 3:
                car = Car(self, "Blue", np.array([px, 6]), np.array(
                    [1.0, 0.0]), random.choice([1, 2,3, 4]), 1)  # Change to move right

            else:
                car = Car(self, "Blue", np.array([px, 6]), np.array(
                    [1.0, 0.0]), random.choice([1, 2,3, 4]), 0)  # Change to move right

            self.space.place_agent(car, car.pos)
            self.schedule.add(car)
            cont += 1
        cont = 0
        for px, py in zip(posiciones_iniciales_x, posiciones_iniciales_y):
            if cont <= 3:
                car = Car(self, "Black", np.array([px, 5.5]), np.array(
                    [1.0, 0.0]), random.choice([1, 2,3, 4]), 1)  # Change to move right
            else:
                car = Car(self, "Black", np.array([px, 5.5]), np.array(
                    [1.0, 0.0]), random.choice([1, 2,3, 4]), 0)  # Change to move right
            self.space.place_agent(car, car.pos)
            self.schedule.add(car)
            cont += 1
        cont = 0
        # Vertical line (moving upwards and then to the left)
        # Generar 4 posiciones iniciales aleatorias con la distancia de separación deseada
        # posiciones_iniciales_x2 = np.random.choice(
        #     np.arange(0, 11, distancia_separacion2), 3, replace=False)
        # Todas las posiciones iniciales en x serán 2.5
        posiciones_iniciales_y2 = np.full(3, -1.5)
        # Corrected: Pass a single y-coordinate instead of a list
        for py in [-1, -1.5, -2]:
            if cont <= 2:
                car = Car(self, "Orange", np.array(
                    [15, py]), np.array([0.0, -1.0]), random.choice([1, 2, 3, 4]),  1)
            else:
                car = Car(self, "Orange", np.array(
                    [15, py]), np.array([0.0, -1.0]), random.choice([1, 2, 3, 4]), 0)
            self.space.place_agent(car, car.pos)
            self.schedule.add(car)
            cont += 1

        self.circles = [
            # primercirculo
            Circle(self.next_id(), self, 15.8, 1.6, 4),
            # segundocirculo
            Circle(self.next_id(), self, 13.2, 6.5, 4),
            # tercercirculo
            Circle(self.next_id(), self, 16.5, 7, 4)
        ]

        self.circles[0].color = "Green"
        self.circles[1].color = "Green"
        self.circles[2].color = "Red"

        self.last_color_change_steps = [0] * len(self.circles)
        self.color_change_steps = [[24, 8, 32], [24, 8, 32], [
            24, 8, 32]]  # Change intervals for each circle

        for circle in self.circles:
            self.space.place_agent(circle, (circle.x, circle.y))

    def reutilizar(self,agent,agentlist):
        if agent.pos[0] <= 5 and len(agentlist)>3:
            agent.color = "Orange"
            agent.pos[0] = 15
            agent.pos[1] = -1
            self.space.place_agent(agent, agent.pos)
    
    def reutilizar1(self,agent,agentlist):
        if agent.pos[0]>=20 and len(agentlist)>3:
            agent.color = "Orange"
            agent.pos[0] = 15
            agent.pos[1] = -1
            self.space.place_agent(agent, agent.pos)
                

    def step(self):
        self.step_count += 1  # Increment step count in each iteration
        semaforo1 = self.circles[0].color
        semaforo2 = self.circles[1].color
        semaforo3 = self.circles[2].color

        for i, circle in enumerate(self.circles):
            color_pattern = self.color_change_steps[i]
            color_index = 0

            if circle.get_circle_portrayal()["Color"] == "Yellow":
                color_index = 1
            elif circle.get_circle_portrayal()["Color"] == "Red":
                color_index = 2

            steps_passed = self.step_count - self.last_color_change_steps[i]
            current_interval = color_pattern[color_index]
            if steps_passed >= current_interval:
                circle.change_color()
                self.last_color_change_steps[i] = self.step_count

        for agent in self.schedule.agents:
            if agent.choice == 1:
                if agent.color == "Purple" or agent.color == "Gray":
                    purple_agents = [other_agent for other_agent in self.schedule.agents if
                                    other_agent.color == "Purple" and other_agent != agent]

                    gray_agents2 = [other_agent for other_agent in self.schedule.agents if
                                    other_agent.color == "Gray" and other_agent != agent]
                    # Coordenadas relevantes
                    current_position = agent.pos[0]
                    coordinateslow = 18.5
                    coordinatestop = 17
                    # Distancia a la que se desea mantener
                    desired_distance = 3.5
                    # Calcular la velocidad en función de la distancia al agente de adelante
                    if current_position == coordinatestop and semaforo1 == "Red":
                        # Detenerse en la coordenada  con semáforo en rojo
                        agent.speed = np.array([0.0, 0.0])
                        agent.counter = 0
                    elif current_position == coordinateslow and semaforo1 == "Yellow":
                        # Disminuir velocidad en la coordenada  con semáforo en amarillo
                        agent.speed = np.array([-0.5, 0.0])

                    else:
                        if agent.counter < 4:
                            # Incrementar el contador, pero no moverse
                            agent.counter += 1
                        else:
                            if(agent.color == "Purple"):
                                maintain_distance_x2(
                                    agent, purple_agents, desired_distance, current_position)
                            else:
                                maintain_distance_x2(
                                    agent, gray_agents2, desired_distance, current_position)
                    if agent.color == "Purple":
                        self.reutilizar(agent,purple_agents)
                    else:
                        self.reutilizar(agent,gray_agents2)
                elif agent.color == "Blue" or agent.color == "Black":
                    # Obtener todos los agentes azules
                    blue_agents = [other_agent for other_agent in self.schedule.agents if
                                other_agent.color == "Blue" and other_agent != agent]

                    blue_agents2 = [other_agent for other_agent in self.schedule.agents if
                                    other_agent.color == "Black" and other_agent != agent]

                    current_position = agent.pos[0]
                    coordinate_7_5 = 7.5
                    coordinate_12_5 = 12.5
                    desired_distance = 3.5

                    if current_position == coordinate_12_5 and semaforo2 == "Red":
                        agent.speed = np.array([0.0, 0.0])
                        agent.counter = 0

                    elif current_position == coordinate_7_5 and semaforo2 == "Yellow":
                        agent.speed = np.array([0.5, 0.0])

                    else:
                        if agent.counter < 4:
                            # Incrementar el contador, pero no moverse
                            agent.counter += 1

                        else:
                            # Calcular la velocidad para mantener la distancia
                            if(agent.color == "Blue"):
                                maintain_distance_x(
                                    agent, blue_agents, desired_distance, current_position)
                            else:
                                maintain_distance_x(
                                    agent, blue_agents2, desired_distance, current_position)
                    if agent.color == "Blue":
                        self.reutilizar1(agent,blue_agents)
                    else:
                        self.reutilizar1(agent,blue_agents2)
                elif agent.color == "Orange":
                    orange_agents = [other_agent for other_agent in self.schedule.agents if
                                    other_agent.color == "Orange" and other_agent != agent]

                    # Coordenadas relevantes
                    current_position = agent.pos[1]
                    coordinate_7_5 = 7.5
                    coordinate_7_2 = 7.2

                    desired_distance = 1

                    # Calcular la velocidad en función de la distancia al agente de adelante
                    if current_position == coordinate_7_5 and semaforo3 == "Red":
                        # Detenerse en la coordenada 12.5 con semáforo en rojo
                        agent.speed = np.array([0.0, 0.0])
                        agent.counter = 0
                    elif current_position == coordinate_7_2 and semaforo3 == "Yellow":
                        # Disminuir velocidad en la coordenada 7.5 con semáforo en amarillo
                        agent.speed = np.array([0.0, -0.5])
                    else:
                        # Calcular la velocidad para mantener la distancia
                        for orange_agent in orange_agents:
                            if orange_agent.pos[1] < current_position:
                                distance = current_position - orange_agent.pos[1]
                                if distance < desired_distance:
                                    agent.speed = np.array([0.0, 0.0])
                                    break
                        else:

                            if agent.counter < 4:
                                # Incrementar el contador, pero no moverse
                                agent.counter += 1
                            else:
                                agent.speed = np.array([0.0, -1.0])
                                if agent.decision == 1:
                                    # Verificar la posición
                                    if agent.pos[0] >= 14 and agent.pos[0] <=17 and agent.pos[1] <= 6.5 and agent.pos[1] >= 6:
                                        # Girar 90 grados a la derecha y comenzar a moverse hacia la derecha
                                        agent.speed = np.array([2.0, 0.0])
                                        self.space.place_agent(agent, [15,6])
                                        agent.color = "Blue"
                                        
                                elif agent.decision == 2:
                                    # Verificar la posición
                                    if agent.pos[0] >= 14 and agent.pos[0] <=17 and agent.pos[1] <= 5.5 and agent.pos[1] >= 5 :
                                        # Girar 90 grados a la derecha y comenzar a moverse hacia la derecha
                                        agent.speed = np.array([2.0, 0.0])
                                        self.space.place_agent(agent, [15,5.5])
                                        agent.color = "Black"

                                elif agent.decision == 3:
                                    # Verificar la posición
                                    if agent.pos[0] >= 14 and agent.pos[0] <=17 and agent.pos[1] <= 3.5 and agent.pos[1] >= 3:
                                        # Girar 90 grados a la derecha y comenzar a moverse hacia la derecha
                                        agent.speed = np.array([-2.0, 0.0])
                                        self.space.place_agent(agent, [15,3])
                                        agent.color = "Gray"

                                elif agent.decision == 4:
                                    # Verificar la posición
                                    if agent.pos[0] >= 14 and agent.pos[0] <=17 and agent.pos[1] <= 2.5 and agent.pos[1] >= 2:
                                        # Girar 90 grados a la derecha y comenzar a moverse hacia la derecha
                                        agent.speed = np.array([-2.0, 0.0])
                                        self.space.place_agent(agent, [15,2.5])
                                        agent.color = "Purple"

                agent.step()
            else:
                continue


canvas = SimpleCanvas(car_draw, 500, 500)

model_params = {}

server = ModularServer(Street, [canvas], "Traffic", model_params)


def setup_model():
    model = Street()
    model.step_count = 0  # Reset step count
    return model

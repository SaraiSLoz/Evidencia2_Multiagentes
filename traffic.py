import numpy as np
import random
from mesa import Agent, Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation
from mesa.visualization.ModularVisualization import ModularServer
import time

from SimpleContinuousModule import SimpleCanvas


class Car(Agent):
    def __init__(self, model: Model, color, pos, speed, decision):
        super().__init__(model.next_id(), model)  # Asigna un ID único automáticamente
        self.color = color
        self.pos = pos
        self.speed = speed
        self.decision = decision
        self.counter = 0

    def step(self):
        new_pos = self.pos + \
            np.array([0.5 * self.speed[0], 0.5 * self.speed[1]])
        self.model.space.move_agent(self, new_pos)


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
            np.arange(0, 26, distancia_separacion), 3, replace=False)
        # Todas las posiciones iniciales en y serán 2.5
        posiciones_iniciales_y = np.full(4, 2.5)

        for px, py in zip(posiciones_iniciales_x, posiciones_iniciales_y):
            car = Car(self, "Purple", np.array([px, py]), np.array(
                [-1.0, 0.0]), random.randint(1, 4))
            self.space.place_agent(car, car.pos)
            self.schedule.add(car)
         # First horizontal line (moving left)
        for px, py in zip(posiciones_iniciales_x, posiciones_iniciales_y):
            car = Car(self, "Gray", np.array([px, 3]), np.array(
                [-1.0, 0.0]), random.randint(1, 4))
            self.space.place_agent(car, car.pos)
            self.schedule.add(car)

        # Second horizontal line (moving right)
        for px, py in zip(posiciones_iniciales_x, posiciones_iniciales_y):
            car = Car(self, "Blue", np.array([px, 6]), np.array(
                [1.0, 0.0]), random.randint(1, 4))  # Change to move right
            self.space.place_agent(car, car.pos)
            self.schedule.add(car)

        for px, py in zip(posiciones_iniciales_x, posiciones_iniciales_y):
            car = Car(self, "Black", np.array([px, 5.5]), np.array(
                [1.0, 0.0]), random.randint(1, 4))  # Change to move right
            self.space.place_agent(car, car.pos)
            self.schedule.add(car)

        # Vertical line (moving upwards and then to the left)
        for py in [-1, -1.5, -2, -2.5]:
            car = Car(self, "Orange", np.array(
                [15, py]), np.array([0.0, -1.0]), random.choice([1, 2, 3, 4]))
            self.space.place_agent(car, car.pos)
            self.schedule.add(car)
        self.circles = [
            # primercirculo
            Circle(self.next_id(), self, 15.8, 2.6, 4),
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

        if self.step_count % 3 == 0:
            colors_to_check = ["Blue", "Gray", "Purple", "Black"]
            agents_to_remove = []

            for color in colors_to_check:
                agents = [
                    agent for agent in self.schedule.agents if agent.color == color]
                if len(agents) > 10:
                    # Agregar los agentes a eliminar
                    agents_to_remove.extend(agents[:len(agents) - 10])

            for agent in agents_to_remove:
                self.space.remove_agent(agent)
                self.schedule.remove(agent)

        if self.step_count % 10 == 0:
            orange_agent = Car(self, "Orange", np.array(
                [15, -0.5]), np.array([0.0, -1.0]), random.choice([1, 2, 3, 4]))
            self.space.place_agent(orange_agent, orange_agent.pos)
            self.schedule.add(orange_agent)

        for agent in self.schedule.agents:

            if agent.color == "Purple" or agent.color == "Gray":
                purple_agents = [other_agent for other_agent in self.schedule.agents if
                                 other_agent.color == "Purple" and other_agent != agent]

                gray_agents2 = [other_agent for other_agent in self.schedule.agents if
                                other_agent.color == "Gray" and other_agent != agent]
                # Coordenadas relevantes
                current_position = agent.pos[0]
                coordinateslow = 18.5
                coordinatestop = 16.5
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

                        if agent.counter < 3:
                            # Incrementar el contador, pero no moverse
                            agent.counter += 1
                        else:
                            agent.speed = np.array([0.0, -1.0])
                            if agent.decision == 1:
                                # Verificar la posición
                                if agent.pos[0] == 15 and agent.pos[1] == 6:
                                    # Girar 90 grados a la derecha y comenzar a moverse hacia la derecha
                                    agent.speed = np.array([2.0, 0.0])
                                    agent.color = "Blue"
                                elif agent.pos[0] == 15 and agent.speed[1] == 1.0:
                                    # Cambiar la dirección a moverse hacia la derecha
                                    agent.speed = np.array([1.0, 0.0])
                                    agent.color = "Blue"

                            elif agent.decision == 2:
                                # Verificar la posición
                                if agent.pos[0] == 15 and agent.pos[1] == 5.5:
                                    # Girar 90 grados a la derecha y comenzar a moverse hacia la derecha
                                    agent.speed = np.array([2.0, 0.0])
                                    agent.color = "Black"
                                elif agent.pos[0] == 15 and agent.speed[1] == 1.0:
                                    # Cambiar la dirección a moverse hacia la derecha
                                    agent.speed = np.array([1.0, 0.0])
                                    agent.color = "Black"

                            elif agent.decision == 3:
                                # Verificar la posición
                                if agent.pos[0] == 15 and agent.pos[1] == 3:
                                    # Girar 90 grados a la derecha y comenzar a moverse hacia la derecha
                                    agent.speed = np.array([-2.0, 0.0])
                                    agent.color = "Gray"
                                elif agent.pos[0] == 15 and agent.speed[1] == 1.0:
                                    # Cambiar la dirección a moverse hacia la derecha
                                    agent.speed = np.array([-1.0, 0.0])
                                    agent.color = "Gray"

                            else:
                                # Verificar la posición
                                if agent.pos[0] == 15 and agent.pos[1] == 2.5:
                                    # Girar 90 grados a la derecha y comenzar a moverse hacia la derecha
                                    agent.speed = np.array([-2.0, 0.0])
                                    agent.color = "Purple"
                                elif agent.pos[0] == 15 and agent.speed[1] == 1.0:
                                    # Cambiar la dirección a moverse hacia la derecha
                                    agent.speed = np.array([-1.0, 0.0])
                                    agent.color = "Purple"

            agent.step()


# canvas = SimpleCanvas(car_draw, 500, 500)

# model_params = {}

# server = ModularServer(Street, [canvas], "Traffic", model_params)


# def setup_model():
#     model = Street()
#     model.step_count = 0  # Reset step count
#     return model


# server.setup_model = setup_model
# server.port = 5100
# server.launch()

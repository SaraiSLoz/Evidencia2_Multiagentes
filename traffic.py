import numpy as np

from mesa import Agent, Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation
from mesa.visualization.ModularVisualization import ModularServer
import time

from SimpleContinuousModule import SimpleCanvas


class Car(Agent):
    def __init__(self, model: Model, pos, speed):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.speed = speed

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
    # Assign different colors based on movement direction
    if agent.speed[0] != 0:
        color = "Blue" if agent.speed[0] > 0 else "Purple"
    else:
        color = "Green" if agent.speed[1] > 0 else "Orange"
    return {"Shape": "rect", "w": 0.034, "h": 0.02, "Filled": "true", "Color": color}


class Street(Model):
    def __init__(self):
        super().__init__()
        self.space = ContinuousSpace(25, 10, True)
        self.schedule = RandomActivation(self)
        # Inicializar el tiempo de último cambio
        self.last_color_change_time = time.time()
        # First horizontal line (moving left)
        for px in np.random.choice(25 + 1, 5, replace=False):
            car = Car(self, np.array([px, 3]), np.array([-1.0, 0.0]))
            self.space.place_agent(car, car.pos)
            self.schedule.add(car)

        # Second horizontal line (moving right)
        for px in np.random.choice(25 + 1, 5, replace=False):
            car = Car(self, np.array([px, 6]), np.array(
                [1.0, 0.0]))  # Change to move right
            self.space.place_agent(car, car.pos)
            self.schedule.add(car)

        # Vertical line (moving upwards and then to the left)
        for py in np.random.choice(10 + 1, 5, replace=False):
            if py < 6:  # Move upwards
                car = Car(self, np.array([15, py]), np.array([0.0, -1.0]))
                self.space.place_agent(car, car.pos)
                self.schedule.add(car)

        self.circles = [
            # primercirculo
            Circle(self.next_id(), self, 15.8, 2.6, 4),
            # segundocirculo
            Circle(self.next_id(), self, 13.6, 6.5, 4),
            # tercercirculo
            Circle(self.next_id(), self, 16.5, 7, 4)
        ]

        self.circles[0].color = "Green"
        self.circles[1].color = "Green"
        self.circles[2].color = "Red"

        # Inicializar los tiempos de último cambio para cada círculo
        self.last_color_change_times = [time.time()] * len(self.circles)

        # Inicializar los intervalos de cambio de color para cada círculo
        # Tiempos en segundos: Verde: 6s, Amarillo: 2s, Rojo: 8s
        self.color_change_intervals = [[6, 2, 8], [
            6, 2, 8], [6, 2, 8]]  # Para cada círculo

        for circle in self.circles:
            self.space.place_agent(circle, (circle.x, circle.y))

    def step(self):
        current_time = time.time()

        for i, circle in enumerate(self.circles):
            # Obtener el patrón de colores para este círculo
            color_pattern = self.color_change_intervals[i]
            color_index = 0  # Inicializar el índice del color actual

            # Determinar el índice del color actual
            if circle.get_circle_portrayal()["Color"] == "Yellow":
                color_index = 1
            elif circle.get_circle_portrayal()["Color"] == "Red":
                color_index = 2

            time_passed = current_time - self.last_color_change_times[i]
            # Obtener el intervalo actual según el color actual
            current_interval = color_pattern[color_index]
            if time_passed >= current_interval:
                circle.change_color()
                self.last_color_change_times[i] = current_time

        self.schedule.step()


canvas = SimpleCanvas(car_draw, 500, 500)

model_params = {}

server = ModularServer(Street, [canvas], "Traffic", model_params)
server.port = 5100
server.launch()

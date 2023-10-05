import numpy as np

from mesa import Agent, Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation
from mesa.visualization.ModularVisualization import ModularServer
import time

from SimpleContinuousModule import SimpleCanvas


class Car(Agent):
    def __init__(self, model: Model, color, pos, speed):
        super().__init__(model.next_id(), model)  # Asigna un ID único automáticamente
        self.color = color
        self.pos = pos
        self.speed = speed

    def step(self):
        new_pos = self.pos + \
            np.array([0.5 * self.speed[0], 0.5 * self.speed[1]])
        self.model.space.move_agent(self, new_pos)

    def update(self, new_color):
        # Actualizar el color del coche
        self.color = new_color
        if new_color == "Purple":
            # Los coches morados se mueven hacia la izquierda
            self.speed = np.array([-1.0, 0.0])
            new_pos = self.pos + \
                np.array([0.5 * self.speed[0], 0.5 * self.speed[1]])
            self.model.space.move_agent(self, new_pos)

        # Actualizar las coordenadas del coche según el nuevo color

        # Mover el coche a las nuevas coordenadas


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
    # Obtener el color del agente
    color = agent.color

    # Definir las dimensiones predeterminadas
    w = 0.034
    h = 0.02

    # Asignar dimensiones y color según el valor de 'color'
    if color == "Blue":
        w = 0.034
        h = 0.02
    elif color == "Purple":
        w = 0.034
        h = 0.02
    elif color == "Green":
        w = 0.02
        h = 0.034
    elif color == "Orange":
        w = 0.02
        h = 0.034

    return {"Shape": "rect", "w": w, "h": h, "Filled": "true", "Color": color}


class Street(Model):
    def __init__(self):
        super().__init__()
        self.space = ContinuousSpace(25, 10, True)
        self.schedule = RandomActivation(self)
        # Inicializar el tiempo de último cambio
        self.last_color_change_time = time.time()
        # First horizontal line (moving left)
        for px in [18, 20, 22, 24]:
            car = Car(self, "Purple", np.array([px, 3]), np.array([-1.0, 0.0]))
            self.space.place_agent(car, car.pos)
            self.schedule.add(car)

        # Second horizontal line (moving right)
        for px in [6, 8, 10, 12]:
            car = Car(self, "Blue", np.array([px, 6]), np.array(
                [1.0, 0.0]))  # Change to move right
            self.space.place_agent(car, car.pos)
            self.schedule.add(car)

        # Vertical line (moving upwards and then to the left)
        for py in [-1, -1.5, -2, -2.5]:
            if py < 6:  # Move upwards
                car = Car(self, "Orange", np.array(
                    [15, py]), np.array([0.0, -1.0]))
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

        semaforo1 = self.circles[0].color  # Cambiado a segundo círculo
        semaforo2 = self.circles[1].color  # Cambiado a segundo círculo
        semaforo3 = self.circles[2].color  # Cambiado a segundo círculo

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

        for agent in self.schedule.agents:
            if agent.pos[1] <= 3:
                agent.update("Purple")
            else:
                if agent.color == "Purple":  # Solo para agentes naranjas
                    if agent.pos[0] == 16:  # Solo para la línea vertical
                        # Coordinar velocidad según el estado del semáforo
                        if semaforo1 == "Red":
                            agent.speed = np.array([0.0, 0.0])  # Detenerse
                        elif semaforo1 == "Green":
                            # Velocidad normal (se mueven hacia abajo)
                            agent.speed = np.array([-1.0, 0.0])
                        elif semaforo1 == "Yellow":
                            # Disminuir velocidad
                            agent.speed = np.array([-0.5, 0.0])

                elif agent.color == "Blue":
                    # Obtener todos los agentes azules
                    blue_agents = [other_agent for other_agent in self.schedule.agents if
                                   other_agent.color == "Blue" and other_agent != agent]

                    # Coordenadas relevantes
                    current_position = agent.pos[0]
                    coordinate_7_5 = 7.5
                    coordinate_12_5 = 12.5

                    # Distancia a la que se desea mantener
                    desired_distance = 1.5  # Ajusta según tu necesidad

                    # Calcular la velocidad en función de la distancia al agente de adelante
                    if current_position == coordinate_12_5 and semaforo2 == "Red":
                        # Detenerse en la coordenada 12.5 con semáforo en rojo
                        agent.speed = np.array([0.0, 0.0])
                    elif current_position == coordinate_7_5 and semaforo2 == "Yellow":
                        # Disminuir velocidad en la coordenada 7.5 con semáforo en amarillo
                        agent.speed = np.array([0.5, 0.0])
                    else:
                        # Calcular la velocidad para mantener la distancia
                        for blue_agent in blue_agents:
                            if blue_agent.pos[0] > current_position:
                                distance = blue_agent.pos[0] - current_position
                                if distance < desired_distance:
                                    agent.speed = np.array([0.0, 0.0])
                                    break
                        else:
                            agent.speed = np.array([1.0, 0.0])
                elif agent.color == "Orange":  # Solo para agentes naranjas
                    if agent.pos[0] == 15:  # Solo para la línea vertical
                        # Coordinar velocidad según el estado del semáforo
                        if semaforo3 == "Red":
                            agent.speed = np.array([0.0, 0.0])  # Detenerse
                        elif semaforo3 == "Green":
                            # Velocidad normal (se mueven hacia abajo)
                            agent.speed = np.array([0.0, -1.0])
                        elif semaforo3 == "Yellow":
                            # Disminuir velocidad
                            agent.speed = np.array([0.0, -0.5])
                agent.step()


canvas = SimpleCanvas(car_draw, 500, 500)

model_params = {}

server = ModularServer(Street, [canvas], "Traffic", model_params)
server.port = 5100
server.launch()

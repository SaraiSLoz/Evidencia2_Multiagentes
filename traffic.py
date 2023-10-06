import numpy as np
import random
from mesa import Agent, Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation
from mesa.visualization.ModularVisualization import ModularServer
import time

from SimpleContinuousModule import SimpleCanvas


class Car(Agent):
    def __init__(self, model: Model, color, pos, speed,decision):
        super().__init__(model.next_id(), model)  # Asigna un ID único automáticamente
        self.color = color
        self.pos = pos
        self.speed = speed
        self.decision = decision

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
        self.step_count = 0  # Contador de pasos
        for px in [18, 20, 22, 24]:
            car = Car(self, "Purple", np.array([px, 3]), np.array([-1.0, 0.0]),random.uniform(1,2))
            self.space.place_agent(car, car.pos)
            self.schedule.add(car)

         # First horizontal line (moving left)
        for px in [18, 20, 22, 24]:
            car = Car(self, "Purple", np.array(
                [px, 3.5]), np.array([-1.0, 0.0]), random.uniform(1,2))
            self.space.place_agent(car, car.pos)
            self.schedule.add(car)

        # Second horizontal line (moving right)
        for px in [6, 8, 10, 12]:
            car = Car(self, "Blue", np.array([px, 6]), np.array(
                [1.0, 0.0]),random.uniform(1,2))  # Change to move right
            self.space.place_agent(car, car.pos)
            self.schedule.add(car)

        for px in [6, 8, 10, 12]:
            car = Car(self, "Blue", np.array([px, 5.5]), np.array(
                [1.0, 0.0]),random.uniform(1,2))  # Change to move right
            self.space.place_agent(car, car.pos)
            self.schedule.add(car)

        # Vertical line (moving upwards and then to the left)
        for py in [-1, -1.5, -2, -2.5]:
            if py < 6:  # Move upwards
                car = Car(self, "Orange", np.array(
                    [15, py]), np.array([0.0, -1.0]),random.randint(1,2))
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
        cont = 0
        for agent in self.schedule.agents:
            
                if agent.color == "Purple":  
                    purple_agents = [other_agent for other_agent in self.schedule.agents if
                                   other_agent.color == "Purple" and other_agent != agent]

                    # Coordenadas relevantes
                    current_position = agent.pos[0]
                    coordinateslow = 18.5
                    coordinatestop = 16.5

                    # Distancia a la que se desea mantener
                    desired_distance = 1.5  

                    # Calcular la velocidad en función de la distancia al agente de adelante
                    if current_position == coordinatestop and semaforo1 == "Red":
                        # Detenerse en la coordenada  con semáforo en rojo
                        agent.speed = np.array([0.0, 0.0])
                    elif current_position == coordinateslow and semaforo1 == "Yellow":
                        # Disminuir velocidad en la coordenada  con semáforo en amarillo
                        agent.speed = np.array([-0.5, 0.0])
                    else:
                        # Calcular la velocidad para mantener la distancia
                        for purple_agent in purple_agents:
                            if purple_agent.pos[0] < current_position:
                                distance = current_position - purple_agent.pos[0]
                                if distance < desired_distance:
                                    agent.speed = np.array([0.0, 0.0])
                                    break
                        else:
                            agent.speed = np.array([-1.0, 0.0])

                elif agent.color == "Blue":
                    # Obtener todos los agentes azules
                    blue_agents = [other_agent for other_agent in self.schedule.agents if
                                   other_agent.color == "Blue" and other_agent != agent]

                    # Coordenadas relevantes
                    current_position = agent.pos[0]
                    coordinate_7_5 = 7.5
                    coordinate_12_5 = 12.5

                    # Distancia a la que se desea mantener
                    desired_distance = 1.5 

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
                    if agent.decision == 1:
                        if agent.pos[0] == 15 and agent.pos[1] == 6:  # Verificar la posición
                            # Girar 90 grados a la derecha y comenzar a moverse hacia la derecha
                            agent.speed = np.array([2.0, 0.0])
                            agent.color = "Blue"
                        elif agent.pos[0] == 15 and agent.speed[1] == 1.0:
                            # Cambiar la dirección a moverse hacia la derecha
                            agent.speed = np.array([1.0, 0.0])
                            agent.color = "Blue"
                    else:
                         if agent.pos[0] == 15 and agent.pos[1] == 3.5:  # Verificar la posición
                            # Girar 90 grados a la derecha y comenzar a moverse hacia la derecha
                            agent.speed = np.array([-2.0, 0.0])
                            agent.color = "Purple"
                         elif agent.pos[0] == 15 and agent.speed[1] == 1.0:
                            # Cambiar la dirección a moverse hacia la derecha
                            agent.speed = np.array([-1.0, 0.0])
                            agent.color = "Purple"
                
                    # if agent.decision == 1:
                    #      agent.pos[1] = 6
                    #      agent.pos[0] = 15 + cont
                    #      agent.speed = np.array([1.0, 0.0])
                    #      cont += 2                     
                    #      agent.step()
                # elif agent.color == "Orange":  # Solo para agentes naranjas
                #   if agent.pos[0] == 15 and agent.pos[1] == 6:  # Verificar la posición
                #     # Girar 90 grados a la derecha y comenzar a moverse hacia la derecha
                #       agent.speed = np.array([1.0, 0.0])
                #   elif agent.pos[0] == 15 and agent.speed[1] == 1.0:
                #     # Cambiar la dirección a moverse hacia la derecha
                #       agent.speed = np.array([1.0, 0.0])
                    # else:      
                    #     if semaforo3 == "Red":
                    #         agent.speed = np.array([0.0, 0.0])  # Detenerse
                    #     elif semaforo3 == "Green":
                    #             # Velocidad normal (se mueven hacia abajo)
                    #         agent.speed = np.array([0.0, -1.0])
                    #     elif semaforo3 == "Yellow":
                    #             # Disminuir velocidad
                    #         agent.speed = np.array([0.0, -0.5])

                agent.step()


canvas = SimpleCanvas(car_draw, 500, 500)

model_params = {}

server = ModularServer(Street, [canvas], "Traffic", model_params)


def setup_model():
    model = Street()
    model.step_count = 0  # Reset step count
    return model


server.setup_model = setup_model
server.port = 5000
server.launch()

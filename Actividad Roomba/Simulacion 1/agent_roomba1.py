# MA Actividad: Roomba
# Simulación 1 - Agent
# Fernanda Cantú Ortega A01782232

# Librerías a utilizar
from mesa import Agent
import networkx as nx

# Clase para definir los agentes de la simulación
class RoombaAgent(Agent):
    # Función para inicializar los agentes
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        # Definir variables iniciales
        self.direction = 4
        self.stepsTomados = 0
        self.posVisitadas = [(1, 1)] 
        self.bateria = 100
        self.charging = False 
        self.caminoEstacion = []

    # Función para definir movimiento de los agentes
    def move(self):
        # Definir los posibles movimientos del agente
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=True) 
        
        # Buscar los vecinos de los agentes
        neighbors = [(p, self.model.grid.get_cell_list_contents([p])) for p in possible_steps]

        # Buscar las celdas sucias
        posDirtyCells = [p for p, contents in neighbors if any(isinstance(agent, DirtyCell_Agent) for agent in contents)]

        # Si la bateria es mayor al 20% y no está cargando:
        if self.bateria > 20 and self.charging == False:
            # Si no hay celdas sucias, moverse aleatoriamente por los espacios libres
            if not posDirtyCells: 
                free_spaces = [p for p in possible_steps if self.model.grid.is_cell_empty(p) and p not in self.posVisitadas]
                if free_spaces:
                    next_move = self.random.choice(free_spaces)
                    self.model.grid.move_agent(self, next_move)
                    self.posVisitadas.append(next_move)
                    self.stepsTomados += 1
                    self.bateria -= 1
                else:
                    free_spaces = [p for p in possible_steps if self.model.grid.is_cell_empty(p)]
                    next_move = self.random.choice(free_spaces)
                    self.model.grid.move_agent(self, next_move)
                    self.stepsTomados += 1
                    self.bateria -= 1     
            # Si si hay celdas sucias, moverse hacia la primera celda sucia
            else: 
                next_move = posDirtyCells[0]
                self.model.grid.move_agent(self, next_move)
                self.stepsTomados += 1
                self.posVisitadas.append(next_move)
                dirt_agent = self.model.grid.get_cell_list_contents([next_move])[0]
                self.model.grid.remove_agent(dirt_agent)
                self.bateria -= 2
        # Si la bateria es menor al 20% o está cargando:
        else:
            estacionesCarga = self.model.grid.get_cell_list_contents([agent.pos for agent in self.model.schedule.agents if isinstance(agent, ChargingStation_Agent)])
            if estacionesCarga:
                estacion = estacionesCarga[0]
                # Si el agente no está en la misma posición que la estación de carga
                if estacion.pos != self.pos:
                    # Si no hay camino a la estación de carga, buscarlo
                    if not self.caminoEstacion:
                        self.caminoEstacion = regresarEstacion(self.posVisitadas, self.pos, estacion.pos)
                    # Si hay camino a la estación de carga, seguirlo
                    if self.caminoEstacion:
                        next_move = self.caminoEstacion.pop(0)
                        self.model.grid.move_agent(self, next_move)
                        self.bateria -= 1
                        self.stepsTomados += 1
                # Si la bateria es menor a 100 y el agente esta en el mismo lugar que la estación de carga, cargar
                elif estacion.pos == self.pos and self.bateria < 100:
                    self.bateria += 5
                    self.model.grid.move_agent(self, estacion.pos)
                    self.charging = True
                # Si la bateria esta llena, se reinicia la lista de camino a la estación de carga
                else:
                    self.caminoEstacion = []
                    self.charging = False
            else:
                # Lógica para moverse aleatoriamente cuando no hay estación de carga
                pass
    
    # Se determina el siguiente movimiento del agente y se ejecuta
    def step(self):
        self.move()

# Definir los obstaculos como agentes
class Obstacle_Agent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass  
    
# Definir las celdas sucias como agentes
class DirtyCell_Agent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass  

# Definir la estación de carga como agente
class ChargingStation_Agent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

# Algoritmo A* para encontrar el camino más corto    
def regresarEstacion(posVisitadas, inicio, final):
    gr = nx.Graph()

    # Nodos del grafo de las celdas visitadas
    for node in posVisitadas:
        gr.add_node(node)

    # Aristas del grafo entre celdas vecinas
    for node in posVisitadas:
        neighbors = [(x, y) for x in range(node[0] - 1, node[0] + 2) for y in range(node[1] - 1, node[1] + 2) if (x, y) in posVisitadas]
        gr.add_edges_from([(node, neighbor) for neighbor in neighbors])  

    # Intenta encontrar el camino más corto
    try:
        path = nx.astar_path(gr, inicio, final)
        return path
    # Si no hay un camino, regresa none
    except nx.NetworkXNoPath:
        return None
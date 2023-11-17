# MA Actividad: Roomba
# Simulación 1 - Model
# Fernanda Cantú Ortega A01782232

# Librerías a utilizar
from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa import DataCollector
from agent_roomba1 import RoombaAgent, Obstacle_Agent, DirtyCell_Agent, ChargingStation_Agent

# Clase para definir el modelo de la simulación
class RoombaModel(Model):
    # Función para inicializar la simulación
    def __init__(self, width, height, numObstacles, numDirtyCells):
        # Obtener cantidad de obstaculos y celdas sucias a partir de los sliders
        self.obstacles = numObstacles
        self.dirty = numDirtyCells

        # Propiedad que permite que haya más de un agente en la misma celda
        self.grid = MultiGrid(width,height,torus = False)

        # Propiedad que permite que los agentes se activen de manera aleatoria
        self.schedule = RandomActivation(self)
        
        # Propiedad que permite que la simulación se ejecute
        self.running = True 

        # Propiedad que permite recolectar datos de los agentes
        self.datacollector = DataCollector( 
        agent_reporters={"Steps": lambda a: a.stepsTomados if isinstance(a, RoombaAgent) else 0})

        # Crear el borde del grid y añadirle un obstaculo a cada una de las posiciones del mismo
        border = [(x,y) for y in range(height) for x in range(width) if y in [0, height-1] or x in [0, width - 1]]

        for pos in border:
            obs = Obstacle_Agent(pos, self)
            self.grid.place_agent(obs, pos)
        
        # Se inicializan el agente limpiador y su estación de carga en el modelo
        charging_station = ChargingStation_Agent(9999, self)
        self.schedule.add(charging_station)
        roombaAgent = RoombaAgent(0, self)
        self.schedule.add(roombaAgent)
        initialPos = (1, 1)
        self.grid.place_agent(charging_station, initialPos)
        self.grid.place_agent(roombaAgent, initialPos)
        
        # Función para generar posiciones aleatorias
        def randPos(w, h): return (
            self.random.randrange(w), self.random.randrange(h)
        )
        
        def create_agent(agent, N, unique_id):
            for i in range(N):
                ag = agent(i + unique_id, self)
                self.schedule.add(ag)
                pos = randPos(self.grid.width, self.grid.height)

                while (not self.grid.is_cell_empty(pos)):
                    pos = randPos(self.grid.width, self.grid.height)

                self.grid.place_agent(ag, pos)
        
        create_agent(Obstacle_Agent, self.obstacles, 1)
        create_agent(DirtyCell_Agent, self.dirty, 1000)
        self.datacollector.collect(self)
        
    # Función para avanzar un paso en la simulación
    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
from mesa.visualization import ModularServer, CanvasGrid, BarChartModule
from mesa.visualization import Slider
from model_roomba1 import RoombaModel, ObstacleAgent, DirtyCellAgent, ChargingStationAgent
from agent_roomba1 import ObstacleAgent, DirtyCellAgent, ChargingStationAgent

# Función para definir como se ve cada agente
def agent_portrayal(agent):
    # Agente principal (RoombaAgent)
    if agent is None: return
    
    portrayal = {"Shape": "circle",
                "Filled": "true",
                "Layer": 0,
                "Color": "red",
                "r": 0.7}
    
    # Obstaculos (ObstacleAgent)
    if (isinstance(agent, ObstacleAgent)):
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 2
        portrayal["w"] = 1
        portrayal["h"] = 1
    
    # Celdas sucias (DirtyCellAgent)
    if (isinstance(agent, DirtyCellAgent)):
        portrayal["Color"] = "brown"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2
    
    # Estaciones de carga (ChargingStationAgent)
    if (isinstance(agent, ChargingStationAgent)):
        portrayal["Color"] = "orange"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.9
        
    return portrayal

# Función para definir los parámetros de la simulación
model_params = {
    "numAgents": 1, 
    "width": 15, 
    "height": 15,
    # <nombre>: Slider(<nombre>, default, inicial, final, step)
    # "numAgents": Slider("Number of Agents", 1, 1, 10, 1), #todavía no tiene funcionalidad
    "obstacles": Slider("Obstacles", 0.15, 0.01, 0.5, 0.01),
    "dirtycells": Slider("Dirty Cells", 0.15, 0.01, 0.5, 0.01)
    }

grid = CanvasGrid(agent_portrayal, 15, 15, 500, 500)

bar_chart = BarChartModule(
    [{"Label":"Steps", "Color":"#AA0000"}], 
    scope="agent", sorting="ascending", sort_by="Steps")

server = ModularServer(RoombaModel, [grid, bar_chart], "Roomba Model - Simulación 1", model_params)
    
server.launch()
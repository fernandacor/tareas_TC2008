from model_roomba1 import RoombaModel, ObstacleAgent, DirtAgent, ChargingStationAgent
from mesa.visualization import CanvasGrid, BarChartModule
from mesa.visualization import ModularServer
from mesa.visualization import Slider

M = 15
N = 15

def agent_portrayal(agent):
    if agent is None: return
    
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 1,
                 "Color": "black",
                 "r": 0.5}

    if (isinstance(agent, ObstacleAgent)):
        portrayal["Color"] = "maroon"
        portrayal["Layer"] = 2
        portrayal["Shape"] = "rect"  # Cambiar la forma a cuadrado
        portrayal["w"] = 0.8  # Ancho del cuadrado
        portrayal["h"] = 0.8  # Altura del cuadrado

    if (isinstance(agent, ChargingStationAgent)):
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 0
        portrayal["Shape"] = "rect"  # Cambiar la forma a cuadrado
        portrayal["w"] = 1  # Ancho del cuadrado
        portrayal["h"] = 1  # Altura del cuadrado
        
    if (isinstance(agent, DirtAgent)):
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.3

    return portrayal

model_params = {"DirtN": Slider("Dirt Amount", 20, 1, M*(M/4), 1), 
                "ObsN": Slider("Obstacles Amount", 10, 1, N*(N/4), 1), 
                "width":M,
                "height":N}

grid = CanvasGrid(agent_portrayal, M, N, 500, 500)

bar_chart = BarChartModule(
    [{"Label":"Steps", "Color":"#AA0000"}], 
    scope="agent", sorting="ascending", sort_by="Steps")

server = ModularServer(RoombaModel, [grid, bar_chart], "Roomba", model_params)
                       
server.port = 8521 # The default
server.launch()
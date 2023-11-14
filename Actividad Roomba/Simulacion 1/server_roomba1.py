from mesa.visualization import ModularServer, CanvasGrid, BarChartModule
from mesa.visualization import Slider
from model_roomba1 import RoombaModel
from agent_roomba1 import ObstacleAgent

def agent_portrayal(agent):
    if agent is None: return
    
    portrayal = {"Shape": "circle",
                "Filled": "true",
                "Layer": 0,
                "Color": "red",
                "r": 0.5}
    
    if (isinstance(agent, ObstacleAgent)):
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2
    
    # if (isinstance(agent, DirtyCellAgent)):
    #     portrayal["Color"] = "darkgreen"
    #     portrayal["Layer"] = 2
    #     portrayal["r"] = 0.5
    
    return portrayal

model_params = {
    "N":1, 
    "width":15, 
    "height":15,
    # default, inicial, final, step
    # AGREGUE ESTO PARA EL SLIDER
    "obstacles": Slider("Obstacles", 0.15, 0.01, 0.5, 0.01),
    # "dirtycells": Slider("Dirty Cells", 0.15, 0.01, 0.5, 0.01)
    }

grid = CanvasGrid(agent_portrayal, 15, 15, 500, 500)

bar_chart = BarChartModule(
    [{"Label":"Steps", "Color":"#AA0000"}], 
    scope="agent", sorting="ascending", sort_by="Steps")

server = ModularServer(RoombaModel, [grid, bar_chart], "Roomba Model - Simulación 1", model_params)
                
server.launch()

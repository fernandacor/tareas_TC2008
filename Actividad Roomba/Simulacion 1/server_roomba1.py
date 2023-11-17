# MA Actividad: Roomba
# Simulación 1 - Server
# Fernanda Cantú Ortega A01782232

# Librerías a utilizar
from model_roomba1 import RoombaModel, Obstacle_Agent, DirtyCell_Agent, ChargingStation_Agent
from mesa.visualization import CanvasGrid, BarChartModule
from mesa.visualization import ModularServer
from mesa.visualization import Slider

# Función para definir como se va a mostrar cada agente
def agent_portrayal(agent):
    # Agente limpiador
    if agent is None: return
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 1,
                 "Color": "red",
                 "r": 0.5}
    
    # Obstáculos
    if (isinstance(agent, Obstacle_Agent)):
        portrayal["Shape"] = "rect"  
        portrayal["Filled"] = True
        portrayal["Color"] = "gray"
        portrayal["Layer"] = 2
        portrayal["w"] = 1
        portrayal["h"] = 1

    # Celdas sucias   
    if (isinstance(agent, DirtyCell_Agent)):
        portrayal["Shape"] = "circle"
        portrayal["Filled"] = True
        portrayal["Color"] = "darkgreen"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.3

    # Estación de carga
    if (isinstance(agent, ChargingStation_Agent)):
        portrayal["Shape"] = "circle"
        portrayal["Filled"] = True
        portrayal["Color"] = "yellow"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.9
         
    return portrayal

# Definición de los parametros del modelo
model_params = {
    # Tamaño del grid
    "width": 15, 
    "height": 15,
    # Sliders para modificar el número de obstáculos, celdas sucias, agentes y tiempo máximo de ejecución
    # "numAgents": 1,
    #"numAgents": Slider("Agents", 3, 1, 10, 1),
    "numObstacles": Slider("Obstacles", 20, 1, 15*(15/4), 1),
    "numDirtyCells": Slider("Dirty Cells", 10, 1, 15*(15/4), 1),
    # "maxSteps": Slider("Max Steps", 100, 1, 1000, 1)
    }

# Definición de la visualización
grid = CanvasGrid(agent_portrayal, 15, 15, 500, 500)

# Gráfica para mostrar el tiempo necesario hasta que todas las celdas estén limpias
# Gráfica para mostrar el porcentaje de celdas limpias después del termino de la simulación
# Gráfica de barras para mostrar pasos del agente limpiador
bar_chart = BarChartModule(
    [{"Label":"Steps", "Color":"#AA0000"}], 
    scope="agent", sorting="ascending", sort_by="Steps")

# Definición del servidor
server = ModularServer(RoombaModel, [grid, bar_chart], "Roomba Simulación 1 - A01782232", model_params)
                       
server.port = 8521
server.launch()
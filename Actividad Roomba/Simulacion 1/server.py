# Actividad 2: Roomba
# Fernanda Cantú A01782232

# Líbrerias a utilizar
from mesa.visualization import CanvasGrid, ChartModule, PieChartModule
from mesa.visualization import ModularServer
from mesa.visualization import Slider

from model import CleaningModel

# Los colores dependen del estado de las células
COLORS = {"Dirty": "#000000", "Clean": "#FF0000"}

# Diccionario para generar la visualización del simulador
def grid(celda):
    if celda is None:
        return
    portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
    (x, y) = celda.pos
    portrayal["x"] = x
    portrayal["y"] = y
    portrayal["Color"] = COLORS[celda.condition]

    return portrayal

#nombreVariable = CanvasGrid(portrayal, grid_row, grid_columns, canvas_width, canvas_height)
canvas_element = CanvasGrid(grid, 10, 10, 500, 500)

# Grafica para mostrar el número de células vivas y muertas con respecto al tiempo
tree_chart = ChartModule(
    [{"Label": label, "Color": color} for label, color in COLORS.items()]
)

# Grafica para mostrar el número de células vivas y muertas en el paso actual
pie_chart = PieChartModule(
    [{"Label": label, "Color": color} for label, color in COLORS.items()]
)

# The model parameters will be set by sliders controlling the initial density
model_params = {
    "height": 10,
    "width": 10,
    # <nombre>: Slider(<label>, <default>, <min_value>, <max_value>, <step_size>)
    "dirtyCells": Slider("Dirty cells", 0.15, 0.01, 0.5, 0.01),
    "obstacules": Slider("Obstacules", 0.15, 0.01, 0.5, 0.01),
}

# Definir qué se va a mostrar en la página al mismo tiempo y que se actualicen cuando el usuario interactue
server = ModularServer(CleaningModel, [canvas_element, tree_chart, pie_chart], "Actividad Roomba - Simulación 1", model_params)

server.launch()
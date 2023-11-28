# Actividad 1: Automata Celular
# Simulación 2
# Fernanda Cantú A01782232

# Líbrerias a utilizar
from mesa.visualization import CanvasGrid, ChartModule, PieChartModule
from mesa.visualization import ModularServer
from mesa.visualization import Slider

from sim2_model import AutomataCelular # corregí el nombre del archivo

# Los colores dependen del estado de las células
COLORS = {"Alive": "#000000", "Dead": "#FFFFFF"}

# Diccionario para generar la visualización del simulador
def cell_automaton_portrayal(cell):
    if cell is None:
        return
    portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
    (x, y) = cell.pos
    portrayal["x"] = x
    portrayal["y"] = y
    portrayal["Color"] = COLORS[cell.condition]

    return portrayal

#nombreVariable = CanvasGrid(portrayal, grid_row, grid_columns, canvas_width, canvas_height)
canvas_element = CanvasGrid(cell_automaton_portrayal, 50, 50, 500, 500)

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
    "height": 50,
    "width": 50,
    "density": Slider("Cell density", 0.15, 0.01, 0.5, 0.01),
}

# Definir qué se va a mostrar en la página al mismo tiempo y que se actualicen cuando el usuario interactue
server = ModularServer(AutomataCelular, [canvas_element, tree_chart, pie_chart], "Automata Celular Simulación 2 - A01782232", model_params)

server.launch()
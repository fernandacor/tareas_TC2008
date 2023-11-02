from mesa.visualization import CanvasGrid, ChartModule, PieChartModule
from mesa.visualization import ModularServer
from mesa.visualization import Slider

from model import AutomataCelular

# The colors of the portrayal will depend on the cell's condition //
COLORS = {"Alive": "#000000", "Dead": "#FF0000"}

# The portrayal is a dictionary that is used by the visualization server to
# generate a visualization of the given agent.
def cell_automaton_portrayal(cell):
    if cell is None:
        return
    portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
    (x, y) = cell.pos
    portrayal["x"] = x
    portrayal["y"] = y
    portrayal["Color"] = COLORS[cell.condition]

    return portrayal

# The canvas element will be 500x500 pixels, with each cell being 5x5 pixels.
# The portrayal method will fill each cell with a representation of the tree
# that is in that cell.
canvas_element = CanvasGrid(cell_automaton_portrayal, 50, 50, 500, 500)

# The chart will plot the number of each type of tree over time.
tree_chart = ChartModule(
    [{"Label": label, "Color": color} for label, color in COLORS.items()]
)

# The pie chart will plot the number of each type of tree at the current step.
pie_chart = PieChartModule(
    [{"Label": label, "Color": color} for label, color in COLORS.items()]
)

# The model parameters will be set by sliders controlling the initial density
model_params = {
    "height": 50,
    "width": 50,
    "density": Slider("Cell density", 0.15, 0.01, 0.5, 0.01),
}

# The modular server is a special visualization server that allows multiple
# elements to be displayed simultaneously, and for each of them to be updated
# when the user interacts with them.
server = ModularServer(
    AutomataCelular, [canvas_element, tree_chart, pie_chart], "Automata Celular Simulación 1 - A01782232", model_params
)

server.launch()
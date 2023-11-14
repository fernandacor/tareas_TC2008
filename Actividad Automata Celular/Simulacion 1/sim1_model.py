import mesa
from mesa import Model, DataCollector
from mesa.space import SingleGrid
from mesa.time import SimultaneousActivation 

from sim1_agent import CellCell

class AutomataCelular(Model):
    """
        Simulación 1 - Modelo de un Automata Celular
        
        Atributos:
            height, width: Tamaño del grid
            density: Porcentaje de celdas que tienen células vivas
    """

    def __init__(self, height=50, width=50, density=0.65):
        """
        Inicializar simulador.
        
        Argumentos:
            height, width: Tamaño del grid del modelo
            density: Porcentaje de celdas que tienen células vivas
        """
        
        # Definir objetos del modelo
        self.schedule = SimultaneousActivation(self) # Objeto de mesa que corre todos los agentes al mismo tiempo
        self.grid = SingleGrid(height, width, torus=False) # Torus define si "the grid wraps or not"
        self.i = 0 # Contador de pasos

        # DatatCollector es un objeto de mesa que sirve para recolectar datos del modelo
        self.datacollector = DataCollector(
            {
                "Alive": lambda m: self.count_type(m, "Alive"),
                "Dead": lambda m: self.count_type(m, "Dead")
            }
        )

        # La densidad basicamente es la probabilidad de que haya una celula viva
        # coord_iter itera sobre, y regresa, las posiciones y el contenido de cada celda
        for contents, (x, y) in self.grid.coord_iter():
            if (self.random.random() < density and y == 49):
                # Se crea una celula
                new_cell = CellCell((x, y), self)
                # Celula nueva se posiciona en el grid
                self.grid.place_agent(new_cell, (x, y))
                # Se agrega la celula nueva al scheduler
                self.schedule.add(new_cell)
                
            # Esto hace que todas las celulas que no estén en Y = 49 estén muertas
            else:
                new_cell = CellCell((x, y), self)
                new_cell.condition = "Dead"
                self.grid.place_agent(new_cell, (x, y))
                self.schedule.add(new_cell)

        self.running = True # Correr simulación
        self.datacollector.collect(self) # Recolectar datos del modelo

    def step(self):
        # El scheduler avanza cada celula por un paso y se guardan los datos en el datacollector
        self.schedule.step()
        self.datacollector.collect(self)

        # Cada que se hace un paso, se suma 1 al contador
        # Cuando llega al paso 49 (o sea al final del grid), se detiene la simulación
        self.i += 1
        if self.i >= 49:
            self.running = False

    @staticmethod
    def count_type(model, cell_condition):
        """
        Metodo helper estatico para contar las celulas con cierta condicion en un modelo dado
        """
        count = 0
        for cell in model.schedule.agents:
            if cell.condition == cell_condition:
                count += 1
        return count
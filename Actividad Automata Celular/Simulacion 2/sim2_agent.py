from mesa import Agent

class CellCell(Agent):
    """
        Celdas con celulas.
        
        Attributes:
            x, y: Grid coordinates
            condition: Puede estar "Alive" o "Dead"
            unique_id: (x,y) tuple.

            unique_id isn't strictly necessary here, but it's good practice to give one to each agent anyway.
    """

    def __init__(self, pos, model):
        """            
        Constructor que sirve para inicializar el estado de las variables
        
        Argumentos:
            self: referencia a una celula en cuestion
            pos: coordenadas de la celula en el grid
            model: referencia al modelo estándar del agente
        """
        super().__init__(pos, model) # super() permite accesar a los metodos de la clase padre
        self.pos = pos # posicion de la celula en el grid
        self.condition = "Alive" # se inicializa como viva la celula
        self._next_condition = None # se inicializa como None el siguiente estado de la celula

    def step(self):
        """
        Constructor para definir el siguiente estado de la celula
        """
        
        # Lista vacía para los vecinos de la celula
        neighbors = []
            
        # self.model.grit.iter_neighbors sirve para iterar sobre los vecinos de la celula
        # True indica que también se incluyen los vecinos diagonales
        for neighbor in self.model.grid.iter_neighbors(self.pos, True):
            # Revisa que la posición del vecino en relación al self
            if neighbor.pos[1] == self.pos[1] + 1: # corregí esto porque no se por que tenía que también checara la posición de x del vecino
                # Si si, se agrega a la lista de vecinos
                neighbors.append(neighbor)
            elif neighbor.pos[1] == 0 and self.pos[1] == 49: # corregí esto para que los neighbors de hasta arriba revisen los de hasta abajo
                neighbors.append(neighbor)
            
        # Si la lista de vecinos tiene 3 elementos, se revisan las condiciones para el sig estado   
        if len(neighbors) == 3:
                # 0 0 1
            if ((neighbors[0].condition == "Dead" and 
                neighbors[1].condition == "Dead" and
                neighbors[2].condition == "Alive") or
                
                # 0 1 1
                (neighbors[0].condition == "Dead" and
                neighbors[1].condition == "Alive" and
                neighbors[2].condition == "Alive") or
                
                # 1 0 0
                (neighbors[0].condition == "Alive" and
                neighbors[1].condition == "Dead" and
                neighbors[2].condition == "Dead") or
                    
                # 1 1 0
                (neighbors[0].condition == "Alive" and
                neighbors[1].condition == "Alive" and
                neighbors[2].condition == "Dead")):
                    
                self._next_condition = "Alive"
            else:
                self._next_condition = "Dead"
    
    def advance(self):
        """
        Avanza el modelo un paso
        """
        if self._next_condition is not None:
            self.condition = self._next_condition
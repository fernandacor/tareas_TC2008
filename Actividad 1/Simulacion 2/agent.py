from mesa import Agent

class TreeCell(Agent):
    """
        A tree cell.
        
        Attributes:
            x, y: Grid coordinates
            condition: Can be "Fine", "On Fire", or "Burned Out"
            unique_id: (x,y) tuple.

            unique_id isn't strictly necessary here, but it's good practice to give one to each agent anyway.
    """

    def __init__(self, pos, model):
        """
        Create a new tree.

        Args:
            pos: The tree's coordinates on the grid.
            model: standard model reference for agent.
        """
        super().__init__(pos, model) # inicializa como vivo
        self.pos = pos
        self.condition = "Alive" 
        self._next_condition = None

    def step(self):
        """
        If the tree is on fire, spread it to fine trees nearby.
        """
        if self.condition == "Dead" or self.condition == "Alive":
            neighbors = []
            for neighbor in self.model.grid.iter_neighbors(self.pos, True):
                if neighbor.pos[1] == self.pos[1] + 1:
                    neighbors.append(neighbor)
                    
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
                    
                    # 0 0 0
                elif ((neighbors[0].condition == "Dead" and 
                    neighbors[1].condition == "Dead" and
                    neighbors[2].condition == "Dead") or
                    # el y del vecino es igual al y de self -1 es arriba
                    # 0 1 0
                    (neighbors[0].condition == "Dead" and
                    neighbors[1].condition == "Alive" and
                    neighbors[2].condition == "Dead") or
                    
                    # 1 0 1
                    (neighbors[0].condition == "Alive" and
                    neighbors[1].condition == "Dead" and
                    neighbors[2].condition == "Alive") or
                    
                    # 1 1 1
                    (neighbors[0].condition == "Alive" and
                    neighbors[1].condition == "Alive" and
                    neighbors[2].condition == "Alive")):
                    
                    self._next_condition = "Dead"
                    
    
    def advance(self):
        """
        Advance the model by one step.
        """
        if self._next_condition is not None:
            self.condition = self._next_condition
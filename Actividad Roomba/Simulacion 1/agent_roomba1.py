from mesa import Agent
import networkx as nx

class RoombaAgent(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of eight directions
    """
    def __init__(self, unique_id, model):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.direction = 4
        self.steps_taken = 0
        self.visited_positions = [(1, 1)]  
        self.battery = 100
        self.charging = False 
        self.path_to_charging_station = []

    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
            include_center=True) 
        
        neighbors = [(p, self.model.grid.get_cell_list_contents([p])) for p in possible_steps]

        # Filtra las posiciones donde hay suciedad
        dirt_positions = [p for p, contents in neighbors if any(isinstance(agent, DirtAgent) for agent in contents)]
        
        #print(dirt_positions)
        if self.battery > 20 and self.charging == False:
            if not dirt_positions:  # Si no hay suciedad, mueve aleatoriamente pero considerando aquellas posiciones que ya han sido visitadas
                free_spaces = [p for p in possible_steps if self.model.grid.is_cell_empty(p) and p not in self.visited_positions]
                if free_spaces:
                    next_move = self.random.choice(free_spaces)
                    self.model.grid.move_agent(self, next_move)
                    self.visited_positions.append(next_move)
                    print(self.visited_positions)
                    self.steps_taken += 1
                    self.battery -= 1
                    print(self.battery)
                else:
                    free_spaces = [p for p in possible_steps if self.model.grid.is_cell_empty(p)]
                    next_move = self.random.choice(free_spaces)
                    print(next_move)
                    self.model.grid.move_agent(self, next_move)
                    print(self.visited_positions)
                    self.steps_taken += 1
                    self.battery -= 1
                    print(self.battery)
                    
            else:  # Si hay suciedad, mueve hacia la primera posición de suciedad y límpiala
                next_move = dirt_positions[0]
                self.model.grid.move_agent(self, next_move)
                self.steps_taken += 1
                self.visited_positions.append(next_move)
                print(self.visited_positions)
                dirt_agent = self.model.grid.get_cell_list_contents([next_move])[0]
                self.model.grid.remove_agent(dirt_agent)
                self.battery -= 2
                print(self.battery)
        else:
            charging_stations = self.model.grid.get_cell_list_contents([agent.pos for agent in self.model.schedule.agents if isinstance(agent, ChargingStationAgent)])
            if charging_stations:
                charging_station = charging_stations[0]
                print(charging_station.pos)
                if charging_station.pos != self.pos:
                    if not self.path_to_charging_station:
                        self.path_to_charging_station = a_star_path_visited_cells(self.visited_positions, self.pos, charging_station.pos)
                        print(self.path_to_charging_station)
                    if self.path_to_charging_station:
                        next_move = self.path_to_charging_station.pop(0)  # Saca el primer elemento de la lista
                        self.model.grid.move_agent(self, next_move)
                        print(f"Moving to charging station: {next_move}")
                        self.battery -= 1  # Costo de movimiento
                        print(self.battery)
                        self.steps_taken += 1
                elif charging_station.pos == self.pos and self.battery < 100:
                    self.battery += 5
                    print(f"Batería cargandose: {self.battery}%")
                    self.model.grid.move_agent(self, charging_station.pos)
                    self.charging = True
                else:
                    # La batería está llena, regresa a la lógica para moverse aleatoriamente
                    print("Battery full")
                    self.path_to_charging_station = []  # Reinicia el camino a la estación
                    self.charging = False  # Marca que ha dejado de cargar
            else:
                # Lógica para moverse aleatoriamente cuando no hay estación de carga
                pass

    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        self.move()

class ObstacleAgent(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass  
    

class DirtAgent(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass  

class ChargingStationAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass
    
def a_star_path_visited_cells(visited_positions, start, goal):
    G = nx.Graph()

    # Agrega nodos al grafo para las celdas visitadas
    for node in visited_positions:
        G.add_node(node)

    # Agrega aristas al grafo para conexiones entre celdas vecinas
    for node in visited_positions:
        neighbors = [(x, y) for x in range(node[0] - 1, node[0] + 2) for y in range(node[1] - 1, node[1] + 2) if (x, y) in visited_positions]
        G.add_edges_from([(node, neighbor) for neighbor in neighbors])
        
    print(G)   

    # Usa el algoritmo A* para encontrar el camino más corto
    try:
        path = nx.astar_path(G, start, goal)
        return path
    except nx.NetworkXNoPath:
        return None
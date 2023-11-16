from mesa import Agent
import networkx as nx

class RoombaAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.direction = 4
        self.steps_taken = 0
        
        #Cosas nuevas
        self.visited_positions = [(1,1)]
        self.battery = 100
        self.charging = False
        self.path_to_charger = []

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=True) 

        # Cosas nuevas
        neighbors = [(p, self.model.grid.get_cell_list_contents([p])) for p in possible_steps]
        dirtyCells = [p for p, contents in neighbors if any (isinstance(agent, DirtyCellAgent) for agent in contents)]
        
        if self.battery > 20 and self.charging == False:
            if not dirtyCells:
                free_spaces = [p for p in possible_steps if self.model.grid.is_cell_empty(p) and p not in self.visited_positions]
                if free_spaces:
                    next_move = self.random.choice(free_spaces)
                    self.model.grid.move_agent(self, next_move)
                    self.visited_positions.append(next_move)
                    self.steps_taken += 1
                    self.battery -= 1
                else:
                    free_spaces = [p for p in possible_steps if self.model.grid.is_cell_empty(p)]
                    next_move = self.random.choice(free_spaces)
                    self.model.grid.move_agent(self, next_move)
                    self.steps_taken += 1
                    self.battery -= 1
            else:
                next_move = dirtyCells[0]
                self.model.grid.move_agent(self, next_move)
                self.steps_taken += 1
                self.visited_positions.append(next_move)
                DirtyCellAgent = self.model.grid.get_cell_list_contents([next_move])[0]
                self.model.grid.remove_agent(DirtyCellAgent)
                self.battery -= 2
        else:
            charging_stations = self.model.get_cell_list_contents([agent.pos for agent in self.model.schedule.agents if isinstance(agent, ChargingStationAgent)])
            if charging_stations:
                charging_stations = charging_stations[0]
                if charging_stations.pos != self.pos:
                    if not self.path_to_charger:
                        self.path_to_charger = a_star_path_visited_cells(self.visited_positions, self.pos, charging_stations.pos)
                    if self.path_to_charger:
                        next_move = self.path_to_charger.pop(0)
                        self.model.grid.move_agent(self, next_move)
                        self.steps_taken += 1
                        self.battery -= 1
                elif charging_stations.pos == self.pos and self.battery < 100:
                    self.battery += 5
                    self.model.grid.move_agent(self, next_move)
                    self.charging = True
                else:
                    self.path_to_charger = []
                    self.charging = False
            else:
                pass   
        
        # Cosas viejas
        # freeSpaces = list(map(self.model.grid.is_cell_empty, possible_steps))

        # next_moves = [p for p,f in zip(possible_steps, freeSpaces) if f == True]
        
        # next_move = self.random.choice(next_moves)
        
        # if self.random.random() < 0.1:
        #     self.model.grid.move_agent(self, next_move)
        #     self.steps_taken+=1
            
    def step(self):
        self.move()
   
class EmptyCellAgent(Agent):
    """
    Empty cell agent. Just to add empty cells to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass 
class ObstacleAgent(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass  

class DirtyCellAgent(Agent):
    """
    Dirty cell agent. Just to add dirty cells to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class ChargingStationAgent(Agent):
    """
    Battery agent. Just to add battery charger to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass
    
def a_star_path_visited_cells(visited_positions, start, goal):
    G = nx.Graph()
    
    for node in visited_positions:
        G.add_node(node)
    
    for node in visited_positions:
        neighbors = [(x, y) for x in range(node[0] -1, node[0] + 2) for y in range(node[1] -1, node[1] + 2) if (x, y) in visited_positions]
        G.add_edges_from([(node, neighbor) for neighbor in neighbors])
    
    try:
        path = nx.astar_path(G, start, goal)
        return path
    except nx.NetworkXNoPath:
        return None
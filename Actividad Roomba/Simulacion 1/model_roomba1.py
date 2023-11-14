from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa import DataCollector
from agent_roomba1 import RoombaAgent, ObstacleAgent, DirtyCellAgent

class RoombaModel(Model):
    """ 
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
        height, width: The size of the grid to model
    """
    def __init__(self, N, width, height, obstacles):
        self.num_agents = N
        # Multigrid is a special type of grid where each cell can contain multiple agents.
        self.grid = MultiGrid(width,height,torus = False) 

        # RandomActivation is a scheduler that activates each agent once per step, in random order.
        self.schedule = RandomActivation(self)
        
        self.running = True 

        self.datacollector = DataCollector( 
        agent_reporters={"Steps": lambda a: a.steps_taken if isinstance(a, RoombaAgent) else 0})
    
        # Creates the border of the grid
        border = [(x,y) for y in range(height) for x in range(width) if y in [0, height-1] or x in [0, width - 1]]

        # Calculate the number of obstacles based on the slider value
        num_obstacles = int(obstacles * width * height) # AGREGUE ESTO PARA LO DEL SLIDER
        
        # # Calculate the number of dirty cells based on the slider value      
        # num_dirtycells = int(dirtycells * width * height) # AGREGUE ESTO PARA LO DEL SLIDER
        
        #Add obstacles to the grid in random positions
        for pos in border:
            a = ObstacleAgent(pos, self)
            self.grid.place_agent(a, pos)
            
        for i in range(num_obstacles): #CAMBIE EL 10 POR NUM_OBSTACLES PARA LO DEL SLIDER
            a = ObstacleAgent(i, self)
            self.schedule.add(a)

            pos = (self.random.randrange(self.grid.width), self.random.randrange(self.grid.height))

            while (not self.grid.is_cell_empty(pos)):
                pos = (self.random.randrange(self.grid.width), self.random.randrange(self.grid.height))

            self.grid.place_agent(a, pos)
        
        # # Add dirty cells to the grid in random positions
        # for i in range(num_dirtycells):
        #     a = DirtyCellAgent(i, self)
        #     self.schedule.add(a)

        #     pos = (self.random.randrange(self.grid.width), self.random.randrange(self.grid.height))

        #     while (not self.grid.is_cell_empty(pos)):
        #         pos = (self.random.randrange(self.grid.width), self.random.randrange(self.grid.height))

        #     self.grid.place_agent(a, pos)

        # Function to generate random positions
        pos_gen = lambda w, h: (self.random.randrange(w), self.random.randrange(h))

        # Add the agent to a random empty grid cell
        for i in range(self.num_agents):

            a = RoombaAgent(i+1000, self) 
            self.schedule.add(a)

            pos = pos_gen(self.grid.width, self.grid.height)

            while (not self.grid.is_cell_empty(pos)):
                pos = pos_gen(self.grid.width, self.grid.height)

            self.grid.place_agent(a, pos)
        
        self.datacollector.collect(self)

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
        self.datacollector.collect(self)
from mesa import Model, agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa import DataCollector
from agent_roomba1 import RoombaAgent, ObstacleAgent, DirtAgent, ChargingStationAgent

class RoombaModel(Model):
    """ 
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
        height, width: The size of the grid to model
    """
    def __init__(self, ObsN, DirtN, width, height):
        self.obstacles = ObsN
        self.dirty = DirtN
        # Multigrid is a special type of grid where each cell can contain multiple agents.
        self.grid = MultiGrid(width,height,torus = False)

        # RandomActivation is a scheduler that activates each agent once per step, in random order.
        self.schedule = RandomActivation(self)
        
        self.running = True 

        self.datacollector = DataCollector( 
        agent_reporters={"Steps": lambda a: a.steps_taken if isinstance(a, RoombaAgent) else 0})

        # Creates the border of the grid
        border = [(x,y) for y in range(height) for x in range(width) if y in [0, height-1] or x in [0, width - 1]]

        # Add obstacles to the grid
        for pos in border:
            obs = ObstacleAgent(pos, self)
            self.grid.place_agent(obs, pos)
        
        charging_station = ChargingStationAgent(9999, self)
        self.schedule.add(charging_station)
        roombaAgent = RoombaAgent(0, self)
        self.schedule.add(roombaAgent)
        initial_position = (1, 1)
        self.grid.place_agent(charging_station, initial_position)
        self.grid.place_agent(roombaAgent, initial_position)
        
        # Function to generate random positions
        def random_position(w, h): return (
            self.random.randrange(w), self.random.randrange(h)
        )
        
        
        def making_agent(agent, N, firstId):
            # Add the agent to a random empty grid cell
            for i in range(N):

                a = agent(i+firstId, self)
                
                self.schedule.add(a)

                pos = random_position(self.grid.width, self.grid.height)

                while (not self.grid.is_cell_empty(pos)):
                    pos = random_position(self.grid.width, self.grid.height)

                self.grid.place_agent(a, pos)
        
        making_agent(ObstacleAgent, self.obstacles, 1)
        making_agent(DirtAgent, self.dirty, 1000)
        self.datacollector.collect(self)

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
        self.datacollector.collect(self)
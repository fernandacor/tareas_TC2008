from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa import DataCollector
from agent_roomba1 import RoombaAgent, ObstacleAgent, DirtyCellAgent, ChargingStationAgent

class RoombaModel(Model):
    """ 
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
        height, width: The size of the grid to model
    """
    def __init__(self, numAgents, width, height, numObstacles, numDirty):
        self.num_agents = numAgents
        
        # Cosas nuevas:
        
        self.obstacles = int(numObstacles * width * height)
        self.dirtycells = int(numDirty * width * height)
        #self.obstacles = numObstacles
        # self.dirtycells = numDirty
        
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
        # num_obstacles = int(obstacles * width * height)
        
        # Calculate the number of dirty cells based on the slider value      
        # num_dirtycells = int(dirtycells * width * height)
        
        #Add obstacles to the grid in random positions
        for pos in border:
            obstacules = ObstacleAgent(pos, self)
            self.grid.place_agent(obstacules, pos)
        
        # Cosas nuevas
        charging_station = ChargingStationAgent(9999, self)
        self.schedule.add(charging_station)
        roomba = RoombaAgent(0, self)
        self.schedule.add(roomba)
        initial_pos = (1,1)
        self.grid.place_agent(charging_station, initial_pos)
        self.grid.place_agent(roomba, initial_pos)
        
        # def random_pos(width, height):
        #     return(self.random.randrange(width), self.random.randrange(height))
            
        # Cosas viejas
        # Añadir obstaculos en posiciones random
        for i in range(self.obstacles):
            obs = ObstacleAgent(i, self)
            self.schedule.add(obs)

            pos = (self.random.randrange(self.grid.width), self.random.randrange(self.grid.height))

            while (not self.grid.is_cell_empty(pos)):
                pos = (self.random.randrange(self.grid.width), self.random.randrange(self.grid.height))

            self.grid.place_agent(obs, pos)
        
        # Añadir obstaculos en posiciones random
        for i in range(self.dirtycells):
            dc = DirtyCellAgent(i+1000, self)
            self.schedule.add(dc)

            pos = (self.random.randrange(self.grid.width), self.random.randrange(self.grid.height))

            while (not self.grid.is_cell_empty(pos)):
                pos = (self.random.randrange(self.grid.width), self.random.randrange(self.grid.height))

            self.grid.place_agent(dc, pos)

        # Si el num de agentes es 1, se pone en (1,1)
        # Si son mas, se ponen en posiciones random
        if numAgents == 1:
            pos_gen = lambda w, h: (1, 1)
        else:
            pos_gen = lambda w, h: (self.random.randrange(w), self.random.randrange(h))

        # Añadir al roomba en una posicion random
        for j in range(self.num_agents):
            roomba = RoombaAgent(j+2000, self) 
            self.schedule.add(roomba)

            pos = pos_gen(self.grid.width, self.grid.height)

            while (not self.grid.is_cell_empty(pos)):
                pos = pos_gen(self.grid.width, self.grid.height)

            self.grid.place_agent(roomba, pos)        
        
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        
        
        
        #         def making_agent(agent, numAgents, firstId):
        #     for i in range(numAgents):
        #         a = agent(firstId + i, self)
        #         self.schedule.add(a)
        #         pos = random_pos(self.grid.width, self.grid.height)
        #         while (not self.grid.is_cell_empty(pos)):
        #             pos = random_pos(self.grid.width, self.grid.height)
        #         self.grid.place_agent(a, pos)
        
        # making_agent(ObstacleAgent, self.obstacles, 1)
        # making_agent(DirtyCellAgent, self.dirtycells, 1000)
        # self.datacollector.collect(self)
import mesa
from mesa import Model, DataCollector
from mesa.space import SingleGrid
from mesa.time import SimultaneousActivation 
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

import random

from agent import CleanerAgent

class CleaningModel(Model):
    def __init__(self, width = 10, height = 10, num_agents = 1):
        self.num_agents = num_agents
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)

        # Create charging station at position (1, 1)
        charging_station = CleanerAgent(0, self)
        self.grid.place_agent(charging_station, (1, 1))
        self.schedule.add(charging_station)

        # Initialize dirty cells
        for _ in range(int(0.2 * width * height)):
            x = random.randrange(width)
            y = random.randrange(height)
            cell = self.grid[x][y]
            cell['clean'] = False

            # Add obstacle with 10% probability
            if random.random() < 0.1:
                cell['obstacle'] = True

        # Create cleaner agents
        for i in range(1, num_agents + 1):
            agent = CleanerAgent(i, self)
            x = random.randrange(width)
            y = random.randrange(height)
            self.grid.place_agent(agent, (x, y))
            self.schedule.add(agent)

        self.datacollector = DataCollector(
            agent_reporters={"Battery": "battery"}
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

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
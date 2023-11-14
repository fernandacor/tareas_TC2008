from mesa import Agent
# from model import CleaningModel
import random

class CleanerAgent(Agent):
    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.pos = pos
        self.battery = 100

    def move(self):
        possible_moves = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )
        new_position = random.choice(possible_moves)
        self.model.grid.move_agent(self, new_position)
        self.battery -= 1

    def charge_battery(self):
        self.battery += 5
        if self.battery > 100:
            self.battery = 100

    def clean_cell(self):
        cell_contents, x, y = self.model.grid.get_cell_list_contents([self.pos])
        if len(cell_contents) > 1:  # More than one agent in the same cell (obstacle or charging station)
            self.battery -= 1
        else:
            self.model.grid[self.pos[0]][self.pos[1]]['clean'] = True
            self.battery -= 1

    def step(self):
        if self.battery <= 0:
            return
        if self.pos == (1, 1):  # If the agent is at the charging station
            self.charge_battery()
        else:
            self.move()
            self.clean_cell()

# Set up and run the model
width, height = 10, 10
num_agents = 1
max_steps = 500

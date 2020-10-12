"""
Creaete Class for environment
"""
import random
import numpy
from functools import reduce

class Space:
    """
    Actions:
        0 - left
        1 - down
        2 - right
        3 - up
        
    Game field (Space):
        Grid with size [height, weight]
        0 - usual cell
        1 - actor
        0.5 - food
    
    """
    
    def __init__(self, width=8, height=8):
        """
        Instance initialization
        
        width * height - size of field
        agent_place, food_place duplicate information from the state
        
        """
        
        self.height = height
        self.width = width
        
        self.action_space = [0, 1, 2, 3]
        self.agent_start_place = None
        self.agent_place = None # (row, colmn)
        self.food_place = None
        self.steps_from_start = None
        
        self.state = None
        print('Evn initializing')
        
    def get_random_food(self):
        """
        Return random empty cell from the state
        
        """
        while True:
            food_height = random.randint(0, self.height - 1)
            food_width = random.randint(0, self.width - 1)
            if food_height != self.agent_place[0] and food_width != self.agent_place[1]:
                break
                
        return (food_height, food_width)
    
    def move(self, new_agent_place):
        """
        Clear old and create new position if the agent
        """
        self.state[self.agent_place[0]][self.agent_place[1]] = 0
        self.state[new_agent_place[0]][new_agent_place[1]] = 1
        self.agent_place = new_agent_place
        
             
             
    def step(self, action):
        """
        Do step in the environment
        
        action must be in action_space
        """
        if action not in self.action_space:
            raise Exception("Unsupported action")
        
        self.steps_from_start += 1
        state = self.state
        done = False
        reward = 0
        
        if action == 0:    # left
            
            if self.agent_place[1] != 0:
                self.move((self.agent_place[0], self.agent_place[1] - 1))
                
        elif action == 1:  # down
            
            if self.agent_place[0] != self.height - 1:
                self.move((self.agent_place[0] + 1, self.agent_place[1]))
            
        elif action == 2:  # right
            if self.agent_place[1] != self.width - 1:
                self.move((self.agent_place[0], self.agent_place[1] + 1))
                
        else:              # up
            if self.agent_place[0] != 0:
                self.move((self.agent_place[0] - 1, self.agent_place[1]))
        
        if self.agent_place == self.food_place:
            done = True
            reward = (abs(self.agent_start_place[0] - self.food_place[0]) + 
                      abs(self.agent_start_place[1] - self.food_place[1])) / self.steps_from_start
            
        
        return numpy.array(reduce(lambda a, b: a + b, self.state)), reward, done, {}
        
        
    
    def reset(self):
        """
        Create start position of environment
        
            agent_place
            food_place
            state
        """
        self.state = [([0] * self.width) for i in range(self.height)]
        self.agent_start_place = (0, 0)
        self.agent_place = self.agent_start_place
        self.food_place = self.get_random_food()
        self.state[self.agent_place[0]][self.agent_place[1]] = 1
        self.state[self.food_place[0]][self.food_place[1]] = 0.5
        
        self.steps_from_start = 0
        
        return numpy.array(reduce(lambda a, b: a + b, self.state))
        
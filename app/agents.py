#!/usr/bin/python -tt
from __future__ import print_function
import random
import os

## Base agent class
#
# The Agent classes are the interfaces to the player. The Agent class is the base class which all
# other agent classes inherit
class Agent:
    ##
    #
    #
    def __init__(self):
        pass


## Agent class for real player
#
# The shot location is requested from the command line.
class AgentReal(Agent):
    ##
    #
    #
    def getShotLocation(self, shotgrid, shipstates):
        return input("Row, col: ")
        
## Random agents
#
# Place a shot at a random location
class AgentRandom(Agent):
    def getShotLocation(self,shotgrid,shipstates):
        validshots = list()
        for row in range(len(shotgrid)):
            for col in range(len(shotgrid[row])):
                if shotgrid[row][col] == 0:
                    validshots.append( (row, col) )
        if len(validshots) >= 1 :    
            return random.choice(validshots)
        else:
            return (-1,-1)

## Hunt and target agent
#
# This agent has two modes: hunting and target. The agent start in hunting mode. In this mode ships
# hunted by placing random shots. When there is a hit, the agent switches to target mode and places
# shots around the hit.
#
# This agent can be improved by detecting the orientation of ship when there are to hits next to
# each other.
class AgentHuntAndTarget(Agent):
    mode = ""
    def getShotLocation(self,shotgrid,shipstates):
        self.mode = "TARGET"
        shot = self.getTargetShots(shotgrid)
        if(shot == (-1,-1)):
            shot = random.choice(self.getHuntShots(shotgrid))
            self.mode = "HUNTING"
        return shot
        
    ## Helper function: getHuntShots
    #
    # In hunting mode a shot is random. However, not the complete grid is a candidate for a random shot.
    # The grid can be viewed as a checkerboard and only the black (or white) squares are a candidate. This
    # approach decreases  the number of shots significantly.
    def getHuntShots(self,grid):
        vector = list()
        row_id = 0
        for row in grid:
            col_id = 0
            for val in row:
                if(row_id % 2 == 0):
                    if (col_id % 2 == 1 and val == 0):
                        vector.append( (row_id, col_id) )
                else:
                    if (col_id %2 == 0 and val == 0):
                        vector.append( (row_id, col_id) )
                col_id += 1
            row_id += 1
        return vector
        
    ## Helper function: getTargetShots
    #
    # This function does two things. First it searches for all hits in the grid. When a hit is found, it
    # determines if there is still a valid shot to the left, right, top or bottom. When a valid shot is
    # found, it return are (row, column) tuple of the shot location. When no valid shots are found next
    # to a hit, the function return (-1,-1)
    def getTargetShots(self,grid):
        row_id = 0
        # Search for a hit
        for row in grid:
            col_id = 0
            for val in row:
                if(val==1): # Hit found
                    if(col_id>0):
                        # search left
                        for c in reversed(range(0,col_id)):
                            if(grid[row_id][c]==0):
                                return (row_id,c)
                            if(abs(grid[row_id][c])==1):
                                break
                                
                    if(col_id<9):
                        # search right
                        for c in range(col_id+1,10):
                            if(grid[row_id][c]==0):
                                return (row_id,c)
                            if(abs(grid[row_id][c])==1):
                                break
                                
                    if(row_id>0):
                        # search upwards
                        for r in reversed(range(0, row_id)):
                            if(grid[r][col_id]==0):
                                return (r,col_id)
                            if(abs(grid[r][col_id])==1):
                                break
                        
                    if(row_id<9):
                        # search downwards
                        for r in range(row_id+1, 10):
                            if(grid[r][col_id]==0):
                                return (r,col_id)
                            if(abs(grid[r][col_id])==1):
                                break
                col_id += 1
            row_id += 1
        return(-1,-1)
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
#!/usr/bin/python -tt
from __future__ import print_function
import random
import ships
import re
from collections import Counter

## PlayerInfo class
#
# The PlayerInfo class contains information about the player
class PlayerInfo:
    name = "unkown"
    id = None
    
    def __init__(self, id):
        self.id = id
    
    ## Set the player name
    #
    # Duh...
    def setName(self, name):
        self.name = name

## Player class
#
# The player class contains all the game information for a player
class Player:
    def __init__(self, id, parent):
        self.parent = parent
        self.info = PlayerInfo(id)
        self.ShipGrid = self.initializeGrid(self.parent.gridsize)
        self.ShotGrid = self.initializeGrid(self.parent.gridsize)
        
        self.ships = {1: ships.Battleship(self), 2: ships.Cruiser(self), 3: ships.Carrier(self), 4: ships.Submarine(self), 5: ships.Destroyer(self)}
        self.shipsAlive = len(self.ships)
    
    ## Placeholder
    #
    #
    def getShotLocation(self, shotgrid, shipstates):
        pass
    
    
    ## Initalize grid
    #
    # This function returns a square array (default size 10x10) filled with zeros
    def initializeGrid(self, size=10):
        grid = []
        for i in range(size):
            grid.append([0]*size)
        return grid
        
    ## Check which ships are still alive
    #
    #
    def getAliveShipCount(self):
        aliveshipcount = 0
        for shipid in self.ships:
            aliveshipcount += self.ships[shipid].getShipState()
            
        return aliveshipcount
    
    ## Get the state of all the ships
    #
    # Returns a dict. The name of shiptype is the key, the value is True for a ships that is still alive
    # and False for a ship that has been sunk.
    def getAllShipStates(self):
        shipstates = dict()
        for shipid in self.ships:
            key = self.ships[shipid].type
            val = self.ships[shipid].getShipState()
            shipstates[key] = val
            
        return shipstates
    
    ## Returns the number of shots
    #
    # The shotgrid contains 1 for a hit and -1 for a missed shot. The number of shots is therefore equal
    # to the sum of the absolute values in the shotgrid 
    def getShotCount(self):
        shotcount = 0
        for row in self.ShotGrid:
            shotcount += sum(map(abs,row))
            
        return shotcount
        
    ## Get the number of hits
    #
    # Counts how many times the umber 1 occurs in the shotgrid
    def getHitCount(self):
        hitcounter = 0
        for row in self.ShotGrid:
            hitcounter += row.count(1)
        
        return hitcounter
   
    ## Print the shot grid
    #
    #
    def printShotGrid(self):
        self.printGrid(self.ShotGrid)
      
    ## Print the ship grid
    #
    #
    def printShipGrid(self):
        self.printGrid(self.ShipGrid)
        
    ## Print a grid
    #
    #
    def printGrid(self, grid):
        # Print column numbers
        column_head =  " ".join(["{: d}".format(x) for x in range(10)])
        print("  |", column_head)
        print("-"*33)
        
        rownum = 0
        for r in grid:
            
            print(rownum, "|",  " ".join(["{: d}".format(x) for x in r]))
            rownum += 1
        print("")
        
    ## Get shot grid
    #
    #
    def getShotgrid(self):
        return self.ShotGrid
            
    ## Place a shot
    #
    #
    def placeShot(self, r, c):
        if r > self.parent.gridsize-1 or c > self.parent.gridsize -1 or r < 0 or c < 0:
            # Invalid shot
            return 0

        #Already shot on that coordinate
        if abs(self.ShotGrid[r][c])==1:
            return 0

        #Valid shot, check if there is a ship
        hit = self.parent.players[1-self.info.id].checkShot(r, c)
        
        #Switch the turn to the other player
        self.parent.switchTurn()

        #Set the shotgrid and return 1 (hit) of -1 (miss)
        if(hit):
            self.ShotGrid[r][c] = 1
            return 1
        else:
            self.ShotGrid[r][c] = -1
            return -1
            
            
    ## Place ship with (external) matrix
    #
    #
    def placeShipsFromMatrix(self, matrix):
        self.ShipGrid = matrix
            
    ## Place ships random
    #
    # The random position is determined in two steps. First a random orientation (horizontal of vertial) is
    # determined. The next step is to combine the orientation with the length of the ship to determine the 
    # position in such a way that the ships stay within the boundaries of the grid. Ships are not allowed 
    # to overlap. Therefore, a position is searched for until there is no overlap with another ship.
    def placeShipsRandom(self):
        for shipid in self.ships:
            if(random.randint(0,1)):
                orientation = 'H'
            else:
                orientation = 'V'
                
            # Try to place the ship until a valid place is found
            while(self.ships[shipid].placed == False):
                if(orientation=='H'):
                    random_r = random.randint(0,self.parent.gridsize-1)
                    random_c = random.randint(0,self.parent.gridsize-1-self.ships[shipid].getShipLength())
                    self.ships[shipid].placeShip(shipid, random_r, random_c, orientation)
                if(orientation=='V'):
                    random_r = random.randint(0,self.parent.gridsize-1-self.ships[shipid].getShipLength())
                    random_c = random.randint(0,self.parent.gridsize-1)
                    self.ships[shipid].placeShip(shipid, random_r, random_c, orientation)
    
    ##
    #
    #
    def checkShot(self, r, c):
        shipid = self.ShipGrid[r][c]
        if shipid > 0:
            self.ShipGrid[r][c] = -self.ShipGrid[r][c]
            if self.ships[shipid].incrementHitCounter():
                #print(self.ships[shipid].type , "sunk")
                self.shipsAlive -= 1
                if self.shipsAlive == 0:
                    self.parent.running = False
                    self.parent.winner = 1-self.info.id
            return True
        else:
            return False
       
## The base class which contains the complete game
#
# Blablabla
class Battleship:
    gridsize = 10
    running = True
    winner = None
    
    #Gamemode:
    # 0: Training
    # 1: Single player
    # 2: Multiplayer
    # 3: Competing agents (multiplayer)
    gamemode = 0

    # Initialize players
    def __init__(self, gamemode=2):
        self.gamemode = gamemode
        self.players = {0: Player(0,self), 1: Player(1,self)}
        self.players[0].info.setName("Player 1")
        self.players[1].info.setName("Player 2")
        
        # Which player has the first turn
        if(self.gamemode == 0):
            self.turn = 0
        else:
            self.turn = random.randint(0,1)
    
    ## Swtich the turn to the other player
    def switchTurn(self):
        if(self.gamemode!=0):
            self.turn = 1 - self.turn

    ## Load ship matrix from file
    #
    #
    def loadShipMatrixFromFile(self,f):
        grid = []
        with open(f) as file:
            for line in file:
                # strip double spaces
                line = re.sub(' +',' ', line.strip())
                grid_row = [int(x) for x in line.split(' ')]
                grid.append(grid_row)
        return grid
    
if __name__=='__main__':
    pass

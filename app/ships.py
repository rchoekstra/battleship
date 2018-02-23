#!/usr/bin/python -tt
from __future__ import print_function

## Baseclass for Ship
#
# This class is only used indirectly. It is inherited by the Battleship, Cruiser, Carrier, Submartine and Destroyer classes.
# Those ship specific classes only implement the constructor, which sets the length of the ship.
class BaseShip:
    shiplength  = 0
    hitcounter = 0
    row = None
    col = None
    orientation = ""    # H(orizontal) or V(ertical)
    placed = False
    type = ""

    ## Ship constructor
    def __init__(self, parent):
        self.parent = parent
    
    ## Hit counter
    #
    # Increments the number of hits. This function returns True if the ship sunk
    def incrementHitCounter(self):
        self.hitcounter += 1
        if self.hitcounter == self.shiplength:
            return True
        else:
            return False

    ## Function to check if ship is still alive
    #
    # Return True if the ship is alive and False if the has has sunk
    def getShipState(self):
        return self.shiplength > self.hitcounter
        
    ## Get the ship length
    #
    # Return ship length
    def getShipLength(self):
        return self.shiplength
    
    ## Place the ship on the grid
    #
    # Place the ship a specified row, column and orientation
    def placeShip(self, id, r, c, orientation):
        gridsize = len(self.parent.ShipGrid)
        
        # Negative rows or columns are not allowed
        if(r<0 or c < 0):
            return False
        
        # Place ship with horizontal orientation
        if(orientation=='H'):
            start = c
            end   = c + self.shiplength - 1

            if(end > gridsize - 1 or r > gridsize - 1):
                return False
            else:
                # Check the position is valid
                for _c in range(start, end+1):
                    # Check if there is another ship
                    if (self.parent.ShipGrid[r][_c] != 0):
                        return False
                        
                # Place the ship
                for _c in range(start, end+1):
                    self.parent.ShipGrid[r][_c] = id

                self.placed = True
                return True
        
        # Place ship with vertical orientation
        elif(orientation=='V'):
            start = r
            end   = r + self.shiplength - 1
            if(end > gridsize - 1 or r > gridsize - 1):
                return False
            else:
                # Check the position is valid
                for _r in range(start, end+1):
                    # Check if there is another ship
                    if (self.parent.ShipGrid[_r][c] != 0):
                        return False
                        
                # Place the ship
                for _r in range(start, end+1):
                    self.parent.ShipGrid[_r][c] = id

                self.placed = True
                return True

## Battleship class
#
# Ship has length 4
class Battleship(BaseShip):
    def __init__(self,parent):
        BaseShip.__init__(self,parent)
        self.shiplength = 4
        self.type = "Battleship"

## Cruiser class
#
# Ship has length 3
class Cruiser(BaseShip):
    def __init__(self,parent):
        BaseShip.__init__(self,parent)
        self.shiplength = 3
        self.type = "Cruiser"
        
## Carier class
#
# Ship has length 5
class Carrier(BaseShip):
    def __init__(self,parent):
        BaseShip.__init__(self,parent)
        self.shiplength = 5
        self.type = "Carrier"

## Submarine class
#
# Ship has length 3
class Submarine(BaseShip):
    def __init__(self,parent):
        BaseShip.__init__(self,parent)
        self.shiplength = 3
        self.type = "Submarine"

## Destroyer class
#
# Ship has length 2
class Destroyer(BaseShip):
    def __init__(self,parent):
        BaseShip.__init__(self,parent)
        self.shiplength = 2
        self.type = "Destroyer"

if __name__=='__main__':
    pass
#!/usr/bin/python -tt
from __future__ import print_function
import battleship as bs
import os
from time import sleep

#Select gamemode
print("Select gamemode")
print("0: Training")
print("1: Single player")
print("2: Multi player")
gamemode = input("? ")

#Initialize the game
game = bs.Battleship(gamemode)

#Initialize the grids
grid1 = game.loadShipMatrixFromFile('shipmatrix1.txt')
game.players[0].placeShipsFromMatrix(grid1)
#game.players[0].placeShipsRandom()

grid2 = game.loadShipMatrixFromFile('shipmatrix2.txt')
game.players[1].placeShipsFromMatrix(grid2)
#game.players[1].placeShipsRandom()

#Start playing
while(game.running):
    validshot = 0
    
    while(validshot==0):
        os.system('clear')
        print(game.players[game.turn].info.name, "may take take a shot")
        print("")
        print("Ships")
        game.players[game.turn].printShipGrid()
        
        print("Shots (n="+str(game.players[game.turn].getShotCount())+")")
        game.players[game.turn].printShotGrid()
        
        rc = input("Row, col: ")
        r = rc[0]
        c = rc[1]
        validshot = game.players[game.turn].placeShot(r,c)
        print("Return value:", validshot)
        _dummy_ = raw_input("Press ENTER to proceed")

print("Game finished")
print("")
for playerid in game.players:
    print("Game statistics for", game.players[playerid].info.name)
    print("Number of shots:", game.players[playerid].getShotCount())
    print("Hits:           ", "?")
    print("Missed:         ", "?")
    print("Ships alive:    ", game.players[playerid].getAliveShipCount())

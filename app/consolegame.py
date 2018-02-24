#!/usr/bin/python -tt
from __future__ import print_function
import battleship as bs
import os
from time import sleep
import agents

#Select gamemode
print("Select gamemode")
print("0: Training")
print("1: Single player")
print("2: Multi player")
print("3: Competing agents")
gamemode = input("? ")

#Initialize the game
game = bs.Battleship(gamemode)

if(gamemode==0):
    agent1 = None
    agent2 = None
if(gamemode==1):
    agent1 = agents.AgentReal()
    agent2 = agents.AgentRandom()
elif(gamemode==2):
    agent1 = agents.AgentReal()
    agent2 = agents.AgentReal()
elif(gamemode==3):
    agent1 = agents.AgentRandom()
    agent2 = agents.AgentRandom()

game.players[0].getShotLocation = agent1.getShotLocation
game.players[1].getShotLocation = agent2.getShotLocation

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
        
        rc = game.players[game.turn].getShotLocation(game.players[game.turn].ShotGrid, game.players[game.turn].getAllShipStates())
        print("Shot location: ",rc)
        validshot = game.players[game.turn].placeShot(rc[0],rc[1])
        print("Return value:", validshot)
        _dummy_ = raw_input("Press ENTER to proceed")

print("\n=============\nGame finished\n=============\n")
for playerid in game.players:
    print("Game statistics for", game.players[playerid].info.name)
    print("-"*(20+len(game.players[playerid].info.name)))
    shotcount = game.players[playerid].getShotCount()
    hitcount  = game.players[playerid].getHitCount()
    print("Number of shots:", shotcount)
    print("Hits:           ", hitcount)
    print("Missed:         ", shotcount - hitcount)
    print("Ships alive:    ", game.players[playerid].getAliveShipCount())
    print("")

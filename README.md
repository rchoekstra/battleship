# Battleship
This is a python implementation of the game Battleship. I'm writing this game for an AI-competition and it's still work in progress. 

## Game description
Battleship is a guessing game for two players. It is played on ruled grids (paper or board) on which the players' fleets of ships (including battleships) are marked. The locations of the fleet are concealed from the other player. Players alternate turns calling "shots" at the other player's ships, and the objective of the game is to destroy the opposing player's fleet.

Battleships:

| Class of ship | Size/length |
|---------------|:-----------:|
| Battleship    | 4           |
| Cruiser       | 3           |
| Carier        | 5           |
| Submarine     | 3           |
| Destroyer     | 2           |

Source: [Wikipedia](https://en.wikipedia.org/wiki/Battleship_(game) "Battleship (game)")

## Usage
To start the game an instance of the Battleship class (battleship.py) must be initiated. Before playing the game the following steps must be performed:

1. Select gamemode
2. Set players detail (optional)
3. Place ships on grid manually or random

### Select gamemode
The gamemode can be selected by passing one of the following numbers to the constructor of the Battleship class:

0. Training
1. Single player
2. Multi player (default)

In training mode (0) only one player places the ships on the grid and the other player takes the shots. The purpose for this training mode is to train an AI-agent. 

In the single player mode (1) a real person can play against an AI-agent. The ships for the AI-agent are placed random on the grid and the real life player must place the ships manually.

In the multi player mode (2) two real persons can play against each other. Both players must place their ships manually.

### Set player details
The Battleship class contains a dictionary 'players'. This dict contains one element for each player (key 0 and 1). Each player element is an instance of the Player class. This class contains a member of type PlayerInfo. Player details can be chaned by calling the right functions of this class (e.g.: Battleship.players[0].info.setName("Player name"))

### Place ships on grid
There are two methods for placing the ships on the grid. 

1. Random
2. External file

By calling the function Battleship.players[].placeShipsRandom() the ships are placed random on the grid.

The load the ships from an external file the following functions can be used:

```python
playerid = 0 #0/1
grid = game.loadShipMatrixFromFile('shipmatrix.txt')
Battleship.players[playerid].placeShipsFromMatrix(grid)
```

## Classes
- Battleship
- Player
- PlayerInfo
- Ships.BaseShip
- Ships.Battleship (inherits BaseShip)
- Ships.Cruiser (inherits BaseShip)
- Ships.Carier (inherits BaseShip)
- Ships.Submarine (inherits BaseShip)
- Ships.Destroyer (inherits BaseShip)
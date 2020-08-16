# Import Battleship essentials
import battleship as bs
from agents import Agent

# Tensorflow/Keras imports
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# Other imports
import random
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import time

# Constants
GRIDSIZE = 6
N_INPUT = GRIDSIZE*GRIDSIZE
N_OUTPUT = GRIDSIZE*GRIDSIZE
DEBUG = True
NUM_EPISODES = 10_000


# Helper functions
def debug(msg, end="\n", flush=True):
    if DEBUG:
        print(msg, end=end, flush=flush)


def OneHotEncodeGrid(grid, num_classes=3):
    one_hot = np.zeros((grid.size, num_classes))
    rows = np.arange(grid.size)
    one_hot[rows, grid.reshape(grid.size)+1] = 1
    return one_hot


def create_q_model():
    model = keras.Sequential()
    model.add(layers.Dense(GRIDSIZE*GRIDSIZE//1.25, activation='relu', name="layer1",
                           input_shape=(GRIDSIZE*GRIDSIZE, 3),
                           bias_initializer='random_normal'))
    model.add(layers.Flatten())
    model.add(layers.Dense(GRIDSIZE*GRIDSIZE//1.25, activation='relu', name="layer2"))
    model.add(layers.Dense(GRIDSIZE*GRIDSIZE//1.25, activation='relu', name="layer3"))
    model.add(layers.Dense(N_OUTPUT, activation='linear', name="action"))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model


model = create_q_model()


# Hyper parameters
LEARNING_RATE = 1 # 1: Only use future Q-value
y = 0.99
eps = 0.1
eps_decay_factor = 0.999

# Track some information per episode
shotcounts = list()
durations = list()


for episode in range(NUM_EPISODES):
    # Initialize game
    if episode % 50 == 0:
        debug(f"Episode {episode}/{NUM_EPISODES}") 
    game_start = time.monotonic()
    game = bs.Battleship(0, GRIDSIZE)
    game.players[1].placeShipsRandom()

    eps *= eps_decay_factor

    while game.running:
        current_state = OneHotEncodeGrid(game.players[0].ShotGrid)
        current_q_values = model.predict(np.array([current_state]))[0].reshape(GRIDSIZE, GRIDSIZE)

        if np.random.random() < eps:
            # Random action
            valid_r, valid_c = np.where(game.players[0].getValidShots())
            ValidShotIndices = list(zip(valid_r, valid_c))
            shot_r, shot_c = random.choice(ValidShotIndices)
        else:
            # Action based on prediction
            valid_actions = current_q_values.copy()
            valid_actions[~game.players[0].getValidShots()] = -999
            shot_r, shot_c = np.unravel_index(valid_actions.argmax(), valid_actions.shape)

        current_q = current_q_values[shot_r, shot_c]
        reward = game.players[0].placeShot(shot_r, shot_c)
        action = (shot_r, shot_c)
        new_state = OneHotEncodeGrid(game.players[0].ShotGrid)

        # Best action based on new state
        max_future_q = np.max(model.predict(np.array([new_state]))[0])
        target_q = current_q_values.copy()
        new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + y * max_future_q)
        target_q[shot_r, shot_c] = new_q

        fit = model.fit(np.array([current_state]), np.array([target_q]).reshape(1, N_OUTPUT), epochs=1, verbose=0)

    shotcount = game.players[0].getShotCount()
    duration = time.monotonic() - game_start

    shotcounts.append(shotcount)
    durations.append(duration)


plt.scatter(df.shotcount, df.duration, s=1)
plt.ylim(0, 2)
plt.show()

plt.plot(df.shotcount)
plt.show()

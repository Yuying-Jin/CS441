''' 
Lab 12: Beginnings of Reinforcement Learning

Create a function called run_episode that takes in two players
and runs a single episode of combat between them. 
As per RL conventions, the function should return a list of tuples
of the form (observation/state, action, reward) for each turn in the episode.
Note that observation/state is a tuple of the form (player1_health, player2_health).
Action is simply the weapon selected by the player.
Reward is the reward for the player for that turn.
'''
import sys
from pathlib import Path

sys.path.append(str((Path(__file__) / ".." / ".." / "..").resolve().absolute()))

from src.lab11.pygame_ai_player import PyGameAICombatPlayer
from src.lab11.pygame_combat import PyGameComputerCombatPlayer
from src.lab11.turn_combat import Combat


def run_episode(player1, player2):
    current_game = Combat()
    episode_log = []

    # initial states of player1
    initial_state_player1 = (player1.health, player1.weapon)

    while not current_game.gameOver:
        # Players select actions
        player1.selectAction(initial_state_player1)

        # Take combat turn
        current_game.newRound()
        current_game.takeTurn(player1, player2)

        # Record state, actions, and rewards for this turn
        state = (player1.health, player2.health)
        actions = player1.weapon
        reward = current_game.checkWin(player1, player2)
        episode_log.append((state, actions, reward))

    return episode_log


if __name__ == "__main__":
    player = PyGameAICombatPlayer("Player")
    computer = PyGameComputerCombatPlayer("Computer")
    print(run_episode(player, computer))

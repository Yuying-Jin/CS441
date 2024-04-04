'''
Lab 13: My first AI agent.
In this lab, you will create your first AI agent.
You will use the run_episode function from lab 12 to run a number of episodes
and collect the returns for each state-action pair.
Then you will use the returns to calculate the action values for each state-action pair.
Finally, you will use the action values to calculate the optimal policy.
You will then test the optimal policy to see how well it performs.

Sidebar-
If you reward every action you may end up in a situation where the agent
will always choose the action that gives the highest reward. Ironically,
this may lead to the agent losing the game.
'''
import sys
from pathlib import Path

sys.path.append(str((Path(__file__) / ".." / ".." / "..").resolve().absolute()))

# line taken from turn_combat.py
sys.path.append(str((Path(__file__) / ".." / "..").resolve().absolute()))

from src.lab11.pygame_combat import PyGameComputerCombatPlayer
from src.lab11.turn_combat import CombatPlayer
from src.lab12.episode import run_episode

from collections import defaultdict
import random
import numpy as np


class PyGameRandomCombatPlayer(PyGameComputerCombatPlayer):
    def __init__(self, name):
        super().__init__(name)

    def weapon_selecting_strategy(self):
        self.weapon = random.randint(0, 2)
        return self.weapon


class PyGamePolicyCombatPlayer(CombatPlayer):
    def __init__(self, name, policy):
        super().__init__(name)
        self.policy = policy

    def weapon_selecting_strategy(self):
        self.weapon = self.policy[self.current_env_state]
        return self.weapon


def run_random_episode(player, opponent):
    player.health = random.choice(range(10, 110, 10))
    opponent.health = random.choice(range(10, 110, 10))
    return run_episode(player, opponent)


def get_history_returns(history):
    total_return = sum([reward for _, _, reward in history])
    returns = {}
    for i, (state, action, reward) in enumerate(history):
        if state not in returns:
            returns[state] = {}
        returns[state][action] = total_return - sum(
            [reward for _, _, reward in history[:i]]
        )
    return returns


def run_episodes(n_episodes):
    ''' Run 'n_episodes' random episodes and return the action values for each state-action pair.
        Action values are calculated as the average return for each state-action pair over the 'n_episodes' episodes.
        Use the get_history_returns function to get the returns for each state-action pair in each episode.
        Collect the returns for each state-action pair in a dictionary of dictionaries where the keys are states and
            the values are dictionaries of actions and their returns.
        After all episodes have been run, calculate the average return for each state-action pair.
        Return the action values as a dictionary of dictionaries where the keys are states and
            the values are dictionaries of actions and their values.
    '''

    # Initialize vars to store Sum of returns for each state-action pair
    # and number of visits for each state-action pair
    action_values_sum = defaultdict(lambda: defaultdict(float))
    action_visit_counts = defaultdict(lambda: defaultdict(int))

    # Create player objects
    player = PyGameRandomCombatPlayer("Player")
    opponent = PyGameComputerCombatPlayer("Computer")

    # Run all episodes
    for _ in range(n_episodes):
        # Get the returns for each state-action pair in each episode
        history = run_random_episode(player, opponent)
        history_returns = get_history_returns(history)

        # Update the sum of returns and visit counts for each state-action pair
        for state, actions_returns in history_returns.items():
            for action, return_ in actions_returns.items():
                action_values_sum[state][action] += return_
                action_visit_counts[state][action] += 1

    # Calculate the average return for each state-action pair
    action_values_avg = defaultdict(lambda: defaultdict(float))

    for state, action_returns in action_values_sum.items():
        for action, total_return in action_returns.items():
            # Get visit count
            visit_count = action_visit_counts[state][action]
            # Calculate average return for the pair
            # If the maximum visit count is zero, divided by 1
            action_values_avg[state][action] = total_return / max(visit_count, 1)

    # Return action values
    return action_values_avg


def get_optimal_policy(action_values):
    optimal_policy = defaultdict(int)
    for state in action_values:
        optimal_policy[state] = max(action_values[state], key=action_values[state].get)
    return optimal_policy


def test_policy(policy):
    print("policy")
    names = ["Legolas", "Saruman"]
    total_reward = 0
    for _ in range(100):
        player1 = PyGamePolicyCombatPlayer(names[0], policy)
        player2 = PyGameComputerCombatPlayer(names[1])
        players = [player1, player2]
        total_reward += sum(
            [reward for _, _, reward in run_episode(*players)]
        )
    return total_reward / 100


if __name__ == "__main__":
    action_values = run_episodes(10000)
    print(action_values)
    optimal_policy = get_optimal_policy(action_values)
    print("optimal_policy")
    print(optimal_policy)
    print(test_policy(optimal_policy))

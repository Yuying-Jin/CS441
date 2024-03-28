""" Create PyGameAIPlayer class here"""
import random

from src.lab4.lab4_solution import AiPlayer

from src.lab11.pygame_human_player import PyGameHumanCombatPlayer


class PyGameAIPlayer:
    def __init__(self) -> None:
        pass

    def selectAction(self, state):
        return ord(str(random.randint(0, 9)))


""" Create PyGameAICombatPlayer class here"""


class PyGameAICombatPlayer(PyGameHumanCombatPlayer):
    def __init__(self, name):
        super().__init__(name)
        self.ai_player = AiPlayer("Trustee")

    def weapon_selecting_strategy(self):
        # delegate the AI player to select weapon
        return self.ai_player.weapon_selecting_strategy()

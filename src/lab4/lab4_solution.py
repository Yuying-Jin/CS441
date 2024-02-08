'''
Lab 4: Rock-Paper-Scissor AI Agent

In this lab you will build one AI agent for the game of Rock-Paper-Scissors, that can defeat a few different kinds of 
computer players.

You will update the AI agent class to create your first AI agent for this course.
Use the precept sequence to find out which opponent agent you are facing, 
so that it can beat these three opponent agents:

    Agent Single:  this agent picks a weapon at random at the start, 
                   and always plays that weapon.  
                   For example: 2,2,2,2,2,2,2,.....

    Agent Switch:  this agent picks a weapon at random at the start,
                   and randomly picks a weapon once every 10 rounds.  
                   For example:  2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,...

    Agent Mimic:  this agent picks a weapon at random in the first round, 
                  and then always does what you did the previous round.  
                  For example:  if you played 1,2,0,1,2,0,1,2,0,...  
                   then this agent would play 0,1,2,0,1,2,0,1,2,...

Discussions in lab:  You don't know ahead of time which opponent you will be facing, 
so the first few rounds will be used to figure this out.   How?

Once you've figured out the opponent, apply rules against that opponent. 
A model-based reflex agent uses rules (determined by its human creator) to decide which action to take.

If your AI is totally random, you should be expected to win about 33% of the time, so here is the requirement:  
In 100 rounds, you should consistently win at least 85 rounds to be considered a winner.

You get a 0 point for beating the single agent, 1 points for beating the switch agent, 
and 4 points for beating the mimic agent.

'''

from rock_paper_scissor import Player
from rock_paper_scissor import run_game
from rock_paper_scissor import random_weapon_select
import random

class AiPlayer(Player):
    def __init__(self, name):
        super().__init__(name)
        self.initial_weapon = random_weapon_select()
        self.guess = -1

    def agent_single(self):
        return self.opponent_choices[0] % 3 - 2

    def agent_switch(self):
        return self.opponent_choices[-1] % 3 - 2 

    def agent_mimic(self):
        return self.my_choices[-1] % 3 - 2 
    
    def weapon_selecting_strategy(self):
        round_num = 5 # monitor the latest $round_num rounds of choices

        # first $round_num rounds, return random weapon
        if len(self.opponent_choices) < round_num:
            return random.randint(0, 2) 
        
        # already know what agent the opponent is applying
        if self.guess == 1:
            return self.agent_switch()
        if self.guess == 2:
            return self.agent_mimic()
        
        # if oppoent choices are static, guessing opponent is single agent
        if all(c == self.opponent_choices[0] for c in self.opponent_choices[-round_num:]):
            self.guess = 0 # guess single agent
            return self.agent_single()  
        
        # if opponent choice is not static and AI guessed oppentent is single agent before, 
        # opponent is switch agent
        if not all(c == self.opponent_choices[0] for c in self.opponent_choices[-round_num:]) and self.guess == 0:
            self.guess = 1 # guess switch agent
            print("++++++++ guess switch +++++++++")
            return self.agent_switch()
        
        # if opponent choice is dynamic, opponent is mimic agent
        if not all(c == self.opponent_choices[0] for c in self.opponent_choices[-round_num:]):
            self.guess = 2 
            print("++++++++ guess mimic +++++++++")
            return self.agent_mimic()


if __name__ == '__main__':
    final_tally = [0]*3
    for agent in range(3):
        for i in range(100):
            tally = [score for _, score in run_game(AiPlayer("AI"), 100, agent)]
            if sum(tally) == 0:
                final_tally[agent] = 0
            else:
                final_tally[agent] += tally[0]/sum(tally)

    print("Final tally: ", final_tally)  
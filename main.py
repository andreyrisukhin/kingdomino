"""
Purpose: initial file for creating and running the monte carlo tree search to play kingdomino.
"""

from kingdomino import *
from mctsking import *


gm = GameManager(cardpath="./cards.txt")
players = [Player(), Player(), Player(), Player(strategy='mcts')]
scores = gm.new_game()

# game_outcomes = []
# n = 100
# for i in range(n):
#     gi_scores = gm.new_game()
#     game_outcomes.append(gi_scores)

# print(f'Outcomes from {n} games')
# print(game_outcomes)

"""
Analysis of scores
"""
# for g in game_outcomes:
#     total_score = sum(g)
#     print(total_score)



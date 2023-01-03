"""
Monte Carlo Tree Search.
Kingdomino player strategy in style of AlphaGo.
"""

"""
Monte carlo tree search first trains, and then plays.
> Save the trained state somewhere


Recall Thompson Sampling worked better in CSE 312 on HW. 

"""

"""
Theoretical calculations
Game depth d: 48 cards / 4 players = 12 turns.
Game breadth b: Max legal moves possible: 8 moves per 2x2 segment * (4*4-1) 2x2 segments = 8*15=120

b^d possible moves at most (overestimate) = 120^12 = 8.91610045E24

Pretty large

Oh, and also, claiming is strategy, up to 4 choice per turn. 


Two principles can reduce effective search space:
> Depth: Positional evaluation, truncate and replace subtree with value approximation function.
> Breadth: Sample from Policy p(a|s) distribution over legal moves a in state s.
    - Monte Carlo rollouts: search to max depth w/o branching, sample long sequences of actions for all players.
        * Effective to average over these rollouts, seen in backgammon and Scrabble.
    - Monte Carlo Tree Search (MCTS) uses rollouts to estimate value. With more simulation, accuracy improves.
    - Asymptotic policy convergence to optimal play and evaluation to optimal value function. 
    - AlphaGo noted prior work had linear feature combinations (shallow) for policy and value functions.
    - AlphaGo used value network and policy network

However, would Kingdomino benefit from reduced depth? Already small, and fixed depth game.

# TODO Future work, after Monte Carlo rollout/playout, try nonlinear feature combinations

"""

"""
{{I did this with Simple Machine Learning project in high school :) }}

Pure Monte Carlo Game/Tree Search has rounds of 4 steps:
1) Selection - start at root, select children until reach leaf. 
    Root R is current game state, leaf L is any node with a child that had no simulation (playout) yet.
    Clever selection, for example with Thompson sampling, is better
2) Expansion
    Unless L ends the game, create 1+ child nodes (valid moves from L), choose node C from them. 
3) Simulation
    Complete 1 random playout from node C. 
    Simple: choose uniform random moves until game end.
4) Backpropagation
    Use playout result to update information in nodes on path from C to R. 

Rounds are repeated while time remains, then the move with most simulations made (highest denominator) is chosen.

Playout k games, record scores, move leading to best score is played. Converges to optimal play (k->inf) in board filling games with random turn order (Hex, Kingdomino).
AlphaZero replaces simulation step with evaluation based on a neural network.
"""

"""
Per wikipedia and their sources suggestion: Choose moves (in each node of game tree) with maximum (wi/ni) + c*sqrt(ln(Ni)/ni).
    wi = # wins for node considered after ith move
    ni = # simulations for the node considered after ith move
    Ni = total # simulations after ith move run by the parent of the node considered
    c = exploration parameter, theoretically sqrt(2), empirically chosen.
    Formula is [exploit] + [explore]

Beware of pruning moves that would have later led to significant outcome difference
"""

"""
Improvements:
# TODO
Priors
Progressive bias
Rapid Action Value Estimation (<- interesting, for when multiple permutations of move sequence leads to same position)

"""


"""
Wikipedia, their authors, ai-boson.github.io
"""

import numpy as np
from collections import defaultdict

from kingdomino import *

"""
Tree looks like:
> Place Castle
Loop
    - Claim card
    - Place card
"""
class MonteCarloTreeSearchNode():
    def __init__(self, state:Board, parent=None, parent_action=None):
        self.state = state # Board state
        self.parent = parent # Root has no parent
        self.parent_action = parent_action 
        self.children = [] # Legal moves
        self._number_of_visits = 0
        self._results = defaultdict(int) # TODO learn about this
        self._results[1], self._results[-1] = 0
        self._untried_actions = None # Legal moves remaining to try
        self._untried_actions = self.untried_actions()

    def untried_actions(self):
        self._untried_actions = self.state.get_legal_actions() # Replace this with forking for either claim or place
        return self._untried_actions

    def q(self): # TODO more descriptive name? Or is this common
        wins = self._results[1]
        losses = self._results[-1]
        return wins - losses 

    def n(self):
        return self._number_of_visits

    def expand(self):
        action = self._untried_actions.pop()
        next_state = self.state.move(action)
        child_node = MonteCarloTreeSearchNode(
            next_state, parent=self, parent_action=action
        )
        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        return self.state.is_game_over()

    def rollout(self):
        """ Fully simulate a game. Return outcome. """
        current_rollout_state = self.state 

        while not current_rollout_state.is_game_over(): # TODO this is likely a typo bug
            possible_moves = current_rollout_state.get_legal_actions()
            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.move(action)
        
        return current_rollout_state.game_result()

    def backpropagate(self, result):
        self._number_of_visits += 1
        self._results[result] += 1
        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        return len(self._untried_actions) == 0

    def best_child(self, c_param=0.1):
        choices_weights = (c.q() / c.n()) + c_param * np.sqrt(2 * np.log(self.n() / c.n()))
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]

    def _tree_policy(self):
        """ Selects the node on which to run rollout. """
        current_node = self
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded(): # TODO could improve boolean semantics here
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

    def best_action(self):
        simulation_n = 100 # TODO adjust this by tuning, make it easier to access
        for i in range(simulation_n):
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)
        return self.best_child(c_param=0)

    def get_legal_actions(self):
        pass # TODO from KD
    
    def is_game_over(self):
        pass # TODO from KD

    def game_result(self):
        pass # TODO from KD

    def move(self, action):
        pass # TODO from KD

def main():
    root = MonteCarloTreeSearchNode(state=inital_state)
    selected_node = root.best_action()











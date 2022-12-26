"""
Purpose: initial file for creating and running the monte carlo tree search to play kingdomino.
"""

"""
Monte carlo tree search first trains, and then plays.
> Save the trained state somewhere


Recall Thompson Sampling worked better in CSE 312 on HW. 

"""

"""
TODO List
1) Data structure to represent maps
2) Score function, get score of a map
"""

import numpy as np

rng = np.random.default_rng()

cards = {}


# Consider representing as tuple (immutable) of ("area code", crown_int)
# If could have a keyarg tuple, best
# TODO ^

class Domino():
    def __init__(self, id:int, area_1:str, crowns_1:int, area_2:str, crowns_2:int):
        self.id = id
        self.area_1, self.crowns_1 = area_1, crowns_1
        self.area_2, self.crowns_2 = area_2, crowns_2

    def __repr__(self):
        return f"Card {self.id}: {self.area_1} {self.crowns_1} {self.area_2} {self.crowns_2}"

    def get_id(self):
        return self.id

    def get_face_1(self):
        return f'{self.area_1}'

class Board():
    """
    Represent a player's Kingdomino board.
        'x' is an empty space.
        'castle' is the player's castle, 1x1.
        Other characters are of form "<area id> <crown count>".
    Has methods to interact, with logic to allow legal moves.
    """
    def __init__(self):
        self.grid = [['x' for i in range(5)] for i in range(5)]
        self.has_castle = False

    def get_grid(self):
        return self.grid # TODO return a copy, not a reference

    def put_castle(self, row:int, col:int):
        """
        Place the castle at coordinates (row, col).
        Update internal castle variable, precondition to playable game.
        """
        self.grid[row][col] = 'castle'
        self.has_castle = True

    def put_domino(self, d:Domino, r1:int, c1:int, r2:int, c2:int):
        """
        Place domino d on grid.
            Area 1 specified by (row 1, col 1), area 2 by (r2,c2).
        """
        pass 



def create_card_map(filepath):
    """
    Takes the filepath to create the cards from.
    Returns a map of card IDs (as in game) to card faces.
    """
    cards = {}
    with open(file=filepath, mode='r') as f:
        contents = f.readlines()
        header = contents[0]
        card_list = contents[1:]
        print(f'header: {header}')
        print(f'card_list: {card_list}')

        # Process the file
        for line in card_list:
            id, card = line.split(" ", maxsplit=1)
            card, _ = card.split("\n")
            a1, c1, a2, c2 = card.split(" ", maxsplit=3)
            cards[id] = Domino(id, area_1=a1, crowns_1=c1, area_2=a2, crowns_2=c2)

    return cards

def shuffle(num_cards):
    """
    Takes an int representing the total number of cards.
    Returns a random sequence of card IDs.
    """
    deck = np.arange(start=1, stop=num_cards)
    shuffled = rng.permutation(deck)
    return shuffled


# cards = create_card_map("./cards.txt")
# print(cards)

b = Board()
print(b.get_grid())




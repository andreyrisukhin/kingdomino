"""
Purpose: initial file for creating and running the monte carlo tree search to play kingdomino.
"""

"""
Monte carlo tree search first trains, and then plays.
> Save the trained state somewhere


Recall Thompson Sampling worked better in CSE 312 on HW. 

"""

from kingdomino import *

# TODO DELETE THESE, DUPLICATED IN GAME MANAGER
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
            cards[int(id)] = Domino(id, area_1=a1, crowns_1=int(c1), area_2=a2, crowns_2=int(c2))
    return cards

def shuffle(num_cards):
    """
    Takes an int representing the total number of cards.
    Returns a random sequence of card IDs.
    """
    deck = np.arange(start=1, stop=num_cards)
    shuffled = rng.permutation(deck)
    return shuffled

# === Local Testing Below ====

# cards = create_card_map("./cards.txt")
# shuffled = shuffle(len(cards))
# print(cards[shuffled[0]])

# print(shuffled[:4])
# print(sorted(shuffled[:4]))

# b = Board()
# print(b)
# # b.put_castle(2,2)
# b.put_castle(4,4)
# print(b)

# for i in range(12):
#     di = cards[shuffled[i]]
#     di_places = b.get_legal_coords(di)

#     if not di_places == []: # Otherwise if no legal moves, skip placing this card
#         b.put_domino(di, di_places[0])

#     print(f'di: {di}')
#     print(f'{len(di_places)} moves')
#     print(b)

# print(b.get_score())


gm = GameManager(cardpath="./cards.txt")

game_outcomes = []
n = 100
for i in range(n):
    gi_scores = gm.new_game()
    game_outcomes.append(gi_scores)

print(f'Outcomes from {n} games')
print(game_outcomes)
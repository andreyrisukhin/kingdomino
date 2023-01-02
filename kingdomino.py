"""
This file contains all Kingdomino-related code.
Game logic, management, turn order all go here.
"""
"""
TODO List
> Domino selection process with multiple (4) players
"""

import numpy as np
rng = np.random.default_rng()

from collections import namedtuple
Face = namedtuple('Face', 'area crowns')
# Could make the domino a namedtuple too, face1 and face2
# Coord = namedtuple('Coord', 'r1 c1 r2 c2') # TODO is this useful?
Claim = namedtuple('Claim', 'pid domino')

class Domino():
    """
    Stores two faces, each a tuple of (area_code:str, crown_count:int).
    """
    def __init__(self, id:int, area_1:str, crowns_1:int, area_2:str, crowns_2:int):
        self.id = id
        self.face_1 = Face(area_1, crowns_1)
        self.face_2 = Face(area_2, crowns_2)

    def __repr__(self):
        """ Noticed that printing domino ID was not useful. """
        s = f'{self.face_1.area}{self.face_1.crowns} {self.face_2.area}{self.face_2.crowns}'
        return s

    def get_id(self):
        return self.id

    def get_face_1(self):
        return self.face_1

    def get_face_2(self):
        return self.face_2


class Board():
    """
    Represent a player's Kingdomino board.
        'x' is an empty space.
        'castle' is the player's castle, 1x1.
        Other characters are of form "<area id> <crown count>".
    Has methods to interact, with logic to allow legal moves.
    Can calculate score.

    Currently supports square boards only.
    """
    def __init__(self, size:int = 5):
        self.size = size
        self.EMPTY = 'x'
        self.CASTLE = 'c'
        self.grid = [[Face(self.EMPTY, 0) for i in range(size)] for i in range(size)]
        self.has_castle = False

    def __repr__(self):
        """ Return a human-friendly picture of the board. """
        s = ''
        for row in self.grid:
            for col in row:
                s += f'{col.area}{col.crowns} '
            s += '\n'
        return s

    def put_castle(self, row:int, col:int):
        """
        Place the castle at coordinates (row, col).
        Update internal castle variable, precondition to playable game.
        """
        assert 0 <= row and row < 5 and 0 <= col and col < 5, "Out of Board Castle Request"
        self.grid[row][col] = Face(self.CASTLE, 0)
        self.has_castle = True

    # TODO possible to make this private? Maybe get a copy of grid locally to sever "self" usage
    # TODO clean this logic
    def get_legal_covering_ij(self, d:Domino, i:int, j:int):
        """
        Given domino d and coordinates i,j, return list of valid placements of the 
            domino covering this space (r1,c1,r2,c2).
        """
        assert 0 <= i and i < 5 and 0 <= j and j < 5, "Out of Board legality query"
        f1 = d.get_face_1()
        f2 = d.get_face_2()
        out_coords = []
        if self.grid[i][j].area == self.EMPTY:
            # print("empty!")
            # Check if f1 can be placed at i,j
            if ((0 <= i-1 and (self.grid[i-1][j].area == f1.area or self.grid[i-1][j].area == self.CASTLE)) or 
                    (i+1 < 5 and (self.grid[i+1][j].area == f1.area or self.grid[i+1][j].area == self.CASTLE)) or 
                    (0 <= j-1 and (self.grid[i][j-1].area == f1.area or self.grid[i][j-1].area == self.CASTLE)) or 
                    (j+1 < 5 and (self.grid[i][j+1].area == f1.area or self.grid[i][j+1].area == self.CASTLE))): 
                # f1 can be placed! Is there room for f2?
                if 0 <= i-1 and self.grid[i-1][j].area == self.EMPTY: 
                    out_coords.append((i,j,i-1,j))
                if i+1 < 5 and self.grid[i+1][j].area == self.EMPTY: 
                    out_coords.append((i,j,i+1,j))
                if 0 <= j-1 and self.grid[i][j-1].area == self.EMPTY: 
                    out_coords.append((i,j,i,j-1))
                if j+1 < 5 and self.grid[i][j+1].area == self.EMPTY: 
                    out_coords.append((i,j,i,j+1))
            # Try f2 at coords
            if ((0 <= i-1 and (self.grid[i-1][j].area == f2.area or self.grid[i-1][j].area == self.CASTLE)) or 
                    (i+1 < 5 and (self.grid[i+1][j].area == f2.area or self.grid[i+1][j].area == self.CASTLE)) or 
                    (0 <= j-1 and (self.grid[i][j-1].area == f2.area or self.grid[i][j-1].area == self.CASTLE)) or 
                    (j+1 < 5 and (self.grid[i][j+1].area == f2.area or self.grid[i][j+1].area == self.CASTLE))): 
                # f2 can be placed! Is there room for f1?
                if 0 <= i-1 and self.grid[i-1][j].area == self.EMPTY: 
                    out_coords.append((i-1,j,i,j))
                if i+1 < 5 and self.grid[i+1][j].area == self.EMPTY: 
                    out_coords.append((i+1,j,i,j))
                if 0 <= j-1 and self.grid[i][j-1].area == self.EMPTY: 
                    out_coords.append((i,j-1,i,j))
                if j+1 < 5 and self.grid[i][j+1].area == self.EMPTY: 
                    out_coords.append((i,j+1,i,j))
        return out_coords

    def get_legal_coords(self, d:Domino):
        """
        Return list of coordinates to place this domino on the board legally.
            Return empty list if no locations are valid.
                If no locations valid, interpreted as the option to skip this piece by future methods.
        """
        assert self.has_castle, "Castle must be placed before dominoes."
        """
        Legal Coordinates are
            (1) Adjacent to existing pieces
            (2) Have at least one face of domino match adjacent face (or castle)
        """
        out_coords = []
        for i, row in enumerate(self.grid):
            for j, element in enumerate(row):
                legal_covering = self.get_legal_covering_ij(d, i, j)
                # print(legal_covering)
                out_coords += legal_covering
        return out_coords

    # TODO how to type check?
    def put_domino(self, d:Domino, coord): #:tuple(int,int,int,int) #r1:int, c1:int, r2:int, c2:int
        """
        Place domino d on grid.
            Face 1 specified by (row 1, col 1), face 2 by (r2,c2).
        """
        r1, c1, r2, c2 = coord
        assert 0 <= r1 and r1 < 5 and 0 <= c1 and c1 < 5, "Out of Board Face 1 coords"
        assert 0 <= r2 and r2 < 5 and 0 <= c2 and c2 < 5, "Out of Board Face 2 coords"
        legal_moves = self.get_legal_coords(d)
        if coord in legal_moves:
            self.grid[r1][c1] = d.get_face_1()
            self.grid[r2][c2] = d.get_face_2()
        else:
            print(f'Illegal attempt to place {d} at {coord}')

    def get_score(self):
        """
        Returns an int score.
        Score calculated: (count adjacent faces of same type) * (crown count in that region).
        """
        to_search_mask = [[1 for i in range(self.size)] for i in range(self.size)] # 1: to search, 0: already searched

        def recur_search(i,j, area_type):
            """
            Given coords and an area type to match.
            Return (island size, crown count).
            """
            if (i < 0 or j < 0 or i >= self.size or j >= self.size
                    or to_search_mask[i][j] == 0 or not area_type == self.grid[i][j].area):
                return 0,0
            else:
                to_search_mask[i][j] = 0
                tiles_up, crowns_up = recur_search(i-1,j, area_type)
                tiles_down, crowns_down = recur_search(i+1,j, area_type)
                tiles_left, crowns_left = recur_search(i,j-1, area_type)
                tiles_right, crowns_right = recur_search(i,j+1, area_type)
                tiles = 1 + tiles_up + tiles_down + tiles_left + tiles_right
                crowns = self.grid[i][j].crowns + crowns_up + crowns_down + crowns_left + crowns_right
                return tiles, crowns
        """
        Had an interesting bug here: score calculation should happen at each island, 
            I calculated outside loops globally which was total tiles * total crowns.
        """
        score = 0
        for i in range(self.size):
            for j in range(self.size): # NOTE rely on square grid assumption
                if to_search_mask[i][j] == 1:
                    tiles_ij, crowns_ij = recur_search(i, j, area_type=self.grid[i][j].area)
                    score += tiles_ij * crowns_ij
        return score 


class GameManager():
    """
    This class manages user interaction with Kingdomino.
    """
    """
    Given the path to the text file containing Kingdomino cards.
    """
    def _create_card_map(self, filepath):
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

    def _shuffle(self, num_cards):
        """
        Takes an int representing the total number of cards.
        Returns a random sequence of card IDs.
        """
        deck = np.arange(start=1, stop=num_cards)
        shuffled = rng.permutation(deck)
        return shuffled

    def __init__(self, cardpath:str):
        self.cardpath = cardpath
        self.card_dict = self._create_card_map(self.cardpath)

    def new_game(self):
        """
        Manages a game.
        """
        shuffled_ids = self._shuffle(len(self.card_dict))
        shuffled_deck = []
        for card_id in shuffled_ids:
            shuffled_deck.append(self.card_dict[card_id])

        players = [Player(), Player(), Player(), Player()]
        g = Game(deck=shuffled_deck, players=players)

        # g.earlyGame()

        # g.midGame()
            
        # g.endGame()

class Player():
    """
    The decisions and logic in how a player chooses moves.
    Play procedures include: firstvalid, random, consoleinput, 
        and eventually markovtree, rnn

    The Player does NOT modify boards passed as fields. Instead,
        sends commands to the Game to modify boards.
    """
    def __init__(self, strategy:str="firstvalid"):
        self.strat = strategy

    def found(self, b:Board):
        """ Return coords to place castle, founding kingdom. """
        if self.strat == "firstvalid": return self._found_firstval(b)
        else: print("error founding, no matching strategy")

    def claim(self, choices, b:Board):
        """ Returns claimed idx from the list of choices. """
        if self.strat == "firstvalid": return self._claim_firstval(choices, b)
        else: print("error claiming, no matching strategy")

    def place(self, d:Domino, b:Board):
        """ Plays the domino on the board. Returns a placement from the list of possible spaces. """
        if self.strat == "firstvalid": return self._place_firstval(d, b)
        else: print("error placing, no matching strategy")

    def _found_firstval(self, b:Board): return 0,0

    def _claim_firstval(self, choices, b:Board): return 0

    def _place_firstval(self, d:Domino, b:Board):
        d_places = b.get_legal_coords(d)
        if not d_places == []: # If valid place exists
            return d_places[0]
        else: # If no placement existed, the domino was discarded
            return None

    # TODO continue strategies

class Game():
    """
    Represents a single game, allows for interaction with boards.
    """
    def __init__(self, deck, players, n_players:int=4):
        assert n_players == len(players), f"Was given {len(players)} players when expecting {n_players}"
        self.n_players = n_players
        self.players = players # List of Player()
        self.boards = [] # p_i's board is at boards[i]
        for p in range(n_players):
            self.boards.append(Board())
        self.deck = deck # A list of Card structs
        self.isOver = False
        self.upcoming = [] # Stores unclaimed cards
        self.claimed = [] # Stores Claim(pid, domino)
        # Upcoming cards in sorted batches of 4
        self.upcoming = self.deck[:4]
        self.upcoming.sort()
        self.deck = self.deck[4:] # Remove from deck
        # Game initializes in player order
        # TODO above, change this to add optionality
        for i, d in enumerate(self.upcoming):
            self.claimed.append(Claim(i, d))
        self.upcoming = []
        print("Players autoclaimed dominos in order")

    def isPlaying(self):
        return not self.isOver

    def play(self):
        print("Placing castles.")
        for i, p in enumerate(self.players):
            print(f'  Player {i} to place castle.')
            found_xy = p.found(self.boards[i])
            self.boards[p].put_castle(found_xy)

        print("Midgame begins")
        print("--------------")

        while not self.deck == []:
            print("Laying cards")
            # Upcoming cards in sorted batches of 4
            self.upcoming = self.deck[:4]
            self.upcoming.sort()
            self.deck = self.deck[4:] # Remove from deck
            new_claims = [None, None, None, None] # Temporary storage 
            for lc in self.claimed: # lc := last claimed
                pi = lc.pid
                p = self.players[lc.pid]
                print(f"  Player {pi} to claim.")
                nc_i = p.claim(self.upcoming, self.boards[pi])
                nc_d = self.upcoming[nc_i]
                new_claims[nc_i] = Claim(pi, nc_d)
                self.upcoming.remove(nc_d) # Remove claimed piece from possible list

                print(f"    Player {pi} to place.")
                xy = p.place(nc_d, self.boards[i])
                self.boards[pi].put_domino(nc_d, xy)
            self.claimed = new_claims

        print("Endgame: Place final claims and tally score.")
        # TODO deduplicate this code
        for lc in self.claimed: # lc := last claimed
                pi = lc.pid
                p = self.players[lc.pid]
                print(f"  Player {pi} to claim.")
                nc_i = p.claim(self.upcoming, self.boards[pi])
                nc_d = self.upcoming[nc_i]
                new_claims[nc_i] = Claim(pi, nc_d)
                self.upcoming.remove(nc_d) # Remove claimed piece from possible list

                print(f"    Player {pi} to place.")
                xy = p.place(nc_d, self.boards[i])
                self.boards[pi].put_domino(nc_d, xy)
        self.claimed = []

        print(f'Final Scores')
        for i,p in enumerate(self.players):
            score_i = self.boards[i].get_score()
            print(f'  Player {i}: {score_i}')


    # TODO add features of UI for possible moves
# TODO discard a domino if cannot put anywhere
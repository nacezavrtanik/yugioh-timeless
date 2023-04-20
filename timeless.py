"""Module for running the Yugioh TIMELESS tournament format."""

import numpy as np
import interface


WINS = 'Wins'
DUELIST = 'Duelist'
PLACE = 'Place'
POINTS = 'Points'

ROUNDS = (0, 1, 2, 3)
PRELIMINARY_ROUNDS = (0, 1, 2)
FINAL_ROUND = 3
PAIRING_CONFIGURATIONS = ([0, 1, 2, 3], [1, 3, 0, 2], [3, 0, 1, 2])
STANDING_CONFIGURATIONS = {
    0: {
        WINS: ([1, 1, 0, 0], ),
        PLACE: ([1, 1, 3, 3], ),
        POINTS: (None, )
    },
    1: {
        WINS: ([2, 2, 0, 0], [2, 1, 1, 0], [1, 1, 1, 1]),
        PLACE: ([1, 1, 3, 3], [1, 2, 2, 4], [1, 1, 1, 1]),
        POINTS: (None, None, None)
    },
    2: {
        WINS: ([3, 2, 1, 0], [2, 2, 1, 1], [3, 1, 1, 1], [2, 2, 2, 0]),
        PLACE: ([1, 2, 3, 4], [1, 1, 3, 3], [1, 2, 2, 2], [1, 1, 1, 4]),
        POINTS: (None, None, None, None)
    },
    3: {  # final round if NO TIE after preliminaries
        WINS: ([4, 2, 2, 0], [4, 2, 1, 1], [3, 3, 2, 0], [3, 3, 1, 1], [3, 2, 2, 1]),
        PLACE: ([1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]),
        POINTS: ([10, 6, 4, 0], [10, 6, 3, 1], [9, 7, 4, 0], [9, 7, 3, 1], [9, 6, 4, 1])
    },
    4: {  # final round IF TIE after preliminaries
        WINS: ([4, 2, 1, 1], [3, 3, 2, 0], [3, 2, 2, 1]),
        PLACE: ([1, 2, 3, 3], [1, 1, 3, 4], [1, 2, 2, 4]),
        POINTS: ([10, 6, 2, 2], [8, 8, 4, 0], [9, 5, 5, 1])
    }
}
TIED_WIN_CONFIGURATIONS_AFTER_PRELIMINARIES = ([3, 1, 1, 1], [2, 2, 2, 0])
IS_TIED_AFTER_PRELIMINARIES = None


class Duelist:
    """Track duelists and scores in the Yugioh TIMELESS tournament format.

    Attributes
    ----------
    name : str
        Name of the duelist.
    wins : int
        Number of duels won.
    """

    def __init__(self, name, wins=0):
        """Create instance of Duelist class.

        Parameters
        ----------
        name : str
            Name of duelist.
        wins : int, optional
            Number of wins.
            (defaults to 0)

        Examples
        --------
        >>> duelist = Duelist('Amadeus', wins=1)
        >>> print(duelist)
        Amadeus
        """
        self.name = name
        self.wins = wins

    def __repr__(self):
        """Return repr(self)."""
        return f'Duelist(\'{self.name}\', wins={self.wins})'

    def __str__(self):
        """Return str(self)."""
        return self.name

    def __lt__(self, other):
        """Return self < other."""
        if isinstance(other, Duelist):
            return self.wins < other.wins
        else:
            return NotImplemented

    def __eq__(self, other):
        """Return self == other."""
        if isinstance(other, Duelist):
            return self is other
        elif isinstance(other, int):
            return self.wins == other
        elif isinstance(other, str):
            return self.name == other
        else:
            return NotImplemented


def enter_unique_duelists():
    """Return list of `Duelist` instances with unique `name` attributes.

    The user is asked to provide four duelist names. The user is prompted
    to keep repeating the process until there are no duplicate entries.

    Returns
    -------
    list
        List of four `Duelist` instances with unique `name` attributes.

    Examples
    --------
    >>> enter_unique_duelists()
    Duelist 1: >? Johann
    Duelist 2: >? Johann
    Duelist 3: >? Amadeus
    Duelist 4: >? Amadeus
    You've entered some duplicate names: Johann, Amadeus.
    Please try again.
    Duelist 1: >? Johann S
    Duelist 2: >? Johann C
    Duelist 3: >? Amadeus
    Duelist 4: >? Falco
    [Duelist('Johann S', wins=0), Duelist('Johann C', wins=0), Duelist('Amadeus', wins=0), Duelist('Falco', wins=0)]
    """

    while True:

        duelist_candidates = [
            Duelist(interface.supervised_input(f'Duelist {i + 1}: ', ['alphabetical', 'less_than_25_characters']))
            for i in range(4)]
        candidate_names = [duelist_candidates[i].name for i in range(4)]

        duplicate_names = {name for name in candidate_names if candidate_names.count(name) > 1}

        if duplicate_names:
            duplicate_names_string = duplicate_names.__str__()[1: -1].replace('\'', '')
            print(f'You\'ve entered some duplicate names: {duplicate_names_string}.\nPlease try again.')
            continue

        return duelist_candidates


def enter_tournament_information():

    deck_sets = {'BASIC': ['Beast', 'Chaos', 'Dragon', 'Spellcaster'],
                 'EXTRA': ['Dinosaur', 'Flip', 'Warrior', 'Zombie']}

    interface.segments.get('format')()
    format_ = interface.supervised_input('Choose format: ', 'choose_from', options=['Basic', 'Extra']).upper()
    decks = deck_sets.get(format_)
    interface.segments.get('entry_fee')()
    entry_fee = int(interface.supervised_input('Set entry fee: ', ['integer', 'multiple_of_10']))
    interface.segments.get('duelists')()
    duelists = np.random.permutation(enter_unique_duelists())

    tournament_information = {'decks': decks, 'entry_fee': entry_fee, 'duelists': duelists}

    return tournament_information


def random_timeless_square():
    """Randomly generate a Timeless square.

    Keeps randomly generating squares until a Timeless sqaure is generated.

    Returns
    -------
    numpy.ndarray
        Timeless square.

    Notes
    -----
    Timeless squares are 4x4 arrays that are isomorphic to Latin squares.
    They are used to model matchups in the Yugioh TIMELESS tournament format.

    Note that results are not repeatable, as fixing a random seed would result
    in the initial random square being created over and over, creating a loop.

    Examples
    --------
    >>> random_timeless_square()
    array([[2, 0, 1, 3],
           [3, 1, 2, 0],
           [2, 0, 3, 1],
           [1, 3, 2, 0]])
    """

    while True:

        random_square = np.array([np.random.permutation(4) for _ in range(4)])

        unique_diagonal = len(set(random_square.diagonal())) == 4
        unique_antidiagonal = len(set(np.fliplr(random_square).diagonal())) == 4
        unique_offdiagonal = len({random_square[0, 1], random_square[1, 0],
                                  random_square[2, 3], random_square[3, 2]}) == 4

        is_timeless = unique_diagonal and unique_antidiagonal and unique_offdiagonal

        if is_timeless:
            return random_square


def check_if_tied_after_preliminaries(duelists):
    """Set global constant `IS_TIED_AFTER_PRELIMINARIES`."""
    duelists_by_wins = sorted(duelists, reverse=True)
    global IS_TIED_AFTER_PRELIMINARIES
    IS_TIED_AFTER_PRELIMINARIES = duelists_by_wins in TIED_WIN_CONFIGURATIONS_AFTER_PRELIMINARIES


def generate_pairings(duelists, decks, matchup, round_):

    if round_ == FINAL_ROUND:
        check_if_tied_after_preliminaries(duelists)

    if round_ in PRELIMINARY_ROUNDS:
        x, y, z, w = PAIRING_CONFIGURATIONS[round_]
        deck_x, deck_y, deck_z, deck_w = [decks[matchup[x, y]], decks[matchup[y, x]],
                                          decks[matchup[z, w]], decks[matchup[w, z]]]
    elif round_ == FINAL_ROUND and IS_TIED_AFTER_PRELIMINARIES:
        x, y, z, w = PAIRING_CONFIGURATIONS[np.random.choice(PRELIMINARY_ROUNDS)]
        deck_x, deck_y, deck_z, deck_w = [decks[matchup[x, x]], decks[matchup[y, y]],
                                          decks[matchup[z, z]], decks[matchup[w, w]]]
    else:
        x, y, z, w = np.flip(np.argsort(duelists))
        deck_x, deck_y, deck_z, deck_w = [decks[matchup[x, x]], decks[matchup[y, y]],
                                          decks[matchup[z, z]], decks[matchup[w, w]]]

    duelist_x, duelist_y, duelist_z, duelist_w = [duelists[i] for i in [x, y, z, w]]

    pairings = [[f'{duelist_x} ({deck_x})', 'VS', f'{duelist_y} ({deck_y})'],
                [f'{duelist_z} ({deck_z})', 'VS', f'{duelist_w} ({deck_w})']]
    interface.segments.get('pairings')(pairings, round_)

    return duelist_x, duelist_y, duelist_z, duelist_w


def register_wins(duelist_x, duelist_y, duelist_z, duelist_w):

    winner_xy = interface.supervised_input(f'Who won, {duelist_x} or {duelist_y}? ',
                                           'choose_from', options=[duelist_x.name, duelist_y.name])
    winner_zw = interface.supervised_input(f'Who won, {duelist_z} or {duelist_w}? ',
                                           'choose_from', options=[duelist_z.name, duelist_w.name])

    winner_xy, loser_xy = [duelist_x, duelist_y] if duelist_x == winner_xy else [duelist_y, duelist_x]
    winner_zw, loser_zw = [duelist_z, duelist_w] if duelist_z == winner_zw else [duelist_w, duelist_z]

    winner_xy.wins += 1
    winner_zw.wins += 1

    return winner_xy, loser_xy, winner_zw, loser_zw


def display_standings(winners_and_losers, round_, entry_fee):

    if round_ == FINAL_ROUND:
        round_ += IS_TIED_AFTER_PRELIMINARIES

    duelists_by_wins = sorted(winners_and_losers, reverse=True)
    config = STANDING_CONFIGURATIONS.get(round_).get(WINS).index(duelists_by_wins)

    if round_ in PRELIMINARY_ROUNDS or IS_TIED_AFTER_PRELIMINARIES:
        duelists_by_place = duelists_by_wins
    else:
        duelists_by_place = winners_and_losers

    standings = {PLACE: STANDING_CONFIGURATIONS.get(round_).get(PLACE)[config],
                 DUELIST: duelists_by_place,
                 WINS: STANDING_CONFIGURATIONS.get(round_).get(WINS)[config],
                 POINTS: STANDING_CONFIGURATIONS.get(round_).get(POINTS)[config]}
    interface.segments.get('standings')(standings, round_)


def timeless(duelists, decks, entry_fee):

    interface.segments.get('start')()
    matchup = random_timeless_square()

    for round_ in ROUNDS:
        pairings = generate_pairings(duelists, decks, matchup, round_)
        winners_and_losers = register_wins(*pairings)
        display_standings(winners_and_losers, round_, entry_fee)


def main():

    interface.segments.get('initial')()
    timeless(**enter_tournament_information())
    interface.segments.get('final')()


if __name__ == '__main__':
    main()

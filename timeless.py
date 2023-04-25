"""Module for running the Yugioh TIMELESS tournament format."""

import numpy as np

import interface
from config import FORMATS, DECK_SETS, ROUNDS, PRELIMINARY_ROUNDS, FINAL_ROUND
from config import PAIRING_CONFIGURATIONS, TIED_WIN_CONFIGURATIONS_AFTER_PRELIMINARIES, STANDING_CONFIGURATIONS


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

    interface.segments.get('enter_format')()
    format_ = interface.supervised_input('Choose format: ', 'choose_from', options=FORMATS)
    interface.segments.get('enter_entry_fee')()
    entry_fee = int(interface.supervised_input('Set entry fee: ', ['integer', 'multiple_of_10']))
    interface.segments.get('enter_duelists')()
    duelists = np.random.permutation(enter_unique_duelists())
    interface.segments.get('enter_tournament_information_end')()

    tournament_information = {'format_': format_, 'entry_fee': entry_fee, 'duelists': duelists}

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

    interface.segments.get('generate_pairings')(pairings, round_)

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

    interface.segments.get('register_wins')()

    return winner_xy, loser_xy, winner_zw, loser_zw


def display_standings(winners_and_losers, round_, entry_fee):

    duelists_by_wins = sorted(winners_and_losers, reverse=True)
    key = round_ if round_ in PRELIMINARY_ROUNDS else round_ + IS_TIED_AFTER_PRELIMINARIES
    index = STANDING_CONFIGURATIONS.get(key).get('Wins').index(duelists_by_wins)

    if round_ in PRELIMINARY_ROUNDS or IS_TIED_AFTER_PRELIMINARIES:
        duelists_by_place = duelists_by_wins
    else:
        duelists_by_place = winners_and_losers

    standings = {'Place': STANDING_CONFIGURATIONS.get(key).get('Places')[index],
                 'Duelist': duelists_by_place,
                 'Wins': STANDING_CONFIGURATIONS.get(key).get('Wins')[index]}

    if round_ == FINAL_ROUND and entry_fee == 0:
        standings['Points'] = STANDING_CONFIGURATIONS.get(key).get('Points')[index]
    elif round_ == FINAL_ROUND and entry_fee != 0:
        entry_fee_unit = entry_fee // 5
        standings['Prize'] = map(
            lambda x: f'¤{x * entry_fee_unit}', STANDING_CONFIGURATIONS.get(key).get('Points')[index])

    interface.segments.get('display_standings')(standings, round_)


def timeless(duelists, format_, entry_fee):

    interface.segments.get('start')(format_)
    decks = DECK_SETS.get(format_)
    matchup = random_timeless_square()

    for round_ in ROUNDS:
        pairings = generate_pairings(duelists, decks, matchup, round_)
        winners_and_losers = register_wins(*pairings)
        display_standings(winners_and_losers, round_, entry_fee)

    interface.segments.get('end')(format_)


def main():

    interface.segments.get('initial')()
    timeless(**enter_tournament_information())
    interface.segments.get('final')()


if __name__ == '__main__':
    main()

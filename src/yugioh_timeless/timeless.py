"""Module containing the main functionality of the `yugioh-timeless` package."""

import random
import itertools

import yugioh_timeless.interface as interface
from yugioh_timeless.config import (
    VARIANTS, DECK_SETS, ROUNDS, PRELIMINARY_ROUNDS, FINAL_ROUND,
    PAIRING_CONFIGURATIONS, TIED_WIN_CONFIGURATIONS_AFTER_PRELIMINARIES,
    STANDING_CONFIGURATIONS,
)


IS_TIED_AFTER_PRELIMINARIES = None


def random_permutation(collection):
    """Return a random permutation of `collection`."""
    return random.choice(list(itertools.permutations(collection)))


class Duelist:
    """Handle duelist scores in the Yugioh TIMELESS tournament format.

    An instance of this class keeps track of the win count for a duelist.
    Another purpose of this class is to improve the readability of the
    `timeless` module by simplifying the syntax for both printing, and
    comparing instances of this class to instances of classes `Duelist`
    `int`, and `str`.

    Attributes
    ----------
    name : str
        Name of the duelist.
    wins : int
        Number of duels won.
    """

    def __init__(self, name, wins=0):
        """Create instance of the `Duelist` class.

        Parameters
        ----------
        name : str
            Name of duelist.
        wins : int, optional
            Number of wins.
            (defaults to 0)
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

    Notes
    -----
    As names are obtained with the function `interface.supervised_input`,
    they are first passed to the `string.capwords` function. Hence, the
    names 'Amadeus', 'amadeus', and ' aMaDEuS   ' are considered the same.
    """

    while True:

        duelist_candidates = [
            Duelist(interface.supervised_input(f'Duelist {i+1}: ', ['alphabetical', 'less_than_25_characters']))
            for i in range(4)]
        candidate_names = [duelist_candidates[i].name for i in range(4)]

        duplicate_names = sorted(list({name for name in candidate_names if candidate_names.count(name) > 1}))

        if duplicate_names:
            duplicate_names_string = str(duplicate_names).replace("'", "").replace("[", "").replace("]", "")
            interface.segment_enter_unique_duelists(duplicate_names_string)
            continue

        return duelist_candidates


def enter_tournament_information():
    """Prompt user to enter arguments for the `timeless` function.

    Returns
    -------
    dict
        Keys are 'variant', 'entry_fee', and 'duelists'. Used as input
        for the `timeless` function.
    """

    interface.segment_enter_variant()
    variant = interface.supervised_input('Choose a deck set: ', 'choose_from', options=VARIANTS)
    interface.segment_enter_entry_fee()
    entry_fee = int(interface.supervised_input('Set entry fee: ', ['integer', 'multiple_of_10', 'max_1000'],
                                               default_tip="Set to 0 for no entry fee."))
    interface.segment_enter_duelists()
    duelists = random_permutation(enter_unique_duelists())
    interface.segment_enter_tournament_information_end()

    tournament_information = {'variant': variant, 'entry_fee': entry_fee, 'duelists': duelists}

    return tournament_information


def random_timeless_square():
    """Randomly generate a Timeless square.

    Keeps randomly generating squares until a Timeless sqaure is generated.

    Returns
    -------
    list of list of int
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
    [(2, 0, 3, 1), (1, 0, 3, 2), (1, 0, 3, 2), (2, 0, 3, 1)]
    """

    while True:

        random_square = [random_permutation(range(4)) for _ in range(4)]

        unique_diagonal = len({random_square[i][i] for i in range(4)}) == 4
        unique_antidiagonal = len({random_square[i][3-i] for i in range(4)}) == 4
        unique_offdiagonal = len({random_square[i][j] for (i, j) in [(0, 1), (1, 0), (2, 3), (3, 2)]}) == 4

        is_timeless = unique_diagonal and unique_antidiagonal and unique_offdiagonal

        if is_timeless:
            return random_square


def check_if_tied_after_preliminaries(duelists):
    """Set global constant `IS_TIED_AFTER_PRELIMINARIES`."""
    duelists_by_wins = sorted(duelists, reverse=True)
    global IS_TIED_AFTER_PRELIMINARIES
    IS_TIED_AFTER_PRELIMINARIES = duelists_by_wins in TIED_WIN_CONFIGURATIONS_AFTER_PRELIMINARIES


def generate_pairings(duelists, decks, matchup, round_):
    """Generate and display pairings for given round.

    Parameters
    ----------
    duelists : list of Duelist
        Duelists that are participating in the tournament, as instances of the
        `Duelist` class. The order of the list matters and should not be
        changed over multiple calls of this function.
    decks : list of str
        Deck names. The order of the list matters and should not be changed
        over multiple calls of this function.
    matchup : list of list of int
        A Timeless square.
    round_ : {0, 1, 2, 3}
        Number of the round to generate pairings for.

    Returns
    -------
    tuple of Duelist
        Contains the same elements as the input list `duelists`, but is ordered
        in such a way as to represent the pairings, i.e. the first two duelists
        play against each other, and the last two duelists play against each
        other.

    Notes
    -----
    The input arguments for this function are intended to be passed from the
    scope of the `timeless` function.
    The elements of the output tuple of this function serve as input for the
    `register_wins` function.
    """

    if round_ == FINAL_ROUND:
        check_if_tied_after_preliminaries(duelists)

    if round_ in PRELIMINARY_ROUNDS:
        x, y, z, w = PAIRING_CONFIGURATIONS[round_]
        deck_x, deck_y, deck_z, deck_w = [decks[matchup[x][y]], decks[matchup[y][x]],
                                          decks[matchup[z][w]], decks[matchup[w][z]]]
    elif round_ == FINAL_ROUND and IS_TIED_AFTER_PRELIMINARIES:
        x, y, z, w = PAIRING_CONFIGURATIONS[random.choice(PRELIMINARY_ROUNDS)]
        deck_x, deck_y, deck_z, deck_w = [decks[matchup[x][x]], decks[matchup[y][y]],
                                          decks[matchup[z][z]], decks[matchup[w][w]]]
    else:
        x, y, z, w = tuple(duelists.index(duelist) for duelist in reversed(sorted(duelists, key=lambda x: x.wins)))
        deck_x, deck_y, deck_z, deck_w = [decks[matchup[x][x]], decks[matchup[y][y]],
                                          decks[matchup[z][z]], decks[matchup[w][w]]]

    duelist_x, duelist_y, duelist_z, duelist_w = [duelists[i] for i in [x, y, z, w]]

    pairings = [[f'{duelist_x} ({deck_x})', 'VS', f'{duelist_y} ({deck_y})'],
                [f'{duelist_z} ({deck_z})', 'VS', f'{duelist_w} ({deck_w})']]

    interface.segment_generate_pairings(pairings, round_)

    return duelist_x, duelist_y, duelist_z, duelist_w


def register_wins(duelist_x, duelist_y, duelist_z, duelist_w):
    """Register wins and return tuple of winners and losers.

    Parameters
    ----------
    duelist_x : Duelist
        First duelist of the first match.
    duelist_y : Duelist
        Second duelist of the first match.
    duelist_z : Duelist
        First duelist of the second match.
    duelist_w : Duelist
        Second duelist of the second match.

    Returns
    -------
    tuple of Duelist
        Elements are the input arguments, but ordered in such a way as to
        represent the outcome of the round, i.e. the winner of the first
        match, followed by the loser of the first match, followed by the
        winner of the second match, and finally the loser of the second match.

    Notes
    -----
    The input arguments for this function are intended to be generated with
    the `generate_pairings` function.
    The output tuple of this function serves as the first input argument for
    the `display_standings` function.
    """

    winner_xy = interface.supervised_input(f'Who won, {duelist_x} or {duelist_y}? ',
                                           'choose_from', options=[duelist_x.name, duelist_y.name])
    winner_zw = interface.supervised_input(f'Who won, {duelist_z} or {duelist_w}? ',
                                           'choose_from', options=[duelist_z.name, duelist_w.name])

    winner_xy, loser_xy = [duelist_x, duelist_y] if duelist_x == winner_xy else [duelist_y, duelist_x]
    winner_zw, loser_zw = [duelist_z, duelist_w] if duelist_z == winner_zw else [duelist_w, duelist_z]

    winner_xy.wins += 1
    winner_zw.wins += 1

    interface.segment_register_wins()

    return winner_xy, loser_xy, winner_zw, loser_zw


def display_standings(winners_and_losers, round_, entry_fee):
    """Display standings after given round.

    Standings for preliminary rounds are displayed as a table with columns
    Place, Duelist, and Wins. For the final round, an additional column is
    displayed, which is either Points (entry fee 0) or Prizes (non-zero entry
    fee).

    Parameters
    ----------
    winners_and_losers : tuple of Duelist
        Elements are: the winner of the first match, the loser of the first
        match, the winner of the second match, and the loser of the second
        match.
    round_ : {0, 1, 2, 3}
        Number of the round to display standings for.
    entry_fee : int
        The entry fee for the tournament in progress.

    Returns
    -------
    None

    Notes
    -----
    The first input argument for this function is intended to be generated with
    the `register_wins` function. The second and third input arguments are
    intended to be passed from the scope of the `timeless` function.
    """

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
        standings['Prize'] = [f'¤{x*entry_fee_unit}' for x in STANDING_CONFIGURATIONS.get(key).get('Points')[index]]

    interface.segment_display_standings(standings, round_)


def timeless(duelists, variant, entry_fee):
    """Run the TIMELESS tournament.

    Parameters
    ----------
    duelists : list of Duelist
        Duelists that are to participate in the tournament, as instances of the
        `Duelist` class. The order of the list technically matters, as the
        course of the tournament depends on it. Practically, however, the order
        of the list does not matter, as the same aspects of the tournament
        which depend on this order also depend on the particular choice of the
        Timeless square, which is generated (randomly) after the `duelists`
        argument is already set.
    variant : {'Basic', 'Extra'}
        Name of the TIMELESS variant.
    entry_fee : int
        The entry fee for this TIMELESS tournament.

    Returns
    -------
    None

    Notes
    -----
    The input arguments for this function are intended to be generated with the
    `enter_tournament_information` function. Said function ensures that the
    arguments are of correct types, and have intended values (such as the entry
    fee being a non-negative multiple of 10). It also randomly shuffles the
    list of duelists.
    """

    interface.segment_starting(variant, entry_fee)
    decks = DECK_SETS.get(variant)
    matchup = random_timeless_square()

    for round_ in ROUNDS:
        pairings = generate_pairings(duelists, decks, matchup, round_)
        winners_and_losers = register_wins(*pairings)
        display_standings(winners_and_losers, round_, entry_fee)

    interface.segment_ending(variant, entry_fee)


def run_yugioh_timeless():
    """Run the TIMELESS tournament in the standard, intended way."""

    interface.segment_initial()
    timeless(**enter_tournament_information())
    interface.segment_final()

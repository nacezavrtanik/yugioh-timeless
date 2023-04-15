"""Module for running the Yugioh Timeless tournament format."""

import numpy as np
from string import capwords
from tabulate import tabulate


def _is_string_of_integer(input_string):
    """Check if a string represents an integer.

    Helper function for `supervised_input`.
    """
    try:
        int(input_string)
    except ValueError:
        return False
    return True


def supervised_input(prompt, conditions, options=None):
    """Require user input to satisfy specified conditions.

    The user is asked to provide an input value. If the provided value violates
    a specified condition, a tip for correcting the input is displayed, then
    the user is once again asked to provide an input value. This process is
    repeated until all specified conditions are satisfied.

    Parameters
    ----------
    prompt : str
        Description of desired input.
    conditions: str, list of str
        Names of conditions. A string can be passed if only one condition is
        specified, otherwise a list of strings.
    options: list of str, optional
        Valid input options if argument `conditions` is set to 'choose_from'.
        If `conditions` does not include 'choose_from', this argument is not
        relevant.

        As user input is passed to the string.capwords function first, option
        strings should ahdere to that format as well.
        (defaults to None)

    Returns
    -------
    str
        User input, satisfying all conditions in `conditions`. Words are
        capitalised, consecutive whitespaces are replaced by a single
        whitespace, and leading and trailing whitespaces are removed.

    Notes
    -----
    User input is immediately passed to the string.capwords function, which
    capitalises words, strips leading and trailing whitespaces, and replaces
    consecutive whitespaces by a single whitespace. There are two reasons for
    this.

    (1) It is more convenient for the user. As all the checks will aplly to
    the modified string, user input will not be sensitive to choice of case
    nor to consecutive whitespaces.
    (2) It looks cleaner.

    Examples
    --------
    >>> supervised_input('Favourite integer: ', 'integer')
    Favourite integer: >? 3.14
    TIP: Enter an integer.
    Favourite integer: >? 3
    '3'

    >>> supervised_input('Your name: ',
    ...                  ['alphabetical', 'less_than_30_characters'])
    Your name: >? Johannes Chrysostomus Wolfgangus Theophilus Mozart 1756
    TIP: Use only letters and whitespaces.
    Your name: >? Johannes Chrysostomus Wolfgangus Theophilus Mozart
    TIP: Use less than 30 characters.
    Your name: >? Amadeus
    'Amadeus'

    >>>supervised_input('Do you like yes or no questions?',
    ...                 'choose_from', options=['Yes', 'No'])
    Do you like yes or no questions?>? I'm not sure
    TIP: Enter one of these: Yes, No.
    Do you like yes or no questions?>? No
    'No'
    """

    condition_checks = {
        'choose_from': lambda input_string: input_string in options,
        'alphabetical': lambda input_string: input_string.replace(' ', '').isalpha(),
        'less_than_30_characters': lambda input_string: len(input_string) < 30,
        'integer': lambda input_string: _is_string_of_integer(input_string),
        'multiple_of_5': lambda input_string: int(input_string) % 5 == 0 and int(input_string) >= 0,
    }

    input_tips = {
        'choose_from': f'''Enter one of these: {options.__str__()[1: -1].replace("'", "")}.''',
        'alphabetical': 'Use only letters and whitespaces.',
        'less_than_30_characters': 'Use less than 30 characters.',
        'integer': 'Enter an integer.',
        'multiple_of_5': 'Pick a non-negative multiple of 5.',
    }

    if isinstance(conditions, str):
        conditions = [conditions]

    while True:

        user_input = capwords(input(prompt))
        check = True

        for condition in conditions:

            condition_satisfied = condition_checks.get(condition)(user_input)
            check = check and condition_satisfied

            if not condition_satisfied:
                print(f'TIP: {input_tips.get(condition)}')
                break

        if check:
            return user_input


def random_timeless_square():
    """Randomly generate a timeless square.

    Keeps randomly generating squares until a Timeless sqaure is generated.

    Returns
    -------
    numpy.ndarray
        Timeless square.

    Notes
    -----
    Timeless squares are 4x4 arrays that are isomorphic to Latin squares.
    They are used to model matchups in the Yugioh Timeless tournament format.

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


class Duelist:
    """Class for tracking duelists and scores in a Yugioh Timeless tournament.

    Attributes
    ----------
    name : str
        Name of the duelist.
    wins : int
        Number of duels won.

    Methods
    -------
    enter_unique_duelists()
        Return list of `Duelist` instances with unique `name` attributes.
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
        Duelist Amadeus, with 1 win(s).
        """
        self.name = capwords(name)
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

    @staticmethod
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
        >>> Duelist.enter_unique_duelists()
        Duelist 1: >? Johann
        Duelist 2: >? Johann
        Duelist 3: >? Amadeus
        Duelist 4: >? Amadeus
        You've entered some duplicate names: Amadeus, Johann.
        Please try again.
        Duelist 1: >? Johann
        Duelist 2: >? Johann C
        Duelist 3: >? Amadeus
        Duelist 4: >? Falco
        [Duelist('Johann', wins=0), Duelist('Johann C', wins=0), Duelist('Amadeus', wins=0), Duelist('Falco', wins=0)]
        """

        while True:

            duelist_candidates = [
                Duelist(supervised_input(f'Duelist {i + 1}: ', ['alphabetical', 'less_than_30_characters']))
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

    format_ = supervised_input('Choose format: ', 'choose_from', options=['Basic', 'Extra']).upper()
    decks = deck_sets.get(format_)

    entry_fee = int(supervised_input('Set entry fee: ', ['integer', 'multiple_of_5', 'less_than_30_characters']))

    duelists = np.random.permutation(Duelist.enter_unique_duelists())

    tournament_information = {'decks': decks, 'entry_fee': entry_fee, 'duelists': duelists}

    return tournament_information


FINAL_ROUND = 3
PAIRING_CONFIGURATIONS = ([0, 1, 2, 3], [1, 3, 0, 2], [3, 0, 1, 2])
STANDING_CONFIGURATIONS = {
    0: {
        'wins': ([1, 1, 0, 0], ),
        'places': ([1, 1, 3, 3], )
    },
    1: {
        'wins': ([2, 2, 0, 0], [2, 1, 1, 0], [1, 1, 1, 1]),
        'places': ([1, 1, 3, 3], [1, 2, 2, 4], [1, 1, 1, 1])
    },
    2: {
        'wins': ([3, 2, 1, 0], [3, 1, 1, 1], [2, 2, 2, 0], [2, 2, 1, 1]),
        'places': ([1, 2, 3, 4], [1, 2, 2, 2], [1, 1, 1, 4], [1, 1, 3, 3])
    },
    3: {
        True: {
            'wins': ([4, 2, 1, 1], [3, 3, 2, 0], [3, 2, 2, 1]),
            'places': ([1, 2, 3, 3], [1, 1, 3, 4], [1, 2, 2, 4]),
            'prizes': ([10, 6, 2, 2], [8, 8, 4, 0], [9, 5, 5, 1])
        },
        False: {
            'wins': ([4, 2, 2, 0], [4, 2, 1, 1], [3, 3, 2, 0], [3, 3, 1, 1], [3, 2, 2, 1]),
            'places': ([1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]),
            'prizes': ([10, 6, 4, 0], [10, 6, 3, 1], [9, 7, 4, 0], [9, 7, 3, 1], [9, 6, 4, 1])
        }
    }
}
TIE_CONFIGURATIONS_AFTER_PRELIMINARIES = ([3, 1, 1, 1], [2, 2, 2, 0])


def check_if_tie_after_preliminaries(duelists):
    duelists_by_wins = sorted(duelists, reverse=True)
    tie = duelists_by_wins in TIE_CONFIGURATIONS_AFTER_PRELIMINARIES
    return tie


def preliminary_round(duelists, decks, matchup, round_):

    # Display pairings
    x, y, z, w = PAIRING_CONFIGURATIONS[round_]
    deck_xy, deck_yx, deck_zw, deck_wz = [decks[matchup[x, y]], decks[matchup[y, x]],
                                          decks[matchup[z, w]], decks[matchup[w, z]]]
    duelist_x, duelist_y, duelist_z, duelist_w = [duelists[i] for i in [x, y, z, w]]
    pairings = [[f'{duelist_x} ({deck_xy})', 'VS', f'{duelist_y} ({deck_yx})'],
                [f'{duelist_z} ({deck_zw})', 'VS', f'{duelist_w} ({deck_wz})']]
    print(f'\nPairings for round {round_ + 1}:\n')
    print(tabulate(pairings, tablefmt='plain'), '\n')

    # Register wins
    winner_xy = supervised_input(f'Who won, {duelist_x} or {duelist_y}?',
                                 'choose_from', options=[duelist_x.name, duelist_y.name])
    winner_zw = supervised_input(f'Who won, {duelist_z} or {duelist_w}?',
                                 'choose_from', options=[duelist_z.name, duelist_w.name])
    for i in [x, y, z, w]:
        if duelists[i] in [winner_xy, winner_zw]:
            duelists[i].wins += 1

    # Display standings
    duelists_by_wins = sorted(duelists, reverse=True)
    config = STANDING_CONFIGURATIONS.get(round_).get('wins').index(duelists_by_wins)
    standings = {
        'Place': STANDING_CONFIGURATIONS.get(round_).get('places')[config],
        'Duelist': duelists_by_wins,
        'Wins': [duelist.wins for duelist in duelists_by_wins]
    }
    print(f'\nStandings after round {round_ + 1}\n')
    print(tabulate(standings, headers='keys', colalign=('center', 'left', 'center')))


def final_round(duelists, decks, matchup, tie_after_preliminaries, entry_fee):

    # Display pairings
    if tie_after_preliminaries:
        x, y, z, w = PAIRING_CONFIGURATIONS[np.random.randint(3)]
    else:
        x, y, z, w = np.flip(np.argsort(duelists))
    deck_x, deck_y, deck_z, deck_w = [decks[matchup[x, x]], decks[matchup[y, y]],
                                      decks[matchup[z, z]], decks[matchup[w, w]]]
    duelist_x, duelist_y, duelist_z, duelist_w = [duelists[i] for i in [x, y, z, w]]
    pairings = [[f'{duelist_x} ({deck_x})', 'VS', f'{duelist_y} ({deck_y})'],
                [f'{duelist_z} ({deck_z})', 'VS', f'{duelist_w} ({deck_w})']]
    print(f'\nPairings for final round:\n')
    print(tabulate(pairings, tablefmt='plain'), '\n')

    # Register wins
    winner_xy = supervised_input(f'Who won, {duelist_x} or {duelist_y}?',
                                 'choose_from', options=[duelist_x.name, duelist_y.name])
    winner_zw = supervised_input(f'Who won, {duelist_z} or {duelist_w}?',
                                 'choose_from', options=[duelist_z.name, duelist_w.name])
    for i in [x, y, z, w]:
        if duelists[i] in [winner_xy, winner_zw]:
            duelists[i].wins += 1

    # Display standings
    if tie_after_preliminaries:
        duelists_by_places = sorted(duelists, reverse=True)
    else:
        duelist_1st = duelist_x if duelist_x == winner_xy else duelist_y
        duelist_2nd = duelist_x if duelist_x != winner_xy else duelist_y
        duelist_3rd = duelist_z if duelist_z == winner_zw else duelist_w
        duelist_4th = duelist_z if duelist_z != winner_zw else duelist_w
        duelists_by_places = [duelist_1st, duelist_2nd, duelist_3rd, duelist_4th]

    config = STANDING_CONFIGURATIONS.get(FINAL_ROUND).get(tie_after_preliminaries).get('wins').index(duelists_by_places)
    standings = {
        'Place': STANDING_CONFIGURATIONS.get(FINAL_ROUND).get(tie_after_preliminaries).get('places')[config],
        'Duelist': duelists_by_places,
        'Wins': [duelist.wins for duelist in duelists_by_places],
        'Prize': STANDING_CONFIGURATIONS.get(FINAL_ROUND).get(tie_after_preliminaries).get('prizes')[config]
        }
    print('\nFINAL STANDINGS\n---------------\n')
    print(tabulate(standings, headers='keys', colalign=('center', 'left', 'center', 'center')))


def timeless(duelists, decks, entry_fee):

    matchup = random_timeless_square()

    preliminary_round(duelists, decks, matchup, 0)
    preliminary_round(duelists, decks, matchup, 1)
    preliminary_round(duelists, decks, matchup, 2)
    tie_after_preliminaries = check_if_tie_after_preliminaries(duelists)
    final_round(duelists, decks, matchup, tie_after_preliminaries, entry_fee)


if __name__ == '__main__':
    timeless(**enter_tournament_information())

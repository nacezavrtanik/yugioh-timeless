"""Module for running the Yugioh Timeless tournament format."""

import numpy as np
from string import capwords


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

    def _is_whole_number(input_string):
        try:
            int(input_string)
        except ValueError:
            return False
        else:
            return True

    condition_checks = {
        'choose_from': lambda input_string: input_string in options,
        'alphabetical': lambda input_string: input_string.replace(' ', '').isalpha(),
        'less_than_30_characters': lambda input_string: len(input_string) < 30,
        'integer': lambda input_string: _is_whole_number(input_string),
        'multiple_of_5': lambda input_string: int(input_string) % 5 == 0 and int(input_string) >= 0
    }

    input_tips = {
        'choose_from': f'''Enter one of these: {options.__str__()[1: -1].replace("'", "")}.''',
        'alphabetical': 'Use only letters and whitespaces.',
        'less_than_30_characters': 'Use less than 30 characters.',
        'integer': 'Enter an integer.',
        'multiple_of_5': 'Pick a non-negative multiple of 5.'
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
        unique_loop = len({random_square[0, 1], random_square[1, 0], random_square[2, 3], random_square[3, 2]}) == 4

        is_timeless = unique_diagonal and unique_antidiagonal and unique_loop

        if is_timeless:
            return random_square


class Duelist:
    """Class for tracking duelists and scores in a Yugioh Timeless tournament.

    Parameters
    ----------
    name : str
        Name of duelist.
    wins : int, optional
        Number of wins.
        (defaults to 0)

    Attributes
    ----------
    wins : int
        Number of duels won.

    Examples
    --------
    >>> duelist = Duelist('Amadeus', wins=3)
    >>> print(duelist)
    Duelist: Amadeus
    Wins: 3
    """

    def __init__(self, name, wins=0):
        self.name = capwords(name)
        self.wins = wins

    def __repr__(self):
        return f'Duelist(\'{self.name}\', wins={self.wins})'

    def __str__(self):
        return f'Duelist: {self.name}\nWins: {self.wins}'

    def increase_win_count(self, n=1):
        """Increase value of `wins` attribute by `n`."""
        self.wins += n

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


class Timeless:

    deck_sets = {'BASIC': ['Beast', 'Chaos', 'Dragon', 'Spellcaster'],
                 'EXTRA': ['Dinosaur', 'Flip', 'Warrior', 'Zombie']}
    pairings = np.array([[0, 1, 2, 3], [1, 3, 0, 2], [3, 0, 1, 2]])

    def __init__(self):
        self.format = supervised_input('Choose format: ', 'choose_from', options=['Basic', 'Extra']).upper()
        self.decks = Timeless.deck_sets.get(self.format)
        self.entry_fee = supervised_input('Set entry fee: ', ['integer', 'multiple_of_5', 'less_than_30_characters'])
        self.duelists = np.random.permutation(Duelist.enter_unique_duelists())
        self.matchup = random_timeless_square()
        self.round = 0

    def __repr__(self):
        return 'Timeless()'

    def __str__(self):
        description = f'Timeless {self.format}, round {self.round + 1}\n'
        description += f'Entry fee: {self.entry_fee}\n'
        description += '\nWINS PER PLAYER\n---------------\n'
        for i in range(4):
            description += f'{self.duelists[i].name}: {self.duelists[i].wins}\n'
        return description


if __name__ == '__main__':

    timeless = Timeless()

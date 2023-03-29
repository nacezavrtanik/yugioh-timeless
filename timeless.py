
from string import capwords


def supervised_input(prompt, conditions):
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

    Returns
    -------
    str
        User input, satisfying all conditions in `conditions`.

    Examples
    --------

    Ask the user to provide their name. Insist for the name to contain only
    letters and whitespaces, and be shorter than 30 characters.

    >>> supervised_input('Your name: ',
    ...                  ['alphabetical', 'less_than_30_characters'])
    Your name: >? Johannes Chrysostomus Wolfgangus Theophilus Mozart 1756
    TIP: A name should only contain letters and whitespaces.
    Your name: >? Johannes Chrysostomus Wolfgangus Theophilus Mozart
    TIP: A name should contain less than 30 characters.
    Your name: >? Amadeus
    'Amadeus'
    """

    condition_checks = {
        '1_or_2': lambda input_string: input_string in ['1', '2'],
        '1_2_or_3': lambda input_string: input_string in ['1', '2', '3'],
        'alphabetical': lambda input_string: input_string.replace(' ', '').isalpha(),
        'less_than_30_characters': lambda input_string: len(capwords(input_string)) < 30
    }

    input_tips = {
        '1_or_2': 'Enter either 1 or 2.',
        '1_2_or_3': 'Enter either 1, 2, or 3.',
        'alphabetical': 'A name should only contain letters and whitespaces.',
        'less_than_30_characters': 'A name should contain less than 30 characters.'
    }

    if isinstance(conditions, str):
        conditions = [conditions]

    while True:

        user_input = input(prompt)
        check = True

        for condition in conditions:

            condition_satisfied = condition_checks.get(condition)(user_input)
            check = check and condition_satisfied

            if not condition_satisfied:
                print(f'TIP: {input_tips.get(condition)}')
                break

        if check:
            return user_input


class Duelist:

    wins = 0

    def __init__(self):
        self.name = capwords(supervised_input('Name of duelist: ', ['alphabetical', 'less_than_30_characters']))

    def increase_win_count(self):
        self.wins += 1

"""  """

import time
from string import capwords

from tabulate import tabulate


def is_string_of_integer(input_string):
    """Check if a string represents an integer."""
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

        As user input first is passed to the `string.capwords` function,
        strings in `options` should adhere to that same format as well.
        (defaults to None)

    Returns
    -------
    str
        User input, satisfying all conditions in `conditions`. Words are
        capitalised, consecutive whitespaces are replaced by a single
        whitespace, and leading and trailing whitespaces are removed.

    Notes
    -----
    User input is immediately passed to the `string.capwords` function, which
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

    >>> supervised_input('Do you like yes or no questions?',
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
        'integer': lambda input_string: is_string_of_integer(input_string),
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


def _typewriter(text, seconds_per_character=0.05, final_nap=0.0):
    """Print text character by character."""
    for character in text:
        print(character, sep='', end='')
        time.sleep(seconds_per_character)
    time.sleep(final_nap)


LINE_WIDTH = 80
title_ = 'T I M E L E S S'.center(LINE_WIDTH)
git = 'git : link'.center(LINE_WIDTH)
yt = 'youtube : link'.center(LINE_WIDTH)
test = '''test string snfsdf
omf3m # 4rm2dlm2f_
mf4 2232345 efe ?('''
title_2 = f'\n\n\n{title_}\n'

t = tabulate([[1, 2, 3], [4, 5, 6]])

# print('\n\n', 31 * ' ', end='')
# typewriter('T I M E', seconds_per_character=0.5, final_nap=1)
# typewriter(' L E S S\n\n', seconds_per_character=0, final_nap=1)
# print(git)
# time.sleep(1)
# print(yt, end='\n\n')
# time.sleep(1)
# print(f"{'':-^80}", end='\n\n')
#
# segments = {'title': ''}
#
#
# def interface_title(title, secs=0.5, nap=0.0):
#     title_string = f'{title:^80}'
#     typewriter(title_string, seconds_per_character=secs, final_nap=nap)


def typewriter(text, pause=0.5, pause_after=None, end_pause=None, end='\n'):

    # TODO ignore_whitespaces=True
    # TODO pause_index

    if not pause or pause == 0:
        print(text, sep='', end=end)

    if pause_after is None:
        for character in text:
            print(character, sep='', end='')
            time.sleep(pause)

    if isinstance(pause_after, str) or isinstance(pause_after, list):
        pause_after = set(pause_after)

    if isinstance(pause_after, set):
        for character in text:
            print(character, sep='', end='')
            if character in pause_after:
                time.sleep(pause)

    if isinstance(pause_after, dict):
        for character in text:
            print(character, sep='', end='')
            if character in pause_after:
                time.sleep(pause_after.get(character))

    if end:
        print(end=end)

    if end_pause:
        time.sleep(end_pause)


def print_centered_table(table):
    rows = table.split('\n')
    for row in rows:
        typewriter(row.center(80), pause=False, end_pause=1)


if __name__ == '__main__':

    typewriter(title_2, pause_after='TIME', pause=1)
    typewriter(git, pause=False, end_pause=1)
    typewriter(yt, pause=False, end_pause=1)
    print(f"\n{'':-^80}\n")
    print_centered_table(t)

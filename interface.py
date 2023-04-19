"""Module for creating a user interface for the TIMELESS tournament format."""

import string
import textwrap
import time

from tabulate import tabulate


LINE_WIDTH = 80
LEFT_MARGIN = 5
RIGHT_MARGIN = LINE_WIDTH - LEFT_MARGIN
INDENT = LEFT_MARGIN * ' '

text_wrapper = textwrap.TextWrapper(width=RIGHT_MARGIN, initial_indent=INDENT, subsequent_indent=INDENT)

TIMELESS = 'T I M E L E S S'.center(LINE_WIDTH)
GIT = 'git: link'.center(LINE_WIDTH)
YOUTUBE = 'youtube: link'.center(LINE_WIDTH)
LINE = LINE_WIDTH * '-'

test = '''test string snfsdf
omf3m # 4rm2dlm2f_
mf4 2232345 efe ?('''
title_2 = f'\n\n\n{TIMELESS}\n'

t = [[1, 2, 3], [4, 5, 6]]

LOREM = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et
dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""


def typewriter(text, pause=0.5, custom=None):

    if custom:
        for i, character in enumerate(text):
            print(character, sep='', end='')
            if i in custom:
                time.sleep(custom.get(i))

    else:
        for character in text:
            print(character, sep='', end='')
            time.sleep(pause)


def print_centered_table(table, **kwargs):
    table = tabulate(table, **kwargs)
    rows = table.split('\n')
    for row in rows:
        print(row.center(80))
        time.sleep(.5)
    print()


def segment_title():

    indices = [title_2.index(character) for character in 'TIME']
    pauses = dict(zip(indices, [.25, .25, .25, 1.5]))

    time.sleep(1)
    typewriter(title_2, custom=pauses)
    time.sleep(1)
    print(f'\n{GIT}')
    time.sleep(0.5)
    print(f'{YOUTUBE}\n')
    time.sleep(0.5)
    print(LINE)


def segment_format():
    description = '''Timeless je poseben turnirski format za štiri igralce.
Ti se pomerijo v treh predrundah (vsak z vsakim), nato
pa sledi še finalna runda. Nobena izmed teh ni časovno
omejena. Igra se z naborom štirih deckov, ki so med
igralce razdeljeni naključno. Po vsaki rundi se decki
ponovno naključno razdelijo med igralce, in sicer tako,
da v štirih rundah vsak igralec igra z vsakim izmed
štirih deckov natanko enkrat. Na voljo sta dva nabora
deckov:

 1) BASIC
 2) EXTRA'''.center(LINE_WIDTH)
    output = text_wrapper.fill(description)

    print(output)


def segment_entry_fee():
    entry_fee = """Kaj pa prijavnina?
Ta gre v celoti v nagradni sklad in se na koncu glede
na dosežke razdeli nazaj med igralce.

 1) 5 €
 2) 10 €
 3) brez"""
    output = text_wrapper.fill(entry_fee)
    print(output)


def segment_duelists():
    print(text_wrapper.fill('Now enter duelist names.'))


def segment_pairings(pairings, round_):
    print(f'\nPairings for round {round_ + 1}:\n')
    print_centered_table(pairings, tablefmt='plain')


def segment_standings(standings, round_):

    if round_ in (0, 1, 2):
        print(f'Standings after round {round_ + 1}:\n')
        del standings['Points']
        print_centered_table(standings, headers='keys', colalign=('center', 'left', 'center'))

    else:
        print('Final standings:\n')
        print_centered_table(standings, headers='keys', colalign=('center', 'left', 'center', 'center'))


SEGMENTS = {
    'pairings': segment_pairings,
    'standings': segment_standings
}


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

        user_input = string.capwords(input(prompt))
        check = True

        for condition in conditions:

            condition_satisfied = condition_checks.get(condition)(user_input)
            check = check and condition_satisfied

            if not condition_satisfied:
                print(f'TIP: {input_tips.get(condition)}')
                break

        if check:
            return user_input


if __name__ == '__main__':

    segment_title()
    print()
    time.sleep(1)
    segment_format()
    input()
    segment_entry_fee()
    input()
    segment_duelists()
    print()
    print(LINE)
    print()
    time.sleep(1)
    print_centered_table(t)

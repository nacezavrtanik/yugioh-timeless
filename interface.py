"""Module for creating a user interface for the TIMELESS tournament format.

This module contains functions pertaining to user interaction during the
TIMELESS tournament format. Its purpose is to separate this part of the code
from the `timeless` module, which implements the actual core structure of the
TIMELESS format, increasing the readability of the `timeless` module in the
process.

Beside other functions, this module contains so-called segment functions,
which are mostly used to print chunks (segments) of text to give the
terminal interface its intended look and feel.

Variables
---------
`TODAY`
    Constant containding today's date as a `datetime.date` instance.
`tournament_report`
    Instance of `io.StringIO` for documentting the course of the tournament.

Functions
---------
`wrap`
    Wrap text to fit inside margins, with empty lines before and after.
`typewriter`
    Print text character by character for typewriter effect.
`supervised_input`
    Require user input to satisfy specified conditions.
`generate_centered_table`
    Generate table with `tabulate.tabulate`, and center it.
`save_tournament_report`
    Save contents of the global variable `tournament_report` to a file.
`segment_initial`
    Print general information on the TIMELESS format.
`segment_enter_variant`
    Print deck choice description.
`segment_enter_entry_fee`
    Print entry fee description.
`segment_enter_duelists`
    Print duelist sign-up prompt.
`segment_enter_tournament_information_end`
    Print bold line.
`segment_starting`
    Print information on the TIMELESS tournament about to start.
`segment_generate_pairings`
    Print pairings.
`segment_register_wins`
    Print empty line.
`segment_display_standings`
    Print standings.
`segment_ending`
    Ask user if a tournament report should be saved and do it (or not).
`segment_final`
    Print exit instructions.

"""

import io
import itertools
import os
import random
import shutil
import string
import textwrap
import time
import datetime

from colorama import Cursor, Fore, Style, just_fix_windows_console
from colorama.ansi import clear_line
from tabulate import tabulate

from config import RIGHT_MARGIN, INDENT, LARGE_INDENT, LINE_WIDTH, GIT, YOUTUBE, LINE, BOLDLINE, NEWLINE, TIMELESS
from config import PRELIMINARY_ROUNDS


LOREM = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Mauris cursus mattis molestie a iaculis. Habitant morbi tristique senectus et. Sit amet luctus venenatis lectus magna fringilla urna.'

just_fix_windows_console()  # enable ANSI escape characters on Windows

TITLE = Fore.CYAN + Style.BRIGHT
SUBTITLE = Fore.CYAN
TODAY = datetime.datetime.today().date()

tournament_report = io.StringIO()


def wrap(text):
    """Wrap text to fit inside margins, with empty lines before and after."""
    text_wrapper = textwrap.TextWrapper(width=RIGHT_MARGIN, initial_indent=INDENT, subsequent_indent=INDENT)
    return NEWLINE + text_wrapper.fill(text) + NEWLINE


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
        Valid strings: 'choose_from', 'alphabetical', 'less_than_25_characters',
        'integer', 'multiple_of_10'.
    options: list of str, optional
        Valid input options if argument `conditions` is set to 'choose_from'.
        If `conditions` does not include 'choose_from', this argument is not
        relevant.

        As user input is first passed to the `string.capwords` function,
        strings in `options` should adhere to that same format as well.
        (defaults to None)

    Returns
    -------
    str
        User input, satisfying all conditions in `conditions`. Words are
        capitalised, consecutive whitespaces are replaced by a single space,
        and leading and trailing whitespaces are removed.

    Notes
    -----
    User input is immediately passed to the `string.capwords` function, which
    capitalises words, strips leading and trailing whitespaces, and replaces
    consecutive whitespaces by a single space. There are two reasons for this.

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
    ...                  ['alphabetical', 'less_than_25_characters'])
            Your name: >? Johannes Chrysostomus Wolfgangus Theophilus Mozart 1756
            TIP: Use only letters and whitespaces.
            Your name: >? Johannes Chrysostomus Wolfgangus Theophilus Mozart
            TIP: Use less than 25 characters.
            Your name: >? Amadeus
    'Amadeus'

    >>> supervised_input('Do you like yes or no questions?',
    ...                 'choose_from', options=['Yes', 'No'])
            Do you like yes or no questions?>? I'm not sure
            TIP: Enter one of these: Yes, No.
            Do you like yes or no questions?>? No
    'No'
    """

    def is_string_of_integer(input_string):
        """Check if a string represents an integer."""
        try:
            int(input_string)
        except ValueError:
            return False
        return True

    condition_checks = {
        'choose_from': lambda input_string: input_string in options,
        'alphabetical': lambda input_string: input_string.replace(' ', '').isalpha(),
        'less_than_25_characters': lambda input_string: len(input_string) < 25,
        'integer': lambda input_string: is_string_of_integer(input_string),
        'multiple_of_10': lambda input_string: int(input_string) % 10 == 0 and int(input_string) >= 0,
        'max_1000': lambda input_string: int(input_string) <= 1000,
    }

    input_tips = {
        'choose_from': f'''Enter one of these: {options.__str__()[1: -1].replace("'", "")}.''',
        'alphabetical': 'Use only letters and whitespaces.',
        'less_than_25_characters': 'Use less than 25 characters.',
        'integer': 'Enter an integer.',
        'multiple_of_10': 'Pick a non-negative multiple of 10.',
        'max_1000': 'Enter a maximum of 1000.',
    }

    if isinstance(conditions, str):
        conditions = [conditions]

    tip_is_displayed = False

    while True:

        user_input = string.capwords(input(colorise(Style.BRIGHT, clear_line() + LARGE_INDENT + prompt)))
        check = True

        for condition in conditions:

            condition_satisfied = condition_checks.get(condition)(user_input)
            check = check and condition_satisfied

            if not condition_satisfied:
                # Insert tip above prompt, replace previous tip if any
                upstep = Cursor.UP() * (1 + tip_is_displayed)
                print(upstep + clear_line() + LARGE_INDENT + f'TIP: {input_tips.get(condition)}', flush=True)
                tip_is_displayed = True
                break

        if check:
            return user_input


def colorise(color, text):
    """TODO"""
    return color + text + Style.RESET_ALL


def simulate_loading(label):
    """TODO"""

    label = label.strip()
    leading_spaces = label.center(LINE_WIDTH).index(label[0])

    print()

    for progress in range(LINE_WIDTH):

        if progress < leading_spaces:
            bar = f'{progress * "-"}{" " * (leading_spaces - progress)}{label}'
        else:
            bar = f'{"-" * (leading_spaces - 1)} {label} {"-" * (progress - leading_spaces - len(label))}'

        print(colorise(SUBTITLE, bar), end='\r', flush=True)
        time.sleep(random.uniform(0, 0.1))

    print()


def center_multiline_string(multiline_string):
    """TODO"""

    lines = multiline_string.split(NEWLINE)
    max_line_length = max(map(len, lines))
    centered_lines = [f'{row:<{max_line_length}}'.center(LINE_WIDTH) for row in lines]  # padded for proper alignment
    centered_multiline_string = NEWLINE.join(centered_lines)

    return centered_multiline_string


def save_tournament_report(variant, entry_fee):
    """Save contents of the global variable `tournament_report` to a file.

    Parameters
    ----------
    variant : {'Basic', 'Extra'}
        Name of the TIMELESS variant.
    entry_fee : int
        Entry fee for the TIMELESS tournament.

    Returns
    -------
    None

    Notes
    -----
    A filename is generated automatically. If a file with that name already
    exists, a number is appended.
    """

    filename = f'{TODAY} TIMELESS-{variant}-{entry_fee} Report.txt'
    counter = itertools.count(2)
    while filename in os.listdir():
        filename = f'{TODAY} TIMELESS-{variant}-{entry_fee} Report {next(counter)}.txt'

    try:
        with open(filename, 'w', encoding='utf-8') as report_file:
            tournament_report.seek(0)
            shutil.copyfileobj(tournament_report, report_file)

    except OSError:
        print(wrap('Sorry, a system-related error occured. Unable to save report.'))

    except Exception:
        print(wrap('Sorry, an unexpected error occured. Unable to save report.'))

    else:
        print(wrap(f'Report saved to {filename}!'))


def segment_initial():
    """Print general information on the TIMELESS format."""

    text = LOREM

    component_1 = colorise(TITLE, 2 * NEWLINE + center_multiline_string(TIMELESS) + NEWLINE)
    component_2 = colorise(SUBTITLE, f'git: {GIT}'.center(LINE_WIDTH))
    component_3 = colorise(SUBTITLE, f'youtube: {YOUTUBE}'.center(LINE_WIDTH))
    component_4 = wrap(text) + NEWLINE

    print(component_1, component_2, component_3, component_4, sep=NEWLINE)


def segment_enter_variant():
    """Print deck choice description."""
    text = LOREM
    simulate_loading('SIGN-UP')
    print(wrap(text))


def segment_enter_entry_fee():
    """Print entry fee description."""
    text = LOREM
    print(wrap(text))


def segment_enter_duelists():
    """Print duelist sign-up prompt."""
    print(wrap(LOREM))


def segment_enter_tournament_information_end():
    """Print bold line."""
    print(colorise(SUBTITLE, 2 * NEWLINE + LINE))


def segment_starting(variant, entry_fee):
    """Print information on the TIMELESS tournament about to start."""

    component_1 = colorise(TITLE, 2 * NEWLINE + ' '.join('TIMELESS').center(LINE_WIDTH))
    component_2 = colorise(TITLE, f'{variant}, ¤{entry_fee}'.center(LINE_WIDTH))
    component_3 = colorise(TITLE, str(TODAY).center(LINE_WIDTH))
    component_4 = colorise(TITLE, 2 * NEWLINE + BOLDLINE)

    print(component_1, component_2, component_3, component_4, sep=NEWLINE)
    print(component_1, component_2, component_3, component_4, sep=NEWLINE, file=tournament_report)


def segment_generate_pairings(pairings, round_):
    """Print pairings."""
    round_label = f' ROUND {round_ + 1} ' if round_ in PRELIMINARY_ROUNDS else ' FINAL ROUND '
    simulate_loading(round_label)
    print(2 * NEWLINE + center_multiline_string(tabulate(pairings, tablefmt='plain')) + NEWLINE)


def segment_register_wins():
    """Print empty line."""
    print(NEWLINE)


def segment_display_standings(standings, round_):
    """Print standings."""

    colalign = ('center', 'left', 'center') if round_ in PRELIMINARY_ROUNDS else ('center', 'left', 'center', 'center')

    component_1 = center_multiline_string(
        tabulate(standings, headers='keys', tablefmt='double_outline', colalign=colalign))
    component_2 = '' if round_ in PRELIMINARY_ROUNDS else colorise(TITLE, 2 * NEWLINE + BOLDLINE + NEWLINE)

    print(component_1, component_2, sep=NEWLINE)
    print(component_1, component_2, sep=NEWLINE, file=tournament_report)


def segment_ending(variant, entry_fee):
    """Ask user if a tournament report should be saved and do it (or not)."""

    simulate_loading('COVERAGE')
    print(wrap(LOREM))

    save_report = supervised_input('Would you like to save a tournament report, yes or no? ',
                                   'choose_from', options=['Yes', 'No'])
    if save_report == 'Yes':
        save_tournament_report(variant, entry_fee)
    else:
        print(wrap('Report not saved.'))

    print(colorise(SUBTITLE, NEWLINE + LINE))


def segment_final():
    """Print exit instructions."""
    input(colorise(SUBTITLE, '(Press ENTER to exit.)'))

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
    Constant containing today's date as a `datetime.date` instance.
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
import string
import textwrap
import time
import datetime

from colorama import just_fix_windows_console
from colorama.ansi import Fore, Style, Cursor, clear_line
from tabulate import tabulate

from config import TERMINAL_WIDTH, TERMINAL_WIDTH_DEFAULT , LINE_WIDTH, LINE_WIDTH_DEFAULT
from config import RIGHT_MARGIN, INDENT, SMALL_INDENT, LARGE_INDENT
from config import LINE, LINE_DEFAULT, BOLDLINE, BOLDLINE_DEFAULT, NEWLINE, TIMELESS, GIT, YOUTUBE
from config import PRELIMINARY_ROUNDS
from config import LOREM


just_fix_windows_console()  # enable ANSI escape sequences on Windows

PRIMARY = Fore.CYAN + Style.BRIGHT
SECONDARY = Fore.CYAN
CLEAR = Style.RESET_ALL
TODAY = datetime.datetime.today().date()

tournament_report = io.StringIO()


def wrap(text):
    """Wrap text to fit inside margins, with empty lines before and after."""
    text_wrapper = textwrap.TextWrapper(width=RIGHT_MARGIN, initial_indent=INDENT, subsequent_indent=INDENT)
    return NEWLINE + text_wrapper.fill(text) + NEWLINE


def colorise(color, text):
    return color + text + CLEAR


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
    ...                  'choose_from', options=['Yes', 'No'])
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
        'choose_from': f'''Enter one of these: {str(options).replace("'", "").replace("[", "").replace("]", "")}.''',
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
                print(colorise(Fore.BLACK + Style.BRIGHT,
                               clear_line() + LARGE_INDENT + f'TIP: {input_tips.get(condition)}'),
                      end='\r' + Cursor.UP())
                tip_is_displayed = True
                break

        if check:
            print(clear_line(), end='') if tip_is_displayed else None
            return user_input


def simulate_loading(label, report=False):

    print()

    label = f' {label.strip()} '
    label_index = label.center(TERMINAL_WIDTH).index(label)

    lag_base = TERMINAL_WIDTH_DEFAULT / (10*TERMINAL_WIDTH)

    for progress in range(1, LINE_WIDTH + 1 - len(label)):

        bar = (SMALL_INDENT + '-'*progress).ljust(label_index)
        labeled_bar = bar[:label_index] + label + bar[label_index:]

        lag_is_long = random.choices([True, False], weights=[2, LINE_WIDTH])[0]
        lag_range = (lag_base, 4*lag_base) if lag_is_long else (0, lag_base)

        print(colorise(SECONDARY, labeled_bar), end='\r', flush=True)
        time.sleep(random.uniform(*lag_range))

    print()

    if report:
        print(NEWLINE + labeled_bar, file=tournament_report)


def center_multiline_string(multiline_string, width=TERMINAL_WIDTH, leftstrip=False):

    lines = [line.lstrip() if leftstrip else line for line in multiline_string.split(NEWLINE)]
    max_length = max(map(len, lines))
    centered_lines = [line.ljust(max_length).center(width).rstrip() for line in lines]
    centered_multiline_string = NEWLINE.join(centered_lines)

    return centered_multiline_string


def convert_to_default_width(chunk):

    if chunk.lstrip().startswith('T I M E L E S S' + NEWLINE):
        return NEWLINE.join([line.strip().center(TERMINAL_WIDTH_DEFAULT).rstrip() for line in chunk.split(NEWLINE)])

    elif chunk == LINE:
        return LINE_DEFAULT

    elif chunk == BOLDLINE:
        return BOLDLINE_DEFAULT

    elif chunk.startswith(SMALL_INDENT + '-'):
        return SMALL_INDENT + f' {chunk.strip(" -")} '.center(LINE_WIDTH_DEFAULT, '-')

    else:
        return center_multiline_string(chunk, width=TERMINAL_WIDTH_DEFAULT, leftstrip=True)


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

    report_text = tournament_report.getvalue() \
        .replace(PRIMARY, '').replace(SECONDARY, '').replace(CLEAR, '') \
        .replace(3*NEWLINE, 2*NEWLINE).strip(NEWLINE)
    report_text = (2*NEWLINE).join([convert_to_default_width(chunk) for chunk in report_text.split(2*NEWLINE)])
    report_text = NEWLINE + report_text

    try:
        with open(filename, 'w', encoding='utf-8') as report_file:
            print(report_text, file=report_file)

    except OSError:
        print(wrap('Sorry, a system-related error occured. Unable to save report.'))

    except Exception:
        print(wrap('Sorry, an unexpected error occured. Unable to save report.'))

    else:
        print(wrap(f'Report saved to {filename}!'))


def segment_initial():
    """Print general information on the TIMELESS format."""

    text = LOREM

    component_1 = colorise(PRIMARY, 3*NEWLINE + center_multiline_string(TIMELESS) + 2*NEWLINE)
    component_2 = colorise(SECONDARY, f'git: {GIT}'.center(TERMINAL_WIDTH).rstrip())
    component_3 = colorise(SECONDARY, f'youtube: {YOUTUBE}'.center(TERMINAL_WIDTH).rstrip())
    component_4 = NEWLINE + wrap(text)

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
    text = LOREM
    print(wrap(text))


def segment_enter_unique_duelists(duplicate_names_string):
    print(f'You\'ve entered some duplicate names: {duplicate_names_string}.{NEWLINE}Please try again.')


def segment_enter_tournament_information_end():
    """Print bold line."""
    print(colorise(SECONDARY, NEWLINE + LINE))


def segment_starting(variant, entry_fee):
    """Print information on the TIMELESS tournament about to start."""

    component_1 = colorise(PRIMARY, 2*NEWLINE + 'T I M E L E S S'.center(TERMINAL_WIDTH).rstrip())
    component_2 = colorise(PRIMARY, f'{variant}, ¤{entry_fee}'.center(TERMINAL_WIDTH).rstrip())
    component_3 = colorise(PRIMARY, str(TODAY).center(TERMINAL_WIDTH).rstrip())
    component_4 = colorise(PRIMARY, NEWLINE + BOLDLINE + NEWLINE)

    print(component_1, component_2, component_3, component_4, sep=2*NEWLINE)
    print(component_1, component_2, component_3, component_4, sep=NEWLINE, file=tournament_report)


def segment_generate_pairings(pairings, round_):
    """Print pairings."""
    round_label = f' ROUND {round_+1} ' if round_ in PRELIMINARY_ROUNDS else ' FINAL ROUND '
    simulate_loading(round_label, report=True)
    print(2*NEWLINE + center_multiline_string(tabulate(pairings, tablefmt='plain')) + NEWLINE)
    print(2*NEWLINE + center_multiline_string(tabulate(pairings, tablefmt='plain')) + NEWLINE, file=tournament_report)


def segment_register_wins():
    """Print empty line."""
    print()


def segment_display_standings(standings, round_):
    """Print standings."""

    colalign = ('center', 'left', 'center') if round_ in PRELIMINARY_ROUNDS else ('center', 'left', 'center', 'center')

    component_1 = center_multiline_string(
        tabulate(standings, headers='keys', tablefmt='double_outline', colalign=colalign))
    if round_ in PRELIMINARY_ROUNDS:
        component_2 = ''
    else:
        component_2 =  colorise(SECONDARY, 2*NEWLINE + LINE + 2*NEWLINE) + \
                       colorise(PRIMARY, NEWLINE + BOLDLINE + NEWLINE)

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

    print(colorise(SECONDARY, LINE))


def segment_final():
    """Print exit instructions."""
    input(colorise(SECONDARY, SMALL_INDENT + '(Press ENTER to exit.)'))

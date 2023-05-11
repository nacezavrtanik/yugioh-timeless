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
`segments`
    Dictionary containing all segment functions.

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
`segment_enter_format`
    Print deck choice description.
`segment_enter_entry_fee`
    Print entry fee description.
`segment_enter_duelists`
    Print duelist sign-up prompt.
`segment_enter_tournament_information_end`
    Print bold line.
`segment_start`
    Print information on the TIMELESS tournament about to start.
`segment_generate_pairings`
    Print pairings.
`segment_register_wins`
    Print empty line.
`segment_display_standings`
    Print standings.
`segment_end`
    Ask user if a tournament report should be saved and do it (or not).
`segment_final`
    Print exit instructions.

"""

import io
import itertools
import os
import shutil
import string
import textwrap
import time
import datetime

from tabulate import tabulate

from config import RIGHT_MARGIN, INDENT, LARGE_INDENT, LINE_WIDTH, GIT, YOUTUBE, BOLDLINE, NEWLINE, TIMELESS
from config import PRELIMINARY_ROUNDS


TODAY = datetime.datetime.today().date()


tournament_report = io.StringIO()


def wrap(text):
    """Wrap text to fit inside margins, with empty lines before and after."""
    text_wrapper = textwrap.TextWrapper(width=RIGHT_MARGIN, initial_indent=INDENT, subsequent_indent=INDENT)
    return NEWLINE + text_wrapper.fill(text) + NEWLINE


def typewriter(text, delay=0.05, ignore_whitespaces=False):
    """Print text character by character for typewriter effect.

    Parameters
    ----------
    text : str
        Text to be printed.
    delay : float or int
        Delay after printing each character, in seconds.
    ignore_whitespaces : bool, optional
        If True, no delay after characters ' ' and '\n'.
        (defaults to False)

    Returns
    -------
    None
    """

    for character in text:
        print(character, sep='', end='', flush=True)
        if ignore_whitespaces and character in [' ', NEWLINE]:
            continue
        time.sleep(delay)


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
    }

    input_tips = {
        'choose_from': f'''Enter one of these: {options.__str__()[1: -1].replace("'", "")}.''',
        'alphabetical': 'Use only letters and whitespaces.',
        'less_than_25_characters': 'Use less than 25 characters.',
        'integer': 'Enter an integer.',
        'multiple_of_10': 'Pick a non-negative multiple of 10.',
    }

    if isinstance(conditions, str):
        conditions = [conditions]

    while True:

        typewriter(LARGE_INDENT + prompt)
        user_input = string.capwords(input())
        check = True

        for condition in conditions:

            condition_satisfied = condition_checks.get(condition)(user_input)
            check = check and condition_satisfied

            if not condition_satisfied:
                print(LARGE_INDENT + f'TIP: {input_tips.get(condition)}', flush=True)
                break

        if check:
            return user_input


def center_multiline_string(multiline_string):
    """TODO"""

    lines = multiline_string.split(NEWLINE)
    max_line_length = max(map(len, lines))
    centered_lines = [f'{row:<{max_line_length}}'.center(LINE_WIDTH) for row in lines]  # padded for proper alignment
    centered_multiline_string = NEWLINE.join(centered_lines)

    return centered_multiline_string


def save_tournament_report(format_):
    """Save contents of the global variable `tournament_report` to a file.

    Parameters
    ----------
    format_ : {'Basic', 'Extra'}
        Name of the TIMELESS format.

    Returns
    -------
    None

    Notes
    -----
    A filename is generated automatically. If a file with that name already
    exists, a number is appended.
    """

    filename = f'{TODAY} TIMELESS {format_} Report.txt'
    counter = itertools.count(2)
    while filename in os.listdir():
        filename = f'{TODAY} TIMELESS {format_} Report {next(counter)}.txt'

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

    text = '''Timeless je poseben turnirski format za štiri igralce.
Ti se pomerijo v treh predrundah (vsak z vsakim), nato
pa sledi še finalna runda. Nobena izmed teh ni časovno
omejena. Igra se z naborom štirih deckov, ki so med
igralce razdeljeni naključno. Po vsaki rundi se decki
ponovno naključno razdelijo med igralce, in sicer tako,
da v štirih rundah vsak igralec igra z vsakim izmed
štirih deckov natanko enkrat.'''

    component_1 = 3 * NEWLINE + center_multiline_string(TIMELESS) + NEWLINE
    component_2 = f'git: {GIT}'.center(LINE_WIDTH)
    component_3 = f'youtube: {YOUTUBE}'.center(LINE_WIDTH)
    component_4 = wrap(text) + NEWLINE
    component_5 = BOLDLINE

    print(component_1, component_2, component_3, component_4, component_5, sep=NEWLINE)
    time.sleep(2)


def segment_enter_format():
    """Print deck choice description."""
    text = '''Na voljo sta dva nabora
deckov:

 1) BASIC
 2) EXTRA'''
    print(wrap(text))


def segment_enter_entry_fee():
    """Print entry fee description."""
    text = """Kaj pa prijavnina?
Ta gre v celoti v nagradni sklad in se na koncu glede
na dosežke razdeli nazaj med igralce.

 1) 5 €
 2) 10 €
 3) brez"""
    print(wrap(text))


def segment_enter_duelists():
    """Print duelist sign-up prompt."""
    print(wrap('Enter duelist names.'))


def segment_enter_tournament_information_end():
    """Print bold line."""
    print(2 * NEWLINE + BOLDLINE)


def segment_start(format_):
    """Print information on the TIMELESS tournament about to start."""

    component_1 = 2 * NEWLINE + ' '.join('TIMELESS').center(LINE_WIDTH)
    component_2 = format_.center(LINE_WIDTH)
    component_3 = str(TODAY).center(LINE_WIDTH)
    component_4 = 2 * NEWLINE + BOLDLINE

    print(component_1, component_2, component_3, component_4, sep=NEWLINE)
    print(component_1, component_2, component_3, component_4, sep=NEWLINE, file=tournament_report)


def segment_generate_pairings(pairings, round_):
    """Print pairings."""

    round_label = f' ROUND {round_ + 1} ' if round_ in PRELIMINARY_ROUNDS else ' FINAL ROUND '

    component_1 = NEWLINE + f'{round_label:-^{LINE_WIDTH}}' + NEWLINE
    component_2 = NEWLINE + center_multiline_string(tabulate(pairings, tablefmt='plain')) + NEWLINE

    print(component_1, component_2, sep=NEWLINE)
    print(component_1, component_2, sep=NEWLINE, file=tournament_report)


def segment_register_wins():
    """Print empty line."""
    print(NEWLINE)


def segment_display_standings(standings, round_):
    """Print standings."""

    colalign = ('center', 'left', 'center') if round_ in PRELIMINARY_ROUNDS else ('center', 'left', 'center', 'center')

    component_1 = center_multiline_string(
        tabulate(standings, headers='keys', tablefmt='double_outline', colalign=colalign))
    component_2 = '' if round_ in PRELIMINARY_ROUNDS else 2 * NEWLINE + BOLDLINE

    print(component_1, component_2, sep=NEWLINE)
    print(component_1, component_2, sep=NEWLINE, file=tournament_report)


def segment_end(format_):
    """Ask user if a tournament report should be saved and do it (or not)."""

    print(wrap('The tournament has concluded. Congratulations to all duelists!'))
    save_report = supervised_input('Would you like to save a tournament report, yes or no? ',
                                   'choose_from', options=['Yes', 'No'])
    if save_report == 'Yes':
        save_tournament_report(format_)
    else:
        print(wrap('Report not saved.'))


def segment_final():
    """Print exit instructions."""
    input(NEWLINE + BOLDLINE + NEWLINE + '(Press ENTER to exit.)')


segments = {
    'initial': segment_initial,
    'enter_format': segment_enter_format,
    'enter_entry_fee': segment_enter_entry_fee,
    'enter_duelists': segment_enter_duelists,
    'enter_tournament_information_end': segment_enter_tournament_information_end,
    'start': segment_start,
    'generate_pairings': segment_generate_pairings,
    'register_wins': segment_register_wins,
    'display_standings': segment_display_standings,
    'end': segment_end,
    'final': segment_final,
}

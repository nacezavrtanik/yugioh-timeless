"""Module for creating a user interface for the `yugioh-timeless` package.

The purpose of this module is to improve the readability of the `timeless`
module, by separating from it interface-related functions. Beside other such
functions, this module contains so-called "segment" functions, which are mostly
used to print chunks (segments) of text to give the terminal interface its
intended look and feel.

"""

import io
import itertools
import os
import random
import string
import textwrap
import time
import datetime
import platform

from tabulate import tabulate

from .config import (
    TERMINAL_WIDTH, TERMINAL_WIDTH_DEFAULT, LINE_WIDTH, LINE_WIDTH_DEFAULT,
    RIGHT_MARGIN, INDENT, SMALL_INDENT, LARGE_INDENT,
    LINE, LINE_DEFAULT, BOLDLINE, BOLDLINE_DEFAULT, NEWLINE, TIMELESS, HOMEPAGE,
    YOUTUBE, PRELIMINARY_ROUNDS, DECK_SETS,
)

UNSUPPORTED_WINDOWS_RELEASES = {"XP", "Vista", "7"}
WINDOWS_RELEASES_WITHOUT_ANSI_TERMINAL = {"8", "8.1"}
assert platform.system() != "Windows" or platform.release() not in UNSUPPORTED_WINDOWS_RELEASES
TERMINAL_SUPPORTS_ANSI = platform.system() != "Windows" or platform.release() not in WINDOWS_RELEASES_WITHOUT_ANSI_TERMINAL

PRIMARY = "\033[96m"
SECONDARY = "\033[36m"
TIP = "\033[90m"
BRIGHT_WHITE_BOLD = "\033[97;1m"
CLEAR = "\033[0m"
CLEAR_LINE = "\033[2K"
CURSOR_UP = "\033[A"

TODAY = datetime.datetime.today().date()

tournament_report = io.StringIO()


def wrap(text):
    """Wrap text to fit inside margins, with empty lines before and after."""
    text_wrapper = textwrap.TextWrapper(width=RIGHT_MARGIN, initial_indent=INDENT, subsequent_indent=INDENT)
    return NEWLINE + text_wrapper.fill(text) + NEWLINE


def colorize(color, text):
    """Apply color to text using ANSI codes."""
    if not TERMINAL_SUPPORTS_ANSI:
        return text
    return color + text + CLEAR


def supervised_input(prompt, conditions, options=None, default_tip=None):
    """Require user input to satisfy specified conditions.

    The user is asked to provide an input value. If the provided value violates
    a specified condition, a tip for correcting the input is displayed below
    the prompt, then the user has to provide another input value. This process
    is repeated until all specified conditions are satisfied.

    Parameters
    ----------
    prompt : str
        Description of desired input.
    conditions: str, list of str
        Names of conditions. A string can be passed if only one condition is
        specified, otherwise a list of strings.
        Valid strings: 'choose_from', 'alphabetical', 'less_than_25_characters',
        'integer', 'multiple_of_10', 'max_1000'.
    options: list of str, optional
        Valid input options if argument `conditions` is set to 'choose_from'.
        If `conditions` does not include 'choose_from', this argument is not
        relevant.

        As user input is first passed to the `string.capwords` function,
        strings in `options` should adhere to that same format as well.
        (defaults to None)
    default_tip : str, optional
        A default tip to be displayed below the input prompt prior to the
        first user input. The message is overwritten by any subsequent tips.
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

    (1) It is more convenient for the user. As all the checks will apply to
    the modified string, user input will not be sensitive to choice of case
    nor to consecutive whitespaces.
    (2) It looks cleaner.
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

    def display_tip(tip, is_default=False):
        """Print the tip and move cursor up again."""
        prefix = NEWLINE if is_default else ""  # to appear below the prompt, the default tip has to be moved down
        print(colorize(TIP, CLEAR_LINE + prefix + LARGE_INDENT + f'TIP: {tip}'), end='\r' + CURSOR_UP)
        nonlocal tip_is_displayed
        tip_is_displayed = True

    while True:

        if default_tip and not tip_is_displayed:
            display_tip(default_tip, is_default=True)

        user_input = string.capwords(input(colorize(BRIGHT_WHITE_BOLD, CLEAR_LINE + LARGE_INDENT + prompt)))
        check = True

        for condition in conditions:

            condition_satisfied = condition_checks.get(condition)(user_input)
            check = check and condition_satisfied

            if not condition_satisfied:
                display_tip(input_tips.get(condition))
                break

        if check:
            if tip_is_displayed:
                print(CLEAR_LINE, end='')
            return user_input


def simulate_loading(label, report=False):
    """Create a labeled loading bar.

    Parameters
    ----------
    label : str
        Text to be displayed on top of the loading bar.
    report : bool, optional
        If True, the final loading bar will be printed to the
        `tournament_report` variable.
        (defaults to False)

    Returns
    -------
    None
    """

    print()

    label = f' {label.strip()} '
    label_index = label.center(TERMINAL_WIDTH).index(label)

    lag_base = TERMINAL_WIDTH_DEFAULT / (10*TERMINAL_WIDTH)

    for progress in range(1, LINE_WIDTH + 1 - len(label)):

        bar = (SMALL_INDENT + '-'*progress).ljust(label_index)
        labeled_bar = bar[:label_index] + label + bar[label_index:]

        lag_is_long = random.choices([True, False], weights=[2, LINE_WIDTH])[0]
        lag_range = (lag_base, 4*lag_base) if lag_is_long else (0, lag_base)

        print(colorize(SECONDARY, labeled_bar), end='\r', flush=True)
        time.sleep(random.uniform(*lag_range))

    print()

    if report:
        print(NEWLINE + labeled_bar, file=tournament_report)


def center_multiline_string(multiline_string, width=TERMINAL_WIDTH, leftstrip=False):
    """Center a multiline string, with trailing whitespaces removed.

    This function preserves the original alignment of the multiline string,
    rather than simply centering each line to the provided width.

    Parameters
    ----------
    multiline_string : str
        String to be centered. May or may not contain newline characters.
    width : int, optional
        The width in respect to which to center.
        (defaults to `config.TERMINAL_WIDTH`)
    leftstrip : bool, optional
        If True, lines have leading whitespaces removed before centering.
        This is particularly useful when re-centering centered tables to
        a different width.
        (defaults to False)

    Returns
    -------
    str
        `multiline_string` centered to `width`, with trailing whitespaces
        removed, and preserved original alignment.
    """

    lines = [line.lstrip() if leftstrip else line for line in multiline_string.split(NEWLINE)]
    max_length = max(map(len, lines))
    centered_lines = [line.ljust(max_length).center(width).rstrip() for line in lines]
    centered_multiline_string = NEWLINE.join(centered_lines)

    return centered_multiline_string


def convert_to_default_width(chunk):
    """Resize a chunk of the `tournament_report` variable to default width."""

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

    The exact formatting of the text in the `tournament_report` variable
    depends on the width of the user's terminal. For the sake of consistency,
    the contents of the `tournament_report` variable are resized to the
    default width `config.TERMINAL_WIDTH_DEFAULT` before saving.
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
        print(wrap('Sorry, a system-related error occurred. Unable to save report.'))

    except Exception:
        print(wrap('Sorry, an unexpected error occurred. Unable to save report.'))

    else:
        print(wrap(f'Report saved to {filename}!'))


def segment_initial():
    """Print general information on the TIMELESS format."""
    text = (
        "Welcome to TIMELESS, a custom 4-player tournament format for the Yu-Gi-Oh! Trading Card Game. Created out of "
        "a desire for high-level gameplay, TIMELESS is designed to facilitate long, strategic games, while staying "
        "true to the core concepts of classic Yu-Gi-Oh!"
    )
    links = center_multiline_string(tabulate([
        ["home:", HOMEPAGE],
        ["youtube:", YOUTUBE]
    ],
        tablefmt="plain",
        colalign=("right", "left")
    ))

    component_1 = colorize(PRIMARY, 3*NEWLINE + center_multiline_string(TIMELESS) + 2*NEWLINE)
    component_2 = colorize(SECONDARY, links)
    component_3 = NEWLINE + wrap(text)

    print(component_1, component_2, component_3, sep=NEWLINE)


def segment_enter_variant():
    """Print deck choice description."""
    text = (
        "A TIMELESS tournament consists of four rounds. The three preliminary rounds, in which each duelist faces off "
        "against every other duelist, are followed up by a final play-off round. In each round, decks from a carefully "
        "constructed deck set of four are randomly assigned to the duelists. This is done in such a way that during the "
        "course of the tournament each duelist pilots each of the decks exactly once. There are two TIMELESS deck sets:"
    )
    variants = center_multiline_string(tabulate(DECK_SETS, headers="keys", tablefmt="simple_outline")) + NEWLINE
    simulate_loading('SIGN-UP')
    print(wrap(text), variants, sep=NEWLINE)


def segment_enter_entry_fee():
    """Print entry fee description."""
    text = (
        "In order to create a prize pool, the duelists may agree on an entry fee. The prize pool is redistributed "
        "among the duelists based on their performance in the tournament."
    )
    print(wrap(text))


def segment_enter_duelists():
    """Print duelist sign-up prompt."""
    print(wrap("Finally, enter the names of the duelists."))


def segment_enter_unique_duelists(duplicate_names_string):
    """Print tip to avoid duplicate names, clear previous duelist entries."""
    tip = colorize(TIP, LARGE_INDENT + f'TIP: Enter unique names only. (Duplicate names: {duplicate_names_string}.)')
    print('', CLEAR_LINE, CLEAR_LINE, CLEAR_LINE + tip, CLEAR_LINE, sep='\r'+CURSOR_UP, end='\r')


def segment_enter_tournament_information_end():
    """Print line."""
    print(colorize(SECONDARY, NEWLINE + LINE))


def segment_starting(variant, entry_fee):
    """Print information on the TIMELESS tournament about to start."""

    component_1 = colorize(PRIMARY, 2*NEWLINE + 'T I M E L E S S'.center(TERMINAL_WIDTH).rstrip())
    component_2 = colorize(PRIMARY, f'{variant}, ¤{entry_fee}'.center(TERMINAL_WIDTH).rstrip())
    component_3 = colorize(PRIMARY, str(TODAY).center(TERMINAL_WIDTH).rstrip())
    component_4 = colorize(PRIMARY, NEWLINE + BOLDLINE + NEWLINE)

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
        component_2 = colorize(SECONDARY, 2*NEWLINE + LINE + 2*NEWLINE) + \
                      colorize(PRIMARY, NEWLINE + BOLDLINE + NEWLINE)

    print(component_1, component_2, sep=NEWLINE)
    print(component_1, component_2, sep=NEWLINE, file=tournament_report)


def segment_ending(variant, entry_fee):
    """Ask user if a tournament report should be saved and do it (or not)."""

    simulate_loading('COVERAGE')
    print(wrap("The tournament has concluded, congratulations to all duelists!"))

    save_report = supervised_input('Would you like to save a tournament report? ',
                                   'choose_from', options=['Yes', 'No'],
                                   default_tip="Enter yes or no.")
    if save_report == 'Yes':
        save_tournament_report(variant, entry_fee)
    else:
        print(wrap('Report not saved.'))

    print(colorize(SECONDARY, LINE))


def segment_final():
    """Print exit instructions."""
    input(colorize(SECONDARY, SMALL_INDENT + '(Press ENTER to exit.)'))

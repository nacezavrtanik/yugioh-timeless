"""Module containing constants for the `yugioh-timeless` package.

Some constants are technically redundant, but they improve readability.

"""

import shutil


# Used in `interface` module
MARGIN = 2
TERMINAL_WIDTH_DEFAULT = 80
TERMINAL_WIDTH = max(TERMINAL_WIDTH_DEFAULT, shutil.get_terminal_size().columns)
LINE_WIDTH_DEFAULT = TERMINAL_WIDTH_DEFAULT - 2*MARGIN
LINE_WIDTH = TERMINAL_WIDTH - 2*MARGIN

LEFT_MARGIN = 2 * MARGIN
RIGHT_MARGIN = TERMINAL_WIDTH - LEFT_MARGIN

INDENT = ' ' * LEFT_MARGIN  # == 2 * SMALL_INDENT
SMALL_INDENT = ' ' * MARGIN
LARGE_INDENT = 2 * INDENT

LINE_DEFAULT = SMALL_INDENT + '-'*LINE_WIDTH_DEFAULT
LINE = SMALL_INDENT + '-'*LINE_WIDTH
BOLDLINE_DEFAULT = SMALL_INDENT + '='*LINE_WIDTH_DEFAULT
BOLDLINE = SMALL_INDENT + '='*LINE_WIDTH
NEWLINE = '\n'

TIMELESS = NEWLINE.join([  # based on `pyfiglet` output
    r'  ____________  ___________                   ',
    r' /_  __/  _/  |/  / ____/ /                   ',
    r'  / /  / // /|_/ / __/ / /   ________________ ',
    r' / / _/ // /  / / /___/ /   / ____/ ___/ ___/ ',
    r'/_/ /___/_/  /_/_____/ /   / __/  \__ \\__ \  ',
    r'                    / /___/ /___ ___/ /__/ /  ',
    r'                   /_____/_____//____/____/   '
])
HOMEPAGE = 'yugioh-timeless.github.io'
YOUTUBE = 'youtube.com/@Yu-Gi-OhTIMELESS'


# Used in `timeless` module
VARIANTS = ['Basic', 'Extra']
DECK_SETS = {  # also used in `interface`
    'Basic': ['Beast', 'Chaos', 'Dragon', 'Spellcaster'],
    'Extra': ['Dinosaur', 'Flip', 'Warrior', 'Zombie']
}


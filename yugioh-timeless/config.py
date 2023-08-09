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

ROUNDS = (0, 1, 2, 3)
PRELIMINARY_ROUNDS = (0, 1, 2)  # also used in `interface`
FINAL_ROUND = 3
PAIRING_CONFIGURATIONS = ([0, 1, 2, 3], [1, 3, 0, 2], [3, 0, 1, 2])
TIED_WIN_CONFIGURATIONS_AFTER_PRELIMINARIES = ([3, 1, 1, 1], [2, 2, 2, 0])
STANDING_CONFIGURATIONS = {
    0: {
        'Wins': ([1, 1, 0, 0], ),
        'Places': ([1, 1, 3, 3], )
    },
    1: {
        'Wins': ([2, 2, 0, 0], [2, 1, 1, 0], [1, 1, 1, 1]),
        'Places': ([1, 1, 3, 3], [1, 2, 2, 4], [1, 1, 1, 1])
    },
    2: {
        'Wins': ([3, 2, 1, 0], [2, 2, 1, 1], [3, 1, 1, 1], [2, 2, 2, 0]),
        'Places': ([1, 2, 3, 4], [1, 1, 3, 3], [1, 2, 2, 2], [1, 1, 1, 4])
    },
    3: {  # final round if NO TIE after preliminaries
        'Wins': ([4, 2, 2, 0], [4, 2, 1, 1], [3, 3, 2, 0], [3, 3, 1, 1], [3, 2, 2, 1]),
        'Places': ([1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]),
        'Points': ([10, 6, 4, 0], [10, 6, 3, 1], [9, 7, 4, 0], [9, 7, 3, 1], [9, 6, 4, 1])
    },
    4: {  # final round IF TIE after preliminaries
        'Wins': ([4, 2, 1, 1], [3, 3, 2, 0], [3, 2, 2, 1]),
        'Places': ([1, 2, 3, 3], [1, 1, 3, 4], [1, 2, 2, 4]),
        'Points': ([10, 6, 2, 2], [8, 8, 4, 0], [9, 5, 5, 1])
    }
}

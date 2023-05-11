"""Module containing constants for the Yugioh TIMELESS tournament format."""


# Used in `interface` module
LINE_WIDTH = 80
LEFT_MARGIN = 4
RIGHT_MARGIN = LINE_WIDTH - LEFT_MARGIN
INDENT = LEFT_MARGIN * ' '
LARGE_INDENT = 2 * INDENT

GIT = 'git-url'
YOUTUBE = 'youtube-url'

BOLDLINE = LINE_WIDTH * '='
NEWLINE = '\n'

TIMELESS = NEWLINE.join([
    r'  ____________  ___________    ________________',
    r' /_  __/  _/  |/  / ____/ /   / ____/ ___/ ___/',
    r'  / /  / // /|_/ / __/ / /   / __/  \__ \\__ \ ',
    r' / / _/ // /  / / /___/ /___/ /___ ___/ /__/ / ',
    r'/_/ /___/_/  /_/_____/_____/_____//____/____/  '
])


# Used in `timeless` module
FORMATS = ['Basic', 'Extra']
DECK_SETS = {
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

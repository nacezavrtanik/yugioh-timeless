"""Module containing constants for the Yugioh TIMELESS tournament format."""

# interface.py
LINE_WIDTH = 80
LEFT_MARGIN = 4
RIGHT_MARGIN = LINE_WIDTH - LEFT_MARGIN
INDENT = LEFT_MARGIN * ' '
LARGE_INDENT = 2 * INDENT

TIMELESS = 'T I M E L E S S'.center(LINE_WIDTH)
GIT = 'git: link'.center(LINE_WIDTH)
YOUTUBE = 'youtube: link'.center(LINE_WIDTH)
LINE = LINE_WIDTH * '-'
BOLD_LINE = LINE_WIDTH * '='
NEWLINE = '\n'

# timeless.py
WINS = 'Wins'
DUELIST = 'Duelist'
PLACE = 'Place'
POINTS = 'Points'
PRIZES = 'Prizes'

ROUNDS = (0, 1, 2, 3)
PRELIMINARY_ROUNDS = (0, 1, 2)
FINAL_ROUND = 3
PAIRING_CONFIGURATIONS = ([0, 1, 2, 3], [1, 3, 0, 2], [3, 0, 1, 2])
STANDING_CONFIGURATIONS = {
    0: {
        WINS: ([1, 1, 0, 0], ),
        PLACE: ([1, 1, 3, 3], ),
        POINTS: (None, )
    },
    1: {
        WINS: ([2, 2, 0, 0], [2, 1, 1, 0], [1, 1, 1, 1]),
        PLACE: ([1, 1, 3, 3], [1, 2, 2, 4], [1, 1, 1, 1]),
        POINTS: (None, None, None)
    },
    2: {
        WINS: ([3, 2, 1, 0], [2, 2, 1, 1], [3, 1, 1, 1], [2, 2, 2, 0]),
        PLACE: ([1, 2, 3, 4], [1, 1, 3, 3], [1, 2, 2, 2], [1, 1, 1, 4]),
        POINTS: (None, None, None, None)
    },
    3: {  # final round if NO TIE after preliminaries
        WINS: ([4, 2, 2, 0], [4, 2, 1, 1], [3, 3, 2, 0], [3, 3, 1, 1], [3, 2, 2, 1]),
        PLACE: ([1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]),
        POINTS: ([10, 6, 4, 0], [10, 6, 3, 1], [9, 7, 4, 0], [9, 7, 3, 1], [9, 6, 4, 1])
    },
    4: {  # final round IF TIE after preliminaries
        WINS: ([4, 2, 1, 1], [3, 3, 2, 0], [3, 2, 2, 1]),
        PLACE: ([1, 2, 3, 3], [1, 1, 3, 4], [1, 2, 2, 4]),
        POINTS: ([10, 6, 2, 2], [8, 8, 4, 0], [9, 5, 5, 1])
    }
}
TIED_WIN_CONFIGURATIONS_AFTER_PRELIMINARIES = ([3, 1, 1, 1], [2, 2, 2, 0])

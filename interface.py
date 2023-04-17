"""  """

import time
from tabulate import tabulate


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

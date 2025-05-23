
import random
import collections
from timeless.utils import generate_indented_repr


TIMELESS_SQUARES = [
        [[0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]],
        [[0, 1, 3, 2], [0, 1, 3, 2], [1, 0, 2, 3], [1, 0, 2, 3]],
        [[0, 3, 1, 2], [2, 1, 3, 0], [3, 0, 2, 1], [1, 2, 0, 3]],
        [[0, 2, 1, 3], [3, 1, 2, 0], [3, 1, 2, 0], [0, 2, 1, 3]],
        [[0, 2, 3, 1], [3, 1, 0, 2], [1, 3, 2, 0], [2, 0, 1, 3]],
        [[0, 3, 2, 1], [2, 1, 0, 3], [0, 3, 2, 1], [2, 1, 0, 3]],
        [[0, 1, 2, 3], [0, 1, 2, 3], [1, 0, 2, 3], [1, 0, 2, 3]],
        [[0, 1, 3, 2], [0, 1, 3, 2], [0, 1, 2, 3], [0, 1, 2, 3]],
        [[0, 3, 1, 2], [2, 1, 3, 0], [3, 1, 2, 0], [0, 2, 1, 3]],
        [[0, 2, 1, 3], [3, 1, 2, 0], [3, 0, 2, 1], [1, 2, 0, 3]],
        [[0, 2, 3, 1], [3, 1, 0, 2], [0, 3, 2, 1], [2, 1, 0, 3]],
        [[0, 3, 2, 1], [2, 1, 0, 3], [1, 3, 2, 0], [2, 0, 1, 3]],
        [[0, 1, 2, 3], [2, 1, 0, 3], [0, 1, 2, 3], [2, 1, 0, 3]],
        [[0, 1, 3, 2], [2, 1, 3, 0], [1, 0, 2, 3], [1, 2, 0, 3]],
        [[0, 3, 1, 2], [0, 1, 3, 2], [3, 0, 2, 1], [1, 0, 2, 3]],
        [[0, 2, 1, 3], [3, 1, 0, 2], [3, 1, 2, 0], [2, 0, 1, 3]],
        [[0, 2, 3, 1], [3, 1, 2, 0], [1, 3, 2, 0], [0, 2, 1, 3]],
        [[0, 3, 2, 1], [0, 1, 2, 3], [0, 3, 2, 1], [0, 1, 2, 3]],
        [[0, 1, 2, 3], [3, 1, 2, 0], [3, 1, 2, 0], [0, 1, 2, 3]],
        [[0, 1, 3, 2], [3, 1, 0, 2], [1, 3, 2, 0], [1, 0, 2, 3]],
        [[0, 3, 1, 2], [2, 1, 0, 3], [0, 3, 2, 1], [1, 2, 0, 3]],
        [[0, 2, 1, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 2, 1, 3]],
        [[0, 2, 3, 1], [0, 1, 3, 2], [1, 0, 2, 3], [2, 0, 1, 3]],
        [[0, 3, 2, 1], [2, 1, 3, 0], [3, 0, 2, 1], [2, 1, 0, 3]],
]


IndexPair = collections.namedtuple("IndexPair", ("duelist", "deck"))


class Square:
    def __init__(self, rows):
        self.rows = rows

    @classmethod
    def random(cls):
        return cls(random.choice(TIMELESS_SQUARES))

    def __repr__(self):
        return generate_indented_repr(
            f"{self.__class__.__qualname__}([",
            ",\n".join(map(repr, self.rows)),
            f"])",
        )

    def __str__(self):
        return "\n".join(
            str(row).replace(",", "").strip("[]") for row in self.rows
        )

    def __getitem__(self, key):
        return self.rows[key]

    def _draw_pairings_for_preliminaries(self, record):
        valid_index_pairs = [
            pair for i in range(4) for j in range(4)
            if i != j and (pair := IndexPair(i, j)) not in record.exhausted_pairs
        ]
        first = random.choice(valid_index_pairs)

        for second_duelist in range(4):
            if self[first.duelist][second_duelist] == first.deck:
                break
        second_deck = self[second_duelist][first.duelist]
        second = IndexPair(second_duelist, second_deck)

        remaining_duelists = [
            duelist for duelist in range(4)
            if duelist not in [first.duelist, second.duelist]
        ]
        third_duelist, fourth_duelist = random.sample(remaining_duelists, 2)
        third_deck = self[third_duelist][fourth_duelist]
        fourth_deck = self[fourth_duelist][third_duelist]
        third = IndexPair(third_duelist, third_deck)
        fourth = IndexPair(fourth_duelist, fourth_deck)

        return (first, second), (third, fourth)

    def _draw_pairings_for_finals(self, record):
        if record.is_tied:
            first, second, third, fourth = [
                IndexPair(index, index) for index in random.sample(range(4), 4)
            ]
        else:
            first, second, third, fourth = [
                IndexPair(index, index) for index in sorted(
                    record.duelist_win_count,
                    key=lambda x: record.duelist_win_count.get(x),
                    reverse=True,
                )
            ]
        return (first, second), (third, fourth)

    def draw_pairings(self, record):
        if record.round.is_final:
            return self._draw_pairings_for_finals(record)
        return self._draw_pairings_for_preliminaries(record)

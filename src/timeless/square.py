
import random
import collections
from timeless.utils import generate_indented_repr
from timeless.config import TIMELESS_SQUARES


IndexPair = collections.namedtuple("IndexPair", ["duelist", "deck"])


class Square:
    def __init__(self, rows=None):
        self.rows = rows or random.choice(TIMELESS_SQUARES)

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

    def _draw_pairs_for_preliminaries(self, tournament):
        valid_index_pairs = [
            pair for i in range(4) for j in range(4)
            if i != j and (pair := IndexPair(i, j)) not in tournament.record
        ]
        first = random.choice(valid_index_pairs)

        for second_duelist in range(4):
            if self[first.duelist][second_duelist] == first.deck:
                break
        second_deck = self[second_duelist][first.duelist]
        second = IndexPair(second_duelist, second_deck)

        # TODO: shuffle
        third_duelist, fourth_duelist = [
            duelist for duelist in range(4)
            if duelist not in [first.duelist, second.duelist]
        ]
        third_deck = self[third_duelist][fourth_duelist]
        fourth_deck = self[fourth_duelist][third_duelist]
        third = IndexPair(third_duelist, third_deck)
        fourth = IndexPair(fourth_duelist, fourth_deck)

        return first, second, third, fourth

    def _draw_pairs_for_finals(self, tournament):
        assert tournament.tied_after_preliminaries is not None
        if tournament.tied_after_preliminaries:
            ...
        else:
            ...

    def draw_pairs(self, tournament):
        if tournament.round + 1 == 4:
            return self._draw_pairs_for_finals(tournament)
        return self._draw_pairs_for_preliminaries(tournament)

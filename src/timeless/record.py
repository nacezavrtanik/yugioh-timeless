
import itertools
from timeless.round import Round
from timeless.standings import Standings
from timeless.utils import generate_indented_repr


class Record:
    def __init__(self, pairings=None, results=None):
        self.pairings = pairings or []
        self.results = results or {}

    def __repr__(self):
        return generate_indented_repr(
            f"{self.__class__.__qualname__}([",
            ",\n".join(map(repr, self.pairings)),
            "])",
        )

    @property
    def round(self):
        return Round(self)

    @property
    def standings(self):
        return Standings(self)

    @property
    def current_pairings(self):
        if not self.pairings:
            return tuple()
        return self.pairings[-1]

    @property
    def pairs(self):
        return set(
            itertools.chain.from_iterable(
                itertools.chain.from_iterable(self.pairings)
            )
        )

    def add_new_pairings(self, pairings):
        self.pairings.append(pairings)

    def update_won_attribute(self, winner):
        for first, second in self.current_pairings:
            if first.duelist == winner:
                self.results[first], self.results[second] = True, False
            elif second.duelist == winner:
                self.results[first], self.results[second] = False, True
            else:
                continue
            break

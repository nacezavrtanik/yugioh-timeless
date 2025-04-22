
import functools
from timeless.round import Round
from timeless.standings import Standings as StandingsMixin
from timeless.utils import generate_indented_repr


class Record(StandingsMixin):
    def __init__(self, rounds=None):
        self.rounds = rounds or [Round(0)]

    def __repr__(self):
        return generate_indented_repr(
            f"{self.__class__.__qualname__}([",
            ",\n".join(map(repr, self.rounds)),
            "])",
        )

    @property
    def round(self):
        return self.rounds[-1]

    @property
    def pairings(self):
        return self.round.pairings

    @property
    def results(self):
        return functools.reduce(
            lambda x, y: x | y,
            (round.results for round in self.rounds if round.results is not None),
            dict(),
        )

    @property
    def exhausted_pairs(self):
        return set().union(*(
            round.pairs for round in self.rounds if round.pairs is not None
        ))

    def advance_round(self):
        round = Round(len(self.rounds))
        self.rounds.append(round)

    def set_pairings(self, pairings):
        self.round.pairings = pairings

    def set_results(self, winner_1, winner_2):
        winners = [winner_1, winner_2]
        results = {}
        for first, second in self.pairings:
            if first.duelist in winners:
                results[first], results[second] = True, False
            elif second.duelist in winners:
                results[first], results[second] = False, True
            else:
                raise RuntimeError("invalid winner input")
        self.round.results = results

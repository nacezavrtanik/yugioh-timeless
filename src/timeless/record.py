
import collections
import itertools
from timeless.round import Round
from timeless.utils import generate_indented_repr


class Record:
    def __init__(self, rounds=None):
        self.rounds = rounds or [Round()]

    def __repr__(self):
        return generate_indented_repr(
            f"{self.__class__.__qualname__}([",
            ",\n".join(map(repr, self.rounds)),
            "])",
        )

    @property
    def pairs(self):
        return itertools.chain.from_iterable(self.rounds)

    @property
    def current_round(self):
        return self.rounds[-1]

    @property
    def win_count(self):
        default = dict.fromkeys(range(4), 0)
        duelist_to_wins = collections.Counter(
            pair.duelist for pair in itertools.chain.from_iterable(self.rounds)
            if pair.won is True
        )
        duelist_to_wins = default | duelist_to_wins
        sorted_by_wins = {
            duelist: duelist_to_wins.get(duelist) for duelist in sorted(
                duelist_to_wins,
                reverse=True,
                key=lambda x: duelist_to_wins.get(x),
            )
        }
        return sorted_by_wins

    @property
    def win_configuration(self):
        return list(self.win_count.values())

    def add_new_round(self, pairs):
        new_round = Round(self.current_round.number + 1, list(pairs))
        self.rounds.append(new_round)

    def update_won_attribute(self, winner):
        for first, second in itertools.batched(self.current_round, 2):
            if first.duelist == winner:
                first.won, second.won = True, False
            elif second.duelist == winner:
                first.won, second.won = False, True
            else:
                continue
            break

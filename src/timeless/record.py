
import collections
import itertools
from timeless.utils import generate_indented_repr
from timeless.config import TIED_WIN_CONFIGURATIONS_AFTER_PRELIMINARIES


class Round:
    def __init__(self, number, pairs):
        self.number = number
        self.pairs = pairs

    def __repr__(self):
        pairs_repr = generate_indented_repr(
            "[", ",\n".join(map(repr, self.pairs)), "]"
        )
        return generate_indented_repr(
            f"{self.__class__.__qualname__}(",
            ",\n".join([
                f"number={self.number!r}",
                f"pairs={pairs_repr}",
            ]),
            f")",
        )

    def __iter__(self):
        return iter(self.pairs)

    @property
    def has_concluded(self):
        return all(pair.won is not None for pair in self.pairs)

    @property
    def is_final(self):
        return self.number == 4


class Record:
    # TODO: add stack for back and fore
    def __init__(self, rounds=None):
        self.rounds = rounds or []

    def __repr__(self):
        if len(self) == 0:
            repr_string = f"{self.__class__.__qualname__}({self.rounds!r})"
        else:
            repr_string = generate_indented_repr(
                f"{self.__class__.__qualname__}([",
                ",\n".join(map(repr, self.rounds)),
                "])",
            )
        return repr_string

    def __contains__(self, value):
        return value in itertools.chain.from_iterable(self.rounds)

    def __len__(self):
        return len(self.rounds)

    @property
    def current_round(self):
        if not self.rounds:
            return None
        return self.rounds[-1]

    @property
    def win_count(self):
        default = dict.fromkeys(range(4), 0)
        duelist_to_wins = collections.Counter(
            pair.duelist for pair in itertools.chain.from_iterable(self.rounds)
            if pair.won is True
        )
        return default | duelist_to_wins

    @property
    def tied_after_preliminaries(self):
        if not any([
            self.current_round.number == 3 and self.current_round.has_concluded,
            self.current_round.number == 4,
        ]):
            return None
        win_configuration = list(reversed(sorted(self.win_count.values())))
        return win_configuration in TIED_WIN_CONFIGURATIONS_AFTER_PRELIMINARIES

    def add_new_round(self, pairs):
        new_round = Round(len(self) + 1, list(pairs))
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


import itertools
from timeless.utils import generate_indented_repr


class Round:
    def __init__(self, number, pairs):
        self.number = number
        self.pairs = pairs

    def __repr__(self):
        return (
            f"{self.__class__.__qualname__}("
            f"number={self.number!r}, pairs={self.pairs!r}"
            f")"
        )

    def __iter__(self):
        return iter(self.pairs)


class Record:
    # TODO: add stack for back and fore
    def __init__(self, rounds=None):
        self.rounds = rounds or []

    def __repr__(self):
        indent = 4 * " "
        if len(self) <= 1:
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

    def add_new_round(self, pairs):
        new_round = Round(len(self) + 1, list(pairs))
        self.rounds.append(new_round)



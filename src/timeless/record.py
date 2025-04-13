
import itertools
from timeless.utils import generate_indented_repr


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
    def win_configuration(self):
        ...

    def add_new_round(self, pairs):
        new_round = Round(len(self) + 1, list(pairs))
        self.rounds.append(new_round)



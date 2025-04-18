
from timeless.utils import generate_indented_repr


class Round:
    def __init__(self, number=0, pairs=None):
        self.number = number
        self.pairs = pairs
        assert (self.number == 0 and self.pairs is None) or len(self.pairs) == 4

    def __repr__(self):
        if self.number == 0:
            return f"{self.__class__.__qualname__}(number={self.number!r}, pairs={self.pairs!r})"
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
        return iter(self.pairs or ())

    @property
    def has_concluded(self):
        return all(pair.won is not None for pair in self)

    @property
    def is_preround(self):
        return self.number == 0

    @property
    def is_preliminary(self):
        return self.number in {1, 2, 3}

    @property
    def is_last_before_finals(self):
        return self.number == 3

    @property
    def is_final(self):
        return self.number == 4



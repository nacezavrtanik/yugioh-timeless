
from timeless.utils import generate_indented_repr


class Round:
    def __init__(self, number, pairings=None, results=None):
        self.number = number
        self.pairings = pairings
        self.results = results

    def __repr__(self):
        if self.pairings is self.results is None:
            return (
                f"{self.__class__.__qualname__}("
                f"number={self.number}, "
                f"pairings={self.pairings}, "
                f"results={self.results})"
            )
        return generate_indented_repr(
            f"{self.__class__.__qualname__}(",
            ",\n".join([
                f"number={self.number!r}",
                f"pairings={self.pairings!r}",
                f"results={self.results!r}",
            ]),
            f")",
        )

    @property
    def is_preround(self):
        return self.number == 0

    @property
    def is_preliminary(self):
        return self.number in {1, 2, 3}

    @property
    def is_final(self):
        return self.number == 4

    @property
    def pairs(self):
        if self.pairings is None:
            return None
        return set(pair for pairing in self.pairings for pair in pairing)

    @property
    def has_concluded(self):
        if self.is_preround:
            return True
        if self.results is None:
            return False
        return self.pairs == set(self.results)

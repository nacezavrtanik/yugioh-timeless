
from timeless.utils import generate_indented_repr


class Round:
    def __init__(self, record):
        self.record = record

    def __repr__(self):
        # TODO
        return f"{self.__class__.__qualname__}(number={self.number!r})"

    @property
    def number(self):
        return len(self.record.pairings)

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

    @property
    def has_concluded(self):
        return self.record.pairs == set(self.record.results)

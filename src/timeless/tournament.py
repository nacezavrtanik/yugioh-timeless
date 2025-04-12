
from timeless.utils import generate_indented_repr
from timeless.entities import Duelist, Deck
from timeless.square import Square
from timeless.record import Round, Record


class Tournament:
    def __init__(self, duelists, decks, square=None, record=None):
        self.duelists = [
            Duelist(i, duelist, self) for i, duelist in enumerate(duelists)
        ]
        self.decks = [
            Deck(i, deck, self) for i, deck in enumerate(decks)
        ]
        self.square = Square(square)
        self.record = Record(record)

    def __repr__(self):
        duelists_repr = generate_indented_repr(
            "[", ",\n".join(map(repr, self.duelists)), "]"
        )
        decks_repr = generate_indented_repr(
            "[", ",\n".join(map(repr, self.decks)), "]"
        )
        return generate_indented_repr(
            f"{self.__class__.__qualname__}(",
            ",\n".join([
                f"duelists={duelists_repr}",
                f"decks={decks_repr}",
                f"square={self.square!r}",
                f"record={self.record!r}",
            ]),
            f")",
        )

    @property
    def round(self):
        return len(self.record)

    @property
    def tied_after_preliminaries(self):
        # TODO: round_has_concluded, IndexPair -> dataclass, check in Record
        ...

    def advance_round(self):
        pairs = self.square.draw_pairs(self)
        new_round = Round(pairs)
        self.record.update_round(new_round)

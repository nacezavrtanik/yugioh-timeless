
from timeless.entities import Duelist, Deck
from timeless.square import Square
from timeless.record import Record
from timeless.utils import generate_indented_repr


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
        return self.record.current_round

    def advance_round(self):
        pairs = self.square.draw_pairs(self.record)
        self.record.add_new_round(pairs)

    def update_record(self, winner):
        for duelist in self.duelists:
            if duelist.name == winner:
                self.record.update_won_attribute(duelist.index)
                break

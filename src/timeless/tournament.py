
from timeless.square import Square
from timeless.record import Record
from timeless.utils import generate_indented_repr


class Tournament:
    def __init__(self, duelists, decks, square, record):
        self.duelists = duelists
        self.decks = decks
        self.square = square
        self.record = record

    def __repr__(self):
        return generate_indented_repr(
            f"{self.__class__.__qualname__}(",
            ",\n".join([
                f"duelists={self.duelists!r}",
                f"decks={self.decks!r}",
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

    def update_record(self, winner_index):
        self.record.update_won_attribute(winner_index)


from timeless.square import Square
from timeless.record import Record
from timeless.utils import generate_indented_repr


class Tournament:
    def __init__(self, duelists, decks, entry_fee, square, record):
        self.duelists = duelists
        self.decks = decks
        self.entry_fee = entry_fee
        self.square = square
        self.record = record

    def __repr__(self):
        return generate_indented_repr(
            f"{self.__class__.__qualname__}(",
            ",\n".join([
                f"duelists={self.duelists!r}",
                f"decks={self.decks!r}",
                f"entry_fee={self.entry_fee!r}",
                f"square={self.square!r}",
                f"record={self.record!r}",
            ]),
            f")",
        )

    @property
    def duelists_to_indices(self):
        return {duelist: index for index, duelist in self.duelists.items()}

    @property
    def decks_to_indices(self):
        return {deck: index for index, deck in self.decks.items()}

    @property
    def pairings(self):
        first_pairing, second_pairing = (
            tuple(
                (self.duelists.get(pair.duelist), self.decks.get(pair.deck))
                for pair in pairing
            ) for pairing in self.record.current_pairings
        )
        return first_pairing, second_pairing

    @property
    def standings(self):
        duelist_standings = self.record.standings.current_standings
        deck_standings = self.record.standings.current_deck_standings
        assert duelist_standings and deck_standings
        if duelist_standings is None:
            return None

        standings = {}

        named_duelist_standings = {}
        for duelist, standing in duelist_standings.items():
            if (points := standing.get("points")) is not None:
                standing["prize"] = f"¤{points * int(self.entry_fee / 5)}"
            named_duelist_standings[self.duelists.get(duelist)] = standing
        standings["duelists"] = named_duelist_standings

        named_deck_standings = {
            self.decks.get(deck): standing
            for deck, standing in deck_standings.items()
        }
        standings["decks"] = named_deck_standings

        return standings

    def advance_round(self):
        pairings = self.square.draw_pairings(self.record)
        self.record.add_new_pairings(pairings)

    def update_results(self, winner):
        winner_index = self.duelists_to_indices.get(winner)
        self.record.update_won_attribute(winner_index)

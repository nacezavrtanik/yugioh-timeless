
from timeless.square import Square
from timeless.record import Record
from timeless.utils import generate_indented_repr


TIED_WIN_CONFIGURATIONS_AFTER_PRELIMINARIES = [3, 1, 1, 1], [2, 2, 2, 0]
STANDING_CONFIGURATIONS = {
    1: {
        'wins': ([1, 1, 0, 0], ),
        'place': ([1, 1, 3, 3], )
    },
    2: {
        'wins': ([2, 2, 0, 0], [2, 1, 1, 0], [1, 1, 1, 1]),
        'place': ([1, 1, 3, 3], [1, 2, 2, 4], [1, 1, 1, 1])
    },
    3: {
        'wins': ([3, 2, 1, 0], [2, 2, 1, 1], [3, 1, 1, 1], [2, 2, 2, 0]),
        'place': ([1, 2, 3, 4], [1, 1, 3, 3], [1, 2, 2, 2], [1, 1, 1, 4])
    },
    4: {  # final round if NO TIE after preliminaries
        'wins': ([4, 2, 2, 0], [4, 2, 1, 1], [3, 3, 2, 0], [3, 3, 1, 1], [3, 2, 2, 1]),
        'place': ([1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]),
        'points': ([10, 6, 4, 0], [10, 6, 3, 1], [9, 7, 4, 0], [9, 7, 3, 1], [9, 6, 4, 1])
    },
    4+1: {  # final round IF TIE after preliminaries
        'wins': ([4, 2, 1, 1], [3, 3, 2, 0], [3, 2, 2, 1]),
        'place': ([1, 2, 3, 3], [1, 1, 3, 4], [1, 2, 2, 4]),
        'points': ([10, 6, 2, 2], [8, 8, 4, 0], [9, 5, 5, 1])
    }
}


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
    def round(self):
        return self.record.current_round

    @property
    def has_concluded(self):
        return self.round.is_final and self.round.has_concluded

    @property
    def tied_after_preliminaries(self):
        if not any([
            self.round.is_last_before_finals and self.round.has_concluded,
            self.round.is_final,
        ]):
            return None
        return self.record.win_configuration in TIED_WIN_CONFIGURATIONS_AFTER_PRELIMINARIES

    @property
    def pairings(self):
        first_pairing, second_pairing = (
            tuple(
                (self.duelists.get(pair.duelist), self.decks.get(pair.deck))
                for pair in pairing
            ) for pairing in self.round.pairings
        )
        return first_pairing, second_pairing

    @property
    def standings(self):
        if self.round.is_preround or not self.round.has_concluded:
            return None
        candidates = STANDING_CONFIGURATIONS.get(
            self.round.number + bool(self.tied_after_preliminaries)
        )
        index = candidates.get("wins").index(self.record.win_configuration)
        standings = {
            self.duelists.get(duelist): {
                label: candidates[label][index][list(self.record.win_count).index(duelist)]
                for label in candidates
            }
            for duelist in range(4)
        }
        if self.round.is_final and self.entry_fee:
            standings = {
                duelist: standings.get(duelist) | {
                    "prize": f"¤{standings.get(duelist).get('points') * int(self.entry_fee / 5)}"
                }
                for duelist in standings
            }
        return standings

    @property
    def deck_standings(self):
        if self.round.is_preround or not self.round.has_concluded:
            return None
        deck_standings = {
            self.decks.get(deck): wins
            for deck, wins in self.record.deck_win_count.items()
        }
        return deck_standings

    def advance_round(self):
        pairs = self.square.draw_pairs(self)
        self.record.add_new_round(pairs)

    def update_results(self, winner):
        winner_index = self.duelists_to_indices.get(winner)
        self.record.update_won_attribute(winner_index)

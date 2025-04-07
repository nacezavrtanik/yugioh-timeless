import random
from .duelist import Duelist


class Tournament:
    TOTAL_DUELISTS = 4
    FINAL_ROUND = 4
    TIED_WIN_CONFIGURATIONS_AFTER_PRELIMINARIES = (3, 1, 1, 1), (2, 2, 2, 0)

    def __init__(
        self,
        duelists: list[Duelist],
        decks: list[str],
        round: int = 1,
    ):
        assert len(duelists) == 4
        self.duelists = duelists
        assert len(decks) == 4
        self.decks = decks
        assert 1 <= round <= self.FINAL_ROUND
        self.round = round

    @property
    def standing_configuration(self) -> tuple[int, int, int, int]:
        return tuple(duelist.wins for duelist in self.duelists)

    @property
    def is_tied_after_preliminaries(self) -> bool | None:
        if self.round != self.FINAL_ROUND:
            return None
        return self.standing_configuration in self.TIED_WIN_CONFIGURATIONS_AFTER_PRELIMINARIES

    def generate_pairings(self):
        decks = self.decks.copy()
        random.shuffle(decks)
        for duelist, deck in zip(self.duelists, decks):
            duelist.update_deck(deck)
            print(f"assigning deck {deck} to {duelist}")

    def update_records(self, winners):
        assert len(winners) == self.TOTAL_DUELISTS / 2
        for duelist in self.duelists:
            print(f"updating records for {duelist}")
            duelist.update_wins(duelist in winners)

    def advance_round(self):
        self.round += 1

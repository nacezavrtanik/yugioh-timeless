import random
from .entities import Duelist, Deck


class Tournament:
    TOTAL_DUELISTS = 4
    FINAL_ROUND = 4
    TIED_WIN_CONFIGURATIONS_AFTER_PRELIMINARIES = (3, 1, 1, 1), (2, 2, 2, 0)

    def __init__(
        self,
        duelists: list[Duelist],
        decks: list[Deck],
        round: int = 1,
    ):
        assert len(duelists) == 4
        self.duelists = duelists
        assert len(decks) == 4
        self.decks = decks
        assert 1 <= round <= self.FINAL_ROUND
        self.round = round

    @property
    def is_pre_match(self) -> bool:
        assert len({len(duelist.record) for duelist in self.duelists}) == 1
        record_length = len(self.duelists[0].record)
        assert record_length in {self.round, self.round - 1}
        return record_length == self.round - 1

    @property
    def standing_configuration(self) -> tuple[int, int, int, int]:
        return tuple(duelist.wins for duelist in self.duelists)

    @property
    def is_tied_after_preliminaries(self) -> bool | None:
        if self.round != self.FINAL_ROUND:
            return None
        return self.standing_configuration in self.TIED_WIN_CONFIGURATIONS_AFTER_PRELIMINARIES

    @property
    def has_concluded(self):
        return self.round == self.FINAL_ROUND and not self.is_pre_match

    def generate_pairings(self):
        assert self.is_pre_match
        decks = self.decks.copy()
        random.shuffle(decks)
        for duelist, deck in zip(self.duelists, decks):
            duelist.deck = deck
            print(f"assigning deck {deck} to {duelist}")

    def update_records(self, winners):
        assert self.is_pre_match
        assert len(winners) == self.TOTAL_DUELISTS / 2
        for duelist in self.duelists:
            print(f"updating records for {duelist}")
            duelist.update_record(duelist in winners)

    def advance_round(self):
        assert not self.is_pre_match
        self.round += 1
        assert self.is_pre_match

import random
from .duelist import Duelist
from .config import TIMELESS_SQUARES


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
        self.matchups = random.choice(TIMELESS_SQUARES)

    @property
    def standing_configuration(self) -> tuple[int, int, int, int]:
        return tuple(duelist.wins for duelist in self.duelists)

    @property
    def is_tied_after_preliminaries(self) -> bool | None:
        if self.round != self.FINAL_ROUND:
            return None
        return self.standing_configuration in self.TIED_WIN_CONFIGURATIONS_AFTER_PRELIMINARIES

    def generate_pairings(self):
        paired_duelists = []
        for duelist in self.duelists:
            if duelist.name in paired_duelists:
                continue
            invalid_choices = [duelist.name] + paired_duelists + duelist.opponent_record
            opponent = random.choice([
                duelist for duelist in self.duelists if duelist.name not in invalid_choices
            ])
            paired_duelists.extend([duelist.name, opponent.name])
            duelist.update_opponent(opponent.name)
            opponent.update_opponent(duelist.name)
            x, y = self.duelists.index(duelist), self.duelists.index(opponent)
            duelist.update_deck(self.decks[self.matchups[x][y]])
            opponent.update_deck(self.decks[self.matchups[y][x]])

    def update_records(self, winners):
        assert len(winners) == self.TOTAL_DUELISTS / 2
        for duelist in self.duelists:
            duelist.update_wins(duelist.name in winners)

    def advance_round(self):
        self.round += 1

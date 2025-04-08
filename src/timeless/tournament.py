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

    def assign_decks(self):
        picked_decks = []
        for duelist in self.duelists:
            invalid_choices = picked_decks + duelist.deck_record
            new_deck = random.choice([
                deck for deck in self.decks if deck not in invalid_choices
            ])
            picked_decks.append(new_deck)
            duelist.update_deck(new_deck)

    def generate_pairings(self):
        paired_duelists = []
        for duelist in self.duelists:
            if duelist.name in paired_duelists:
                continue
            invalid_choices = [duelist.name] + paired_duelists + duelist.opponent_record
            new_opponent = random.choice([
                duelist for duelist in self.duelists if duelist.name not in invalid_choices
            ])
            paired_duelists.extend([duelist.name, new_opponent.name])
            duelist.update_opponent(new_opponent.name)
            new_opponent.update_opponent(duelist.name)

    def update_records(self, winners):
        assert len(winners) == self.TOTAL_DUELISTS / 2
        for duelist in self.duelists:
            duelist.update_wins(duelist.name in winners)

    def advance_round(self):
        self.round += 1

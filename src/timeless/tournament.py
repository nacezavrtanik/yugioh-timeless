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
    ):
        assert len(duelists) == 4
        self.duelists = duelists
        assert len(decks) == 4
        self.decks = decks
        self.matchups = random.choice(TIMELESS_SQUARES)

    @property
    def round(self):
        duelist_rounds = {duelist.round for duelist in self.duelists}
        assert len(duelist_rounds) == 1
        return list(duelist_rounds)[0]

    @property
    def standing_configuration(self) -> tuple[int, int, int, int]:
        return tuple(duelist.wins for duelist in self.duelists)

    @property
    def is_tied_after_preliminaries(self) -> bool | None:
        if self.round != self.FINAL_ROUND:
            return None
        return self.standing_configuration in self.TIED_WIN_CONFIGURATIONS_AFTER_PRELIMINARIES

    def _generate_pairings_for_preliminary_round(self):
        paired_duelists = []
        for duelist in self.duelists:
            if duelist.name in paired_duelists:
                continue
            invalid_choices = [duelist.name] + paired_duelists + duelist.opponent_record
            opponent = random.choice([
                duelist for duelist in self.duelists if duelist.name not in invalid_choices
            ])
            paired_duelists.extend([duelist.name, opponent.name])
            x, y = self.duelists.index(duelist), self.duelists.index(opponent)
            duelist.update_matchup(self.decks[self.matchups[x][y]], opponent.name)
            opponent.update_matchup(self.decks[self.matchups[y][x]], duelist.name)

    def _generate_pairings_for_final_round(self):
        if self.is_tied_after_preliminaries:
            paired_duelists = []
            for duelist in self.duelists:
                if duelist.name in paired_duelists:
                    continue
                invalid_choices = [duelist.name] + paired_duelists
                opponent = random.choice([
                    duelist for duelist in self.duelists if duelist.name not in invalid_choices
                ])
                paired_duelists.extend([duelist.name, opponent.name])
                x, y = self.duelists.index(duelist), self.duelists.index(opponent)
                duelist.update_matchup(self.decks[self.matchups[x][x]], opponent.name)
                opponent.update_matchup(self.decks[self.matchups[y][y]], duelist.name)
        else:
            duelists_by_wins = sorted(self.duelists, key=lambda x: x.wins)
            for duelist, opponent in [
                (duelists_by_wins[i], duelists_by_wins[i+1])
                for i in [0, 2]
            ]:
                x, y = self.duelists.index(duelist), self.duelists.index(opponent)
                duelist.update_matchup(self.decks[self.matchups[x][x]], opponent.name)
                opponent.update_matchup(self.decks[self.matchups[y][y]], duelist.name)

    def generate_pairings(self):
        if self.round == self.FINAL_ROUND:
            self._generate_pairings_for_final_round()
        else:
            self._generate_pairings_for_preliminary_round()

    def update_records(self, winners):
        assert len(winners) == self.TOTAL_DUELISTS / 2
        for duelist in self.duelists:
            duelist.update_wins(duelist.name in winners)

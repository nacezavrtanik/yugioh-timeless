
import collections
from timeless.round import Round


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


class Standings:
    def __init__(self, record):
        self.record = record

    @property
    def tied_after_preliminaries(self):
        if not any([
            self.record.round.is_last_before_finals and self.record.round.has_concluded,
            self.record.round.is_final,
        ]):
            return None
        return self.win_configuration in TIED_WIN_CONFIGURATIONS_AFTER_PRELIMINARIES

    @property
    def current_standings(self):
        if self.record.round.is_preround or not self.record.round.has_concluded:
            return None
        candidates = STANDING_CONFIGURATIONS.get(
            self.record.round.number + bool(self.tied_after_preliminaries)
        )
        index = candidates.get("wins").index(self.win_configuration)
        standings = {
            duelist: {
                label: candidates[label][index][list(self.win_count).index(duelist)]
                for label in candidates
            }
            for duelist in range(4)
        }
        return standings

    @property
    def current_deck_standings(self):
        if self.record.round.is_preround or not self.record.round.has_concluded:
            return None
        return self.deck_win_count

    def _get_win_count(self, which):
        default = dict.fromkeys(range(4), 0)
        index_to_wins = collections.Counter(
            getattr(pair, which) for pair in self.record.pairs
            if self.record.results.get(pair) is True
        )
        index_to_wins = default | index_to_wins
        sorted_by_wins = {
            index: index_to_wins.get(index) for index in sorted(
                index_to_wins,
                reverse=True,
                key=lambda x: index_to_wins.get(x),
            )
        }
        return sorted_by_wins

    @property
    def win_count(self):
        return self._get_win_count("duelist")

    @property
    def deck_win_count(self):
        return self._get_win_count("deck")

    @property
    def win_configuration(self):
        return list(self.win_count.values())


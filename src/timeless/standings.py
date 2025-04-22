
import collections
from timeless.round import Round


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
    },
}


class Standings:
    @property
    def standings(self):
        if self.round.is_preround or not self.round.has_concluded:
            return None
        configuration_key = self.round.number
        if self.round.is_final:
            configuration_key += self.is_tied
        candidates = STANDING_CONFIGURATIONS.get(configuration_key)
        index = candidates.get("wins").index(self.duelist_win_configuration)
        duelist_standings = {
            duelist: {
                label: configurations[index][list(self.duelist_win_count).index(duelist)]
                for label, configurations in candidates.items()
            }
            for duelist in self.duelist_win_count
        }
        deck_standings = {
            deck: {"wins": wins} for deck, wins in self.deck_win_count.items()
        }
        return dict(duelists=duelist_standings, decks=deck_standings)

    @property
    def is_tied(self):
        upper_bracket = set(self.duelist_win_configuration[:2])
        lower_bracket = set(self.duelist_win_configuration[2:])
        return not upper_bracket.isdisjoint(lower_bracket)

    def _get_win_count(self, which):
        default = dict.fromkeys(range(4), 0)
        index_to_wins = collections.Counter(
            getattr(pair, which) for pair in self.exhausted_pairs
            if self.results.get(pair) is True
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
    def duelist_win_count(self):
        return self._get_win_count("duelist")

    @property
    def deck_win_count(self):
        return self._get_win_count("deck")

    @property
    def duelist_win_configuration(self):
        return list(self.duelist_win_count.values())

    @property
    def deck_win_configuration(self):
        return list(self.deck_win_count.values())

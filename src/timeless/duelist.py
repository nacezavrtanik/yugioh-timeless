
class Duelist:
    def __init__(
        self,
        name: str,
        win_record: list[int] | None = None,
        matchup_record: list[tuple[str, str]] | None = None,
    ):
        self.name = name
        self.win_record = win_record or []
        self.matchup_record = matchup_record or []

    def __repr__(self):
        return (
            f"{self.__class__.__qualname__}("
            f"name={self.name!r}, "
            f"win_record={self.win_record!r}, "
            f"matchup_record={self.matchup_record!r})"
        )

    def __str__(self):
        return self.name

    @property
    def wins(self):
        if not self.win_record:
            return 0
        return self.win_record[-1]

    @property
    def deck(self):
        if not self.deck_record:
            return None
        return self.deck_record[-1]

    @property
    def opponent(self):
        if not self.opponent_record:
            return None
        return self.opponent_record[-1]

    @property
    def deck_record(self):
        return [matchup[0] for matchup in self.matchup_record]

    @property
    def opponent_record(self):
        return [matchup[1] for matchup in self.matchup_record]

    def update_wins(self, won: bool):
        self.win_record.append(self.wins + int(won))

    def update_matchup(self, deck: str, opponent: str):
        assert (deck, opponent) not in self.matchup_record
        self.matchup_record.append((deck, opponent))

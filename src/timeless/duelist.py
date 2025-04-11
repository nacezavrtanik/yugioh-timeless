
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
        assert self.name
        assert len(self.matchup_record) <= 4
        self._validate_state()

    def _validate_state(self) -> bool:
        assert len(self.matchup_record) - len(self.win_record) in [0, 1]


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
    def wins(self) -> int | None:
        if not self.win_record:
            return None
        return self.win_record[-1]

    @property
    def deck(self) -> str | None:
        if not self.deck_record:
            return None
        return self.deck_record[-1]

    @property
    def opponent(self) -> str | None:
        if not self.opponent_record:
            return None
        return self.opponent_record[-1]

    @property
    def deck_record(self) -> list[str]:
        if not self.matchup_record:
            return []
        return [matchup[0] for matchup in self.matchup_record]

    @property
    def opponent_record(self) -> list[str]:
        if not self.matchup_record:
            return []
        return [matchup[1] for matchup in self.matchup_record]

    def update_wins(self, won: bool) -> None:
        assert self.is_dueling
        wins = 0 if self.wins is None else self.wins
        self.win_record.append(wins + int(won))
        self._validate_state()

    def update_matchup(self, deck: str, opponent: str) -> None:
        assert self.round < 4
        assert not self.is_dueling
        assert deck not in self.deck_record
        assert opponent not in self.opponent_record or self.round == 3
        assert (deck, opponent) not in self.matchup_record
        self.matchup_record.append((deck, opponent))
        self._validate_state()

    @property
    def round(self) -> int:
        return len(self.matchup_record)

    @property
    def is_dueling(self) -> bool:
        return self.round > len(self.win_record)

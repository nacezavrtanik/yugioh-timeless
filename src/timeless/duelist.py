
class Duelist:
    def __init__(
        self,
        name: str,
        win_record: list[int] | None = None,
        deck_record: list[str] | None = None,
        opponent_record: list[str] | None = None,
    ):
        self.name = name
        self.win_record = win_record or []
        self.deck_record = deck_record or []
        self.opponent_record = opponent_record or []

    def __repr__(self):
        return (
            f"{self.__class__.__qualname__}("
            f"name={self.name!r}, "
            f"win_record={self.win_record!r}, "
            f"deck_record={self.deck_record!r}, "
            f"opponent_record={self.opponent_record!r})"
        )

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

    def update_wins(self, won: bool):
        self.win_record.append(self.wins + int(won))
        print(f"updating records for {self}")

    def update_deck(self, deck: str):
        self.deck_record.append(deck)
        print(f"assigning deck {deck} to {self}")

    def update_opponent(self, name):
        self.opponent_record.append(name)
        print(f"assigning opponent {name} to {self}")

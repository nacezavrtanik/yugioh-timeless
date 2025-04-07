
class Duelist:
    def __init__(
        self,
        name: str,
        win_record: list[int] | None = None,
        deck_record: list[str] | None = None,
    ):
        self.name = name
        self.win_record = win_record or []
        self.deck_record = deck_record or []

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

    def update_wins(self, won: bool):
        self.win_record.append(self.wins + int(won))

    def update_deck(self, deck: str):
        self.deck_record.append(deck)


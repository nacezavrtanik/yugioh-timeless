
class TournamentEntity:
    def __init__(
        self,
        name: str,
        record: str = "",
    ):
        self.name = name
        self.record = record

    def __repr__(self):
        args = ", ".join([f"{key}={val}" for key, val in self.__dict__.items()])
        return f"{self.__class__.__qualname__}({args})"

    @property
    def wins(self) -> int:
        assert len(self.record) <= 4
        return int(self.record[-1]) if self.record else 0

    def update_record(self, won: bool):
        last_record = int(self.record[-1]) if self.record else 0
        self.record += str(last_record + won)


class Deck(TournamentEntity):
    pass


class Duelist(TournamentEntity):
    def __init__(
        self,
        name: str,
        record: str = "",
        deck: Deck | None = None,
    ):
        super().__init__(name, record)
        self.deck = deck
        self.place = None
        self.points = None

    def update_record(self, won: bool):
        super().update_record(won)
        self.deck.update_record(won)


class Entity:
    def __init__(self, index, name, tournament):
        self.index = index
        self.name = name
        self.tournament = tournament

    def __repr__(self):
        return (
            f"{self.__class__.__qualname__}("
            f"index={self.index!r}, "
            f"name={self.name!r}, "
            f"tournament=<{self.tournament.__class__.__qualname__}@id={id(self.tournament)}>)"
        )


class Duelist(Entity):
    ...


class Deck(Entity):
    ...


class Entity:
    def __init__(self, index, name, record):
        self.index = index
        self.name = name
        self.record = record

    def __repr__(self):
        return (
            f"{self.__class__.__qualname__}("
            f"index={self.index!r}, "
            f"name={self.name!r}, "
            f"record=<{self.record.__class__.__qualname__}@id={id(self.record)}>)"
        )


class Duelist(Entity):
    ...


class Deck(Entity):
    ...

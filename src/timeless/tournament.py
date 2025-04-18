
from timeless.square import Square
from timeless.record import Record
from timeless.standing import Standing
from timeless.utils import generate_indented_repr


class Tournament:
    def __init__(self, duelists, decks, square, record):
        self.duelists = duelists
        self.decks = decks
        self.square = square
        self.record = record

    def __repr__(self):
        return generate_indented_repr(
            f"{self.__class__.__qualname__}(",
            ",\n".join([
                f"duelists={self.duelists!r}",
                f"decks={self.decks!r}",
                f"square={self.square!r}",
                f"record={self.record!r}",
            ]),
            f")",
        )

    @property
    def round(self):
        return self.record.current_round

    @property
    def has_concluded(self):
        return self.round.is_final and self.round.has_concluded

    @property
    def tied_after_preliminaries(self):
        if not any([
            self.round.is_last_before_finals and self.round.has_concluded,
            self.round.is_final,
        ]):
            return None
        return self.record.win_configuration in Standing.TIED_WIN_CONFIGURATIONS_AFTER_PRELIMINARIES

    @property
    def standings(self):
        if self.round.is_preround or not self.round.has_concluded:
            return None
        candidates = Standing.STANDING_CONFIGURATIONS.get(
            self.round.number + bool(self.tied_after_preliminaries)
        )
        index = candidates.get("wins").index(self.record.win_configuration)
        standings = {
            duelist: {
                label: candidates[label][index][list(self.record.win_count).index(duelist)]
                for label in candidates
            }
            for duelist in self.record.win_count
        }
        standings = {duelist: Standing(**kwargs) for duelist, kwargs in standings.items()}
        return standings

    @property
    def pairings(self):
        if self.round.is_preround:
            return None
        return self.round[:2], self.round[2:]

    def advance_round(self):
        pairs = self.square.draw_pairs(self)
        self.record.add_new_round(pairs)

    def update_record(self, winner_index):
        self.record.update_won_attribute(winner_index)

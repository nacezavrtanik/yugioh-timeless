
import random
import itertools
from timeless import Tournament, Square, Record


class API:
    def __init__(self):
        self._tournament = None
        self._duelists = None
        self._decks = None
        self._entry_fee = None

    def register_duelists(self, duelists):
        self._duelists = duelists

    def register_decks(self, decks):
        self._decks = decks

    def register_entry_fee(self, entry_fee):
        self._entry_fee = entry_fee

    @property
    def tournament(self):
        if self._tournament is None:
            if any(arg is None for arg in [
                self._duelists, self._decks, self._entry_fee
            ]):
                return None
            duelists = dict(zip(range(4), random.sample(self._duelists, 4)))
            decks = dict(zip(range(4), random.sample(self._decks, 4)))
            entry_fee = self._entry_fee
            square = Square.random()
            record = Record()
            self._tournament = Tournament(duelists, decks, entry_fee, square, record)
        return self._tournament

    @property
    def duelists_to_indices(self):
        if not self.tournament:
            return None
        return {duelist: index for index, duelist in self.tournament.duelists.items()}

    def get_pairings(self):
        self.tournament.advance_round()
        return self.tournament.pairings

    def submit_winners(self, winner_1, winner_2):
        self.tournament.update_record(self.duelists_to_indices.get(winner_1))
        self.tournament.update_record(self.duelists_to_indices.get(winner_2))

    def get_standings(self):
        return self.tournament.standings

    def get_deck_standings(self):
        return self.tournament.deck_standings


_api = API()


def register_duelists(duelists):
    _api.register_duelists(duelists)


def register_decks(decks):
    _api.register_decks(decks)


def register_entry_fee(entry_fee):
    _api.register_entry_fee(entry_fee)


def get_pairings():
    return _api.get_pairings()


def submit_winners(winner_1, winner_2):
    _api.submit_winners(winner_1, winner_2)


def get_standings():
    return _api.get_standings()


def get_deck_standings():
    return _api.get_deck_standings()

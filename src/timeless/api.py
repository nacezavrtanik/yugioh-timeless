
import abc
import random
import itertools
from timeless import Tournament, Square, Record


class API(abc.ABC):

    @abc.abstractmethod
    def create_tournament(self, duelists, decks, entry_fee):
        pass

    @abc.abstractmethod
    def read_pairings(self):
        pass

    @abc.abstractmethod
    def update_results(self, winner_1, winner_2):
        pass

    @abc.abstractmethod
    def read_standings(self):
        pass


class StatefulAPI(API):
    def __init__(self):
        self.tournament = None

    def create_tournament(self, duelists, decks, entry_fee):
        duelists = dict(zip(range(4), random.sample(duelists, 4)))
        decks = dict(zip(range(4), random.sample(decks, 4)))
        square = Square.random()
        record = Record()
        self.tournament = Tournament(duelists, decks, entry_fee, square, record)

    def read_pairings(self):
        self.tournament.advance_round()
        self.tournament.draw_pairings()
        return self.tournament.pairings

    def update_results(self, winner_1, winner_2):
        self.tournament.submit_results(winner_1, winner_2)

    def read_standings(self):
        return self.tournament.standings

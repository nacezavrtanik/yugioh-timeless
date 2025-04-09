
from timeless.duelist import Duelist
from timeless.tournament import Tournament
from timeless.config import DECK_SETS


class CLI:

    def __init__(self, args):
        self.args = args
        self.tournament = None

        print("HEADER")
        self.perform_registration()
        self.run_tournament()

    def perform_registration(self):
        variant = self.args.variant or input("enter variant: ")
        decks = DECK_SETS.get(variant.capitalize())
        entry_fee = self.args.entry_fee or input("enter entry fee: ")
        duelists = self.args.duelists or input("enter duelists: ").split()
        duelists = list(map(Duelist, duelists))
        self.tournament = Tournament(duelists, decks)

    def run_tournament(self):
        for _ in range(3):
            self.tournament.assign_decks()
            self.tournament.generate_pairings()
            print("PAIRINGS")
            print(*self.tournament.duelists, sep="\n")
            winners = []
            winners.append(input("winner 1: "))
            winners.append(input("winner 2: "))
            self.tournament.update_records(winners)
            print("STANDINGS")


from timeless.tournament import Tournament
from timeless.config import DECK_SETS

import timeless.api


class CLI:

    def __init__(self, args):
        self.args = args

        print("HEADER")
        self.perform_registration()
        self.run_tournament()

    def perform_registration(self):
        if self.args.decks:
            decks = self.args.decks
        elif self.args.variant:
            decks = DECK_SETS.get(self.args.variant.capitalize())
        else:
            decks = input("enter decks or variant: ")
            decks = decks.split()
            if len(decks) == 1:
                variant = decks[0].capitalize()
                decks = DECK_SETS.get(variant.capitalize())
            elif len(decks) == 4:
                pass
        timeless.api.register_decks(decks)

        entry_fee = self.args.entry_fee or int(input("enter entry fee: "))
        timeless.api.register_entry_fee(entry_fee)

        duelists = self.args.duelists or input("enter duelists: ").split()
        timeless.api.register_duelists(duelists)

    def run_tournament(self):
        for _ in range(4):
            print("PAIRINGS")
            print(*timeless.api.get_pairings(), sep="\n")

            timeless.api.submit_winners(input("winner 1: "), input("winner 2: "))

            print("STANDINGS")
            print(*timeless.api.get_standings(), sep="\n")

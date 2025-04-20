
from timeless.parser import Parser
from timeless.tournament import Tournament
from timeless.config import DECK_SETS


class CLI:

    def __init__(self, api):
        self.api = api
        self.parser = Parser()
        self.prompter = None
        self.printer = None

    def run(self):
        print("HEADER")
        self.perform_registration()
        self.run_tournament()

    def perform_registration(self):
        args = self.parser.parse_args()
        duelists = args.duelists or input("enter duelists: ").split()
        if args.decks:
            decks = args.decks
        elif args.variant:
            decks = DECK_SETS.get(args.variant.capitalize())
        else:
            decks = input("enter decks or variant: ")
            decks = decks.split()
            if len(decks) == 1:
                variant = decks[0].capitalize()
                decks = DECK_SETS.get(variant.capitalize())
            elif len(decks) == 4:
                pass
        entry_fee = args.entry_fee or int(input("enter entry fee: "))
        self.api.create_tournament(duelists, decks, entry_fee)

    def run_tournament(self):
        for _ in range(4):
            print("PAIRINGS")
            print(*self.api.read_pairings(), sep="\n")

            self.api.update_results(input("winner 1: "), input("winner 2: "))

            standings = self.api.read_standings()
            print("STANDINGS")
            print(*standings.get("duelists").items(), sep="\n")

            print("DECK STANDINGS")
            print(*standings.get("decks").items(), sep="\n")

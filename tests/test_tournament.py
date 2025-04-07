
import pytest

import timeless


def test_tournament_round():
    try:
        decks = ["plant", "goat", "chaos", "ritual"]

        nace = timeless.Duelist("nace")
        lucija = timeless.Duelist("lucija")
        jaka = timeless.Duelist("jaka")
        tisa = timeless.Duelist("tisa")

        duelists = [nace, lucija, jaka, tisa]

        tournament = timeless.Tournament(duelists, decks)
        tournament.generate_pairings()
        tournament.update_records({nace, lucija})
        tournament.advance_round()
    except Exception as exc_info:
        pytest.fail(f"Unexpected error: {exc_info}")


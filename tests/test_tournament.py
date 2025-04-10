
import pytest

import timeless


def test_tournament_round():
    try:
        decks = ["plant", "goat", "chaos", "ritual"]
        duelists = [timeless.Duelist(name) for name in ["nace", "lucija", "jaka", "tisa"]]

        tournament = timeless.Tournament(duelists, decks)
        tournament.generate_pairings()
        tournament.update_records({"nace", "lucija"})
    except Exception as exc_info:
        pytest.fail(f"Unexpected error: {exc_info}")


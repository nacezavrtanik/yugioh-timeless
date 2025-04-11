
import pytest
from hypothesis import strategies as st, given

from test_duelist import st_duelists
import timeless
from timeless.config import TIMELESS_SQUARES


@st.composite
def st_tournaments(draw):
    duelists = draw(st.lists(st_duelists(), min_size=4, max_size=4))
    decks = draw(st.lists(st.text(min_size=1), min_size=4, max_size=4))
    matchup = draw(st.sampled_from(TIMELESS_SQUARES))
    tournament = timeless.Tournament(duelists, decks, matchup)
    return tournament


@given(
    st.lists(st.text(min_size=1), min_size=4, max_size=4, unique=True),
    st.lists(st.text(min_size=1), min_size=4, max_size=4),
    st.none(),
)
def test_tournament_init_first_round_with_duelist_strings(
    duelists, decks, matchup
):
    try:
        tournament = timeless.Tournament(duelists, decks, matchup)
    except Exception as exc_info:
        pytest.fail(f"Unexpected error: {exc_info}")


@given(st_tournaments())
def test_tournament_init(tournament):
    ...


def test_tournament_round():
    try:
        decks = ["plant", "goat", "chaos", "ritual"]
        duelists = [timeless.Duelist(name) for name in ["nace", "lucija", "jaka", "tisa"]]

        tournament = timeless.Tournament(duelists, decks)
        tournament.generate_pairings()
        tournament.update_records({"nace", "lucija"})
    except Exception as exc_info:
        pytest.fail(f"Unexpected error: {exc_info}")


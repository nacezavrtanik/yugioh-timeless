
import pytest
from hypothesis import strategies as st, given, example

import timeless


@st.composite
def win_records(draw, start=0, step=1, min_size=0, max_size=4):
    assert max_size <= 4
    size = draw(st.integers(min_value=min_size, max_value=max_size))
    records = []
    while len(records) < size:
        if records:
            last_element = records[-1]
        else:
            last_element = draw(
                st.integers(min_value=start, max_value=start + step)
            )
        next_element = draw(st.integers(
            min_value=last_element, max_value=last_element + step
        ))
        records.append(next_element)
    assert len(records) <= 4
    return records


@st.composite
def matchup_records(draw, min_size=0, max_size=4):
    assert max_size <= 4
    size = draw(st.integers(min_value=min_size, max_value=max_size))
    decks = draw(st.lists(
        st.text(min_size=1), unique=True, min_size=size, max_size=size
    ))
    opponents = draw(st.lists(
        st.text(min_size=1), unique=True, min_size=size, max_size=size
    ))
    if len(opponents) == 4:
        # Replace final element with a possibly non-unique one
        opponents[-1] = draw(st.text(min_size=1))
    records = list(zip(decks, opponents))
    assert len(records) <= 4
    return records


@st.composite
def duelists(draw, dueling=None, max_round=4):
    name = draw(st.text(min_size=1))
    win_records_max_size = max_round - 1 if dueling is True else max_round
    win_record = draw(win_records(max_size=win_records_max_size))
    win_record_length = len(win_record)
    if dueling is None:
        matchup_record_size = dict(
            min_size=win_record_length,
            max_size=min([max_round, win_record_length + 1]),
        )
    elif dueling is True:
        matchup_record_size = dict(
            min_size=win_record_length + 1,
            max_size=win_record_length + 1,
        )
    elif dueling is False:
        matchup_record_size = dict(
            min_size=win_record_length,
            max_size=win_record_length,
        )
    matchup_record = draw(matchup_records(**matchup_record_size))
    return timeless.Duelist(name, win_record, matchup_record)


@given(duelists(dueling=True), st.booleans())
def test_update_wins(duelist, won):
    wins = 0 if duelist.wins is None else duelist.wins
    duelist.update_wins(won)
    assert duelist.wins == wins + 1 if won else duelist.wins == wins


@given(
    duelists(dueling=False, max_round=3),
    st.lists(st.text(min_size=1), unique=True, min_size=4),
    st.lists(st.text(min_size=1), unique=True, min_size=3),
)
def test_update_matchup(duelist, decks, opponents):
    deck = None
    for deck in decks:
        if deck not in duelist.deck_record:
            break
    opponent = opponents[0]
    if duelist.round < 4:
        for opponent in opponents:
            if opponent not in duelist.opponent_record:
                break
    try:
        duelist.update_matchup(deck, opponent)
    except Exception as exc_info:
        pytest.fail(f"Unexpected error: {exc_info}")

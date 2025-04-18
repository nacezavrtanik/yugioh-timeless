#!/usr/bin/env python3
"""Package for running the Yugioh TIMELESS tournament format."""


__version__ = '0.1.1-beta'


from timeless.square import Square
from timeless.round import Round
from timeless.record import Record
from timeless.tournament import Tournament

import timeless.api


__all__ = [
    "Square",
    "Round",
    "Record",
    "Tournament",
]

#!/usr/bin/env python3
"""Package for running the Yugioh TIMELESS tournament format."""


__version__ = '0.1.1-beta'


from .duelist import Duelist
from .tournament import Tournament

from .timeless import run_yugioh_timeless


__all__ = [
    "Duelist",
    "Tournament",
    "run_yugioh_timeless",
]


if __name__ == '__main__':
    run_yugioh_timeless()

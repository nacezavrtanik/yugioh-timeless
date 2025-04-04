#!/usr/bin/env python3
"""Package for running the Yugioh TIMELESS tournament format."""


__version__ = '0.1.1-beta'


from .timeless import run_yugioh_timeless


__all__ = ['run_yugioh_timeless']


if __name__ == '__main__':
    run_yugioh_timeless()

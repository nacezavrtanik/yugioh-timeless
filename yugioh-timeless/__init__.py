#!/usr/bin/env python3
"""Package for running the Yugioh TIMELESS tournament format."""


__author__ = 'Nace Zavrtanik'
__copyright__ = 'Copyright (C) 2023 Nace Zavrtanik'
__credits__ = []

__license__ = 'GNU AGPLv3'
__version__ = '1.0'
__maintainer__ = 'Nace Zavrtanik'
__email__ = 'yugioh.timeless@gmail.com'


from timeless import run_yugioh_timeless


__all__ = ['run_yugioh_timeless']


if __name__ == '__main__':
    run_yugioh_timeless()


import argparse
from . import __version__


class UpperSectionHelpFormatter(argparse.HelpFormatter):
    def add_usage(self, *args, prefix=None):
        prefix = "USAGE: " if prefix is None else prefix
        super().add_usage(*args, prefix=prefix)

    def start_section(self, heading):
        return super().start_section(heading.upper())


class Parser(argparse.ArgumentParser):
    def __init__(self):
        super().__init__(
            prog="timeless",
            description="Interactively generate pairings for a Yu-Gi-Oh! TIMELESS tournament.",
            formatter_class=UpperSectionHelpFormatter,
        )
        self.version = __version__

        self.add_argument(
            "-v", "--version",
            help="show version number and exit",
            action="version",
            version=self.version,
        )

        registration_group = self.add_argument_group(
            title="registration",
            description="Pass these directly to skip interactive registration.",
            )

        registration_group.add_argument(
            "--variant",
            help="choose deck set",
            type=str,
            choices=["basic", "extra"],
        )

        registration_group.add_argument(
            "--duelists",
            help="enter duelists",
            type=str,
            nargs=4,
            metavar=("DUELIST_1", "DUELIST_2", "DUELIST_3", "DUELIST_4"),
        )

        registration_group.add_argument(
            "--entry-fee",
            help="set entry fee",
            type=int,
        )

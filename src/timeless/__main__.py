
from .parser import Parser
from .cli import CLI


def run_cli():
    parser = Parser()
    args = parser.parse_args()
    cli = CLI(args)


if __name__ == "__main__":
    run_cli()

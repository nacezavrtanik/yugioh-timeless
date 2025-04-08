
from .parser import Parser


def run_cli():
    parser = Parser()
    args = parser.parse_args()
    print(args)


if __name__ == "__main__":
    run_cli()

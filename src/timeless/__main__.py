
from timeless.cli import CLI
from timeless.api import StatefulAPI


def run_cli():
    api = StatefulAPI()
    cli = CLI(api)
    cli.run()


if __name__ == "__main__":
    run_cli()

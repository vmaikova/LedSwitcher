# -*- coding: utf-8 -*-

"""Console script for ledswitcher."""
import sys
import click
from ledswitcher import taskResult

@click.command()
@click.option("--input", default=None, help="input URI (file or URL)")
def main(input=None):
    print(taskResult(input))
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

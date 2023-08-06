import click

from pybooklib import console, pybook


@click.group()
def cli():
    "Request books and data from a specified library"
    pass

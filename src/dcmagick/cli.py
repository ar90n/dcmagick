import click

from .dump import dump
from .find import find

cmd = click.Group()
cmd = click.version_option()(cmd)

cmd.command()(dump)
cmd.command()(find)


def main():
    cmd()

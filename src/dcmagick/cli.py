import click

from .dump import dump
from .find import find

cmd = click.Group()
cmd = click.version_option()(cmd)

cmd.add_command(dump)
cmd.add_command(find)


def main():
    cmd()

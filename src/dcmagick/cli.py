import click

from .dump import dump
from .find import find
from .convert import convert

cmd = click.Group()
cmd = click.version_option()(cmd)

cmd.add_command(dump)
cmd.add_command(find)
cmd.add_command(convert)


def main():
    cmd()

import click

from .dump import dump
from .find import find
from .render import render

cmd = click.Group()
cmd = click.version_option()(cmd)

cmd.add_command(dump)
cmd.add_command(find)
cmd.add_command(render)


def main():
    cmd()

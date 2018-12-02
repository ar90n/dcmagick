import click

from .subcommands import dump

cmd = click.Group()
cmd = click.version_option()(cmd)

cmd.command()(dump)


def main():
    cmd()

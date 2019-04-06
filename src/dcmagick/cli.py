import click

from .convert import convert
from .dump import dump
from .find import find

cmd = click.Group()
cmd = click.version_option()(cmd)

cmd.add_command(dump)
cmd.add_command(find)
cmd.add_command(convert)


def main():
    try:
        cmd()
    except FileNotFoundError as e:
        msg = "{} doesn't exit".format(str(e.filename))
        click.echo(msg, err=True)

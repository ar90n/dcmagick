import json
from enum import Enum
from pathlib import Path

import click
from pydicom import dcmread

from .query import match

@click.command()
@click.option("--name", type=str, help="File name pattern to find dicom file.")
@click.option("--query", type=str, help="Query to find dicom file.")
@click.argument("root", nargs=1)
def find(name, query, root):
    name = name or "*"
    query = query or "{}"
    query_obj = json.loads(query)
    if query_obj is None:
        click.echo("{} is not supported query.".format(query))
        return

    for path in Path(root).glob("**/{}".format(name)):
        if not match(query_obj, path):
            continue
        click.echo(path)
import json
from pathlib import Path

import click

from ..common.query import match
from ..common.context import slice_context


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
        with slice_context(path, None) as  proxy_and_param:
            slice_proxy, proc_params = proxy_and_param
            if match(query_obj, slice_proxy):
                click.echo(path)

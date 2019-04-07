import json
from pathlib import Path

import click

from joblib import Parallel, delayed

from ..common.context import slice_context
from ..common.query import match


@click.command()
@click.option("-p", type=int, default=1, help="Number of process.")
@click.option("--name", type=str, help="File name pattern to find dicom file.")
@click.option("--query", type=str, help="Query to find dicom file.")
@click.argument("root", nargs=1)
def find(p, name, query, root):
    name = name or "*"
    query = query or "{}"
    query_obj = json.loads(query)
    if query_obj is None:
        click.echo("{} is not supported query.".format(query))
        return

    def _find_task(path):
        with slice_context(str(path), None) as slice_proxy:
            if match(query_obj, slice_proxy):
                click.echo(path)

    Parallel(n_jobs=p)(
        [delayed(_find_task)(p) for p in Path(root).glob("**/{}".format(name))]
    )

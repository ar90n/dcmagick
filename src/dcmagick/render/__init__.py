from pathlib import Path

import click

from .slice import render as slice

render = click.Group(name='render')
render.add_command(slice, name='slice')


def main():
    render()

# from .util import read_dcms, slice_location_order


# dcmagick render --wc 500 --ww 244 input.dcm output.png
# dcmagick render --pr gsps0.dcm --pr gsps1.dcm input0.dcm input1.dcm output.png
# dcmagick render --cmap rainbow input.dcm output.png
# dcmagick render --cmap-file ./rainbow.map input.dcm output.png
# dcmagick render --resize 400x400 input.dcm output.png
# dcmagick render --mpr --camera position ./ output.png
# dcmagick render --mip --cameraposition ./ output.png
# dcmagick render --vr --camera position ./ output.png
# dcmagick render --camera position --animation 30 --alignz 200,-220  ./ output.png
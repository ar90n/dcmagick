import json
from enum import Enum
from pathlib import Path

import click
from pydicom import dcmread, datadict
from pydicom.uid import UID
from pydicom.multival import MultiValue


class Format(Enum):
    PRETTY = 'pretty'
    JSON = 'json'

    def __str__(self):
        return self.value


def dump_pretty(dcm):
    return str(dcm)

def repval(self):
    def r(v):
        import numbers
        if isinstance(v, numbers.Real) or isinstance(v, bool):
            return v
        elif isinstance(v, str):
            return v.rstrip('\x00\u0000')
        else:
            return repr(v).rstrip('\x00').replace('\u0000','')


    vvm = datadict.get_entry(self.tag)[1].split('-')

    """Return a str representation of the element's `value`."""
    byte_VRs = ['OB', 'OW', 'OW/OB', 'OW or OB', 'OB or OW',
                'US or SS or OW', 'US or SS']
    if (self.VR in byte_VRs and len(self.value) > self.maxBytesToDisplay):
        repVal = "Array of %d bytes" % len(self.value)
    elif 1 < self.VM:
        repVal = [r(v) for v in self]
    elif len(vvm) == 2 or 1 < int(vvm[0]):
        repVal = [r(self.value)]
    elif isinstance(self.value, UID):
        repVal = self.value.name
    else:
        repVal = r(self.value)  # will tolerate unicode too
    return repVal


def dump_json(dcm):
    def _impl(ds):
        result = {}
        for key in sorted(ds.keys()):
            element = ds[key]
            if element.VR == "SQ":
                tag_value = []
                for dataset in element.value:
                    tag_value.append(_impl(dataset))
            else:
                tag_value = {
                    'vr': element.VR,
                    'description': element.description(),
                    'value': repval(element)
                }
            key = '{:04x},{:04x}'.format(element.tag.group, element.tag.elem)
            result[key] = tag_value

        return result

    return json.dumps(_impl(dcm))


@click.option("--format", type=str, default=Format.PRETTY)
@click.argument("src", nargs=1)
def dump(format, src: str):
    if not Path(src).exists():
        msg = "{} doesn't exit".format(src)
        click.echo(msg, err=True)

    dcm = dcmread(src)
    if format == 'pretty':
        result = dump_pretty(dcm)
    else:
        result = dump_json(dcm)
    click.echo(result)

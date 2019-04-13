import json

from pydicom import datadict, dcmread
from pydicom.multival import MultiValue
from pydicom.uid import UID

from ..common.dicom import create_dataset_of


def dump_value(value):
    def repr_value(value):
        import numbers

        if isinstance(value, numbers.Real) or isinstance(value, bool):
            return value

        if not isinstance(value, str):
            value = repr(value)
        return value.rstrip("\x00\u0000")

    def is_array_value(value):
        """
        Return a str representation of the element's `value`.
        The following codes from pydicom repository.
        """
        byte_VRs = [
            "OB",
            "OW",
            "OW/OB",
            "OW or OB",
            "OB or OW",
            "US or SS or OW",
            "US or SS",
        ]
        return value.VR in byte_VRs and len(value.value) > value.maxBytesToDisplay

    def is_multiple_values(value):
        tag = value.tag
        if not tag.is_private:
            vvm = datadict.get_entry(tag)[1].split("-")
            return len(vvm) == 2 or 1 < int(vvm[0])
        elif hasattr(tag, "private_creator"):
            vvm = datadict.get_private_entry(tag, tag.private_creator)[1].split("-")
            return len(vvm) == 2 or 1 < int(vvm[0])
        else:
            return 1

    if is_array_value(value):
        repVal = "Array of %d bytes" % len(value.value)
    elif is_multiple_values(value):
        repVal = (
            [repr_value(v) for v in value]
            if 1 < value.VM
            else [repr_value(value.value)]
        )
    elif isinstance(value.value, UID):
        repVal = value.value.name
    else:
        repVal = repr_value(value.value)
    return repVal


def dump(proxy):
    def _convert_to_dict(ds):
        converted = {}
        for key in sorted(ds.keys()):
            element = ds[key]
            dumped_key = str(key).strip("()")
            dumped_value = (
                [_convert_to_dict(dataset) for dataset in element.value]
                if element.VR == "SQ"
                else {
                    "vr": element.VR,
                    "description": element.description(),
                    "value": dump_value(element),
                }
            )
            converted[dumped_key] = dumped_value
        return converted

    return json.dumps(_convert_to_dict(create_dataset_of(proxy)))

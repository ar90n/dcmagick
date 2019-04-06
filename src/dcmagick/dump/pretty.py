from ..common.dicom import create_dataset_of

def dump_pretty(proxy):
    ds = create_dataset_of(proxy)
    return str(ds)

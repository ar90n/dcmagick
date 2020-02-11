from ..common.dicom import create_dataset_of


def dump(proxy):
    return str(create_dataset_of(proxy))

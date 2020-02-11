import pydicom


def slice_location_order(dcm):
    return dcm.SliceLocation


def read_dcms(dcm_paths):
    result = {}
    for path in dcm_paths:
        dcm = pydicom.dcmread(path)
        result.setdefault(dcm.StudyInstanceUID, {}).setdefault(
            dcm.SeriesInstanceUID, {}
        )[dcm.SOPInstanceUID] = dcm

    return result

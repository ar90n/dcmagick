from pydicom import dcmread


def match(query, path):
    try:
        dcm = dcmread(str(path))
    except:
        return False
    return True
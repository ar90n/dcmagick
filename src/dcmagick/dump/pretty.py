from pydicom import dcmread

def dump_pretty(src):
    return str(dcmread(src))
import glob
import os
import sys


def hamming_bytes(a: bytes, b: bytes) -> float:
    """
    You can use this function to compare byte arrays (hashes).
    The returned value is a 0->1 match fraction.
    """
    a = int.from_bytes(a, sys.byteorder, signed=False)
    b = int.from_bytes(b, sys.byteorder, signed=False)
    xor = bin(a ^ b)[2:]  # Cut off the 0b prefix.
    return xor.count('1') / len(xor)


def init():
    """
    Load the pHash C++ library.
    By default it looks for the lib file in the parent folder to this file, as this is the "site-packages" folder.
    If that doesn't work, it will try just loading any pHash it can. This is useful for development instances etc.
    :return:
    """
    import cppyy
    cppyy.include('pHash.h')
    import cppyy
    cppyy.include('pHash.h')
    matches = glob.glob(os.path.join(os.path.dirname(__file__), '../pHash.*'))
    if matches:
        cppyy.load_library(matches[0])
    else:
        cppyy.load_library('pHash')

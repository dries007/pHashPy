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
    :return:
    """
    import cppyy
    cppyy.include('pHash.h')
    cppyy.load_library('pHash')

import ctypes
import os

import cppyy.ll


def video_hash(file: str) -> bytes:
    """
    Wraps `ph_dct_videohash`

    "Compute video hash based on the dct of normalized video 32x32x64 cube."

    :param file: path to a file
    :return: hash as a byte array
    """
    if not os.path.isfile(file):
        raise FileNotFoundError(file)
    size = ctypes.c_int(0)
    raw = cppyy.gbl.ph_dct_videohash(file, size)
    if size.value == 0:
        raise RuntimeError("Video could not be loaded: %r" % file)
    try:
        raw = cppyy.ll.cast['uint64_t*'](raw)
        raw.reshape((size.value, ))
        return bytes(raw)
    finally:
        cppyy.ll.free(raw)


def video_hash_dist(a: bytes, b: bytes, threshold=21) -> float:
    """
    Wraps `ph_dct_videohash_dist`

    Returns a "similarity" fraction (0->1) between hashes a and b.
    """
    ptr = ctypes.POINTER(ctypes.c_uint64)
    len_a = (len(a)//8)
    len_b = (len(a)//8)
    a = ctypes.cast((ctypes.c_uint64 * len_a).from_buffer_copy(a), ptr)
    b = ctypes.cast((ctypes.c_uint64 * len_b).from_buffer_copy(b), ptr)
    return cppyy.gbl.ph_dct_videohash_dist(a, len_a, b, len_b, threshold)

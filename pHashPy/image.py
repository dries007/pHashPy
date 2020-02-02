import ctypes
import os

import cppyy.ll


def dct_image_hash(file: str) -> int:
    """
    Wraps `ph_dct_imagehash`

    "Compute dct robust image hash."

    :param file: path to a file
    :return: hash as an int (should be 64 bit)
    """
    if not os.path.isfile(file):
        raise FileNotFoundError(file)
    hash = ctypes.c_uint64(0)
    ret = cppyy.gbl.ph_dct_imagehash(file, hash)
    if ret < 0:
        raise RuntimeError("Image could not be loaded: %r" % file)
    return hash.value


def mh_image_hash(file: str, alpha: float = 2.0, lvl: float = 1) -> bytes:
    """
    Wraps `ph_mh_imagehash`

    "Create MH image hash for filename image."

    :param file: path to a file
    :param alpha: int scale factor for marr wavelet (default=2)
    :param lvl: int level of scale factor (default = 1)
    :return: hash as a byte array
    """
    if not os.path.isfile(file):
        raise FileNotFoundError(file)
    size = ctypes.c_int(0)
    try:
        raw = cppyy.gbl.ph_mh_imagehash(file, size, alpha, lvl)
    except cppyy.gbl.cimg_library.CImgIOException:
        raise RuntimeError("Image could not be loaded: %r" % file)
    try:
        raw = cppyy.ll.cast['uint8_t*'](raw)
        raw.reshape((size.value, ))
        return bytes(raw)
    finally:
        cppyy.ll.free(raw)

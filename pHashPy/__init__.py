"""
    pHash Python bindings

    Copyright (c) Dries007 2020
    Licenced under GLPv3+ (see COPYING file)

    See README.md for more info.

    You should import from this module, or call helpers.init yourself.
"""

from pHashPy.helpers import hamming_bytes, init
from pHashPy.video import video_hash, video_hash_dist
from pHashPy.image import dct_image_hash, mh_image_hash

init()

import argparse
import functools
import multiprocessing
import sys

from pHashPy import video_hash, dct_image_hash, mh_image_hash


functions = {
    "video": video_hash,
    "dct_image": dct_image_hash,
    "mh_image": mh_image_hash,
}

parser = argparse.ArgumentParser()
parser.add_argument("mode", choices=functions.keys())
parser.add_argument("input", nargs="+")
parser.add_argument("-j", default=1, type=int, help="Enable parallel processing with N cores.")


def callback(inp, x):
    if isinstance(x, bytes):
        x = x.hex()
    elif isinstance(x, int):
        x = hex(x)[2:]
    print(x, inp)


def main():
    args = parser.parse_args()
    f = functions[args.mode]
    error = functools.partial(print, file=sys.stderr)

    if args.j == 1 or len(args.input) == 1:
        for inp in args.input:
            callback(inp, f(inp))
    else:
        with multiprocessing.Pool(args.j) as p:
            for inp in args.input:
                cb = functools.partial(callback, inp)
                p.apply_async(f, args=(inp,), callback=cb, error_callback=error)
            p.close()
            p.join()


if __name__ == "__main__":
    main()

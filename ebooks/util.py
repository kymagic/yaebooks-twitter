import hashlib
from functools import partial
import sys

""" Print to stderr """
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

"""
Returns the MD5 hash of the given filename.

Shamelessly stolen from http://stackoverflow.com/questions/7829499/using-hashlib-to-compute-md5-digest-of-a-file-in-python-3/7829658#7829658
"""
def md5sum(filename):
    with open(filename, mode='rb') as f:
        d = hashlib.md5()
        for buf in iter(partial(f.read, 128), b''):
            d.update(buf)
    return d.hexdigest()

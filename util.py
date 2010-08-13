"""
Miscellaneous Util Functions
"""

import sys

def Log(s, stream=sys.stderr, newline=True):
    stream.write(s)
    if newline:
        stream.write("\n")
    return

def unicode_to_ascii(text):
    return ''.join([c for c in text if ord(c) < 128])


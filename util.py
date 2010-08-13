"""
Miscellaneous Util Functions
"""

import sys

def Log(s, stream=sys.stderr, newline=True):
    stream.write(s)
    if newline:
        stream.write("\n")
    return


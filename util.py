"""
Miscellaneous Util Functions
"""

import sys
import unicodedata

def Log(s, stream=sys.stderr, newline=True):
    s = str(s)
    stream.write(s)
    if newline:
        stream.write("\n")
    return

def unicode_to_ascii(text):
    li = []
    for c in text:
        if ord(c) < 128:
            li.append(c)
        else:
            li.append(' ')

    return ''.join(li)


"""
Makes Queries from keywords and their relevances.
"""

import math

def expand_queries_from_keywords(keyword_relevances, count = 3):
    queries = []

    keywords = keyword_relevances[:count]

    queries = [ (' '.join(x), sum(y)) for (x,y) in [ zip(*group) for group in cross_product(keyword_relevances)] ]

    return queries

def cross_product(l):
    return reduce(lambda z, x: z + [y + [x] for y in z], l, [[]])[1:]

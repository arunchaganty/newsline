"""
Makes Queries from keywords and their relevances.
"""

import math

def MakeQueriesFromKeywords(keyword_relevances):
    queries = []
    
    keyword_relevances = [a for (a,b) in keyword_relevances[:3]]
    phrases = keyword_relevances
    #phrases = GenerateAllProperSubsetsInOrder(keyword_relevances)
    #phrases = [" ".join(x) for x in phrases]

    return [('', phrases[0])] + [(a, '') for a in phrases[1:]]

def GenerateAllProperSubsetsInOrder(l):
    return reduce(lambda z, x: z + [y + [x] for y in z], l, [[]])[1:]

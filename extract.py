"""
Extract keywords from news articles.
"""

import count_articles
import util

import calais

import math
import re


analyzer = calais.Calais()

def extract_keywords(article):
    """Extract keywords from an article class. """

    # Title 
    keywords = calais.get_keywords(analyzer.analyze(article.title))
    keywords += calais.get_keywords(analyzer.analyze(article.lead))

    # Keywords
    keywords = list(relevant_lead.union(relevant_title))

    return keywords


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
    content = ' '.join(article.title.tokens + article.lead.tokens)
    keywords = analyzer.get_keywords(content)
    return keywords

def rank_keywords(results, count=5):
    return analyzer.rank_keywords(results, count)


"""
Extract keywords from news articles.
"""

import count_articles
import util

import nltk

import math
import re


__word_distribution = None

def get_word_distribution():
    global __word_distribution
    if __word_distribution == None:
        __word_distribution = nltk.FreqDist(nltk.corpus.reuters.words())
    else :
        return __word_distribution

def extract_keywords(article):
    """Extract keywords from an article class. """

    # Remove stopwords
    relevant_title = [w for w in set(article.title) if w not in nltk.corpus.stopwords.words()]
    relevant_title = [w for w in relevant_title if not re.match("^[^a-zA-Z]+$", w)]
    relevant_lead = [w for w in set(article.lead) if w not in nltk.corpus.stopwords.words()]
    relevant_lead = [w for w in relevant_lead if not re.match("^[^a-zA-Z]+$", w)]

    # Choose special words in i
    # keywords = [w[0] for w in tagged if not w[1].startswith("NNP") and
    #     __word_distribution[w[0]] <= __special_threshold]
    # keywords.sort(key = lambda w: 1/float(__word_distribution[w]))
    # keywords = keywords[0:2]

    # Choose the proper nouns from the lead paragraph 
    # Tag POS (HACK)
    relevant_lead = [ w[0] for w in nltk.pos_tag(relevant_lead) if w[1].startswith("NNP") ]

    # Keywords
    keywords = relevant_lead + relevant_title

    return keywords

def rank_keywords(article, keywords, count_function):
    """Rank keywords in terms of their importance to the article.

       The count function takes a list of pairs [(k, t)]. The first string in
       the pair is a keyword to be searched, and the second is a title
       keyword."""

    # Importance of appearance in lead para/title
    leadFactor = 0.8

    # Calculate TF (modified)
    TF = {}

    lead_fdistribution = nltk.FreqDist(article.title.tokens + article.lead.tokens)
    text_fdistribution = nltk.FreqDist(article.text)

    for word in keywords:
        TF[word] = leadFactor * lead_fdistribution[word] / lead_fdistribution.N() \
            + (1-leadFactor) * text_fdistribution[word] / text_fdistribution.N()

    # Calculate IDF
    IDF = {}

    # Get total documents(D) by searching for 'a' <- really common word
    # Replace with the result of 
    # D = count_fun('a')
    D = 1385541

    article_frequency = count_function([(w, "") for w in keywords])
    for (word, d) in zip(keywords, article_frequency):
        if d > 0:
            IDF[word] = math.log(D/d)
        else:
            IDF[word] = 0   # The keyword is useless anyways

    # Calculate TF-IDF
    score = {}
    for word in keywords:
        score[word] = TF[word]*IDF[word]

    ranked_keywords = score.items()
    ranked_keywords.sort(key = lambda kv: kv[1], reverse=True)
    
    return ranked_keywords

def get_articles(article, ranked_keywords):
    pass


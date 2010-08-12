"""
Extract keywords from news articles
"""

import nltk
import math

#__word_dist = nltk.FreqDist(nltk.corpus.reuters.words())
__special_threshold = 50

class Article:

    def __init__(self, title, lead, text):
        self.title = nltk.Text(nltk.wordpunct_tokenize(title))
        self.lead = nltk.Text(nltk.wordpunct_tokenize(lead))
        self.text = nltk.Text(nltk.wordpunct_tokenize(text))

def extract_keywords(article):
    """Extract keywords from a text """

    # Remove stopwords
    relevant = [w for w in set(article.lead).union(set(article.title)) if w not in nltk.corpus.stopwords.words()]

    # Tag POS (HACK)
    tagged = nltk.pos_tag(relevant)

    # Choose proper nouns
    proper_nouns = [ w[0] for w in tagged if w[1].startswith("NNP") ]

    # Choose special words in i
    # keywords = [w[0] for w in tagged if not w[1].startswith("NNP") and __word_dist[w[0]] <= __special_threshold]
    # keywords.sort(key = lambda w: 1/float(__word_dist[w]))
    # keywords = keywords[0:2]

    # Keywords
    keywords = proper_nouns

    return keywords

def rank_keywords(article, keywords, count_fun):
    """Rank keywords in terms of their importance to the article."""

    # Importance of appearance in lead para/title
    leadFactor = 0.8

    # Calculate TF (modified)
    TF = {}

    lead_fdist = nltk.FreqDist(article.title.tokens + article.lead.tokens)
    text_fdist = nltk.FreqDist(article.text)

    for word in keywords:
        TF[word] = leadFactor * lead_fdist[word] / lead_fdist.N() + (1-leadFactor) * text_fdist[word] / text_fdist.N()

    # Calculate IDF
    IDF = {}

    # Get total documents(D) by searching for 'a' <- really common word
    D = count_fun('a')
    for word in keywords:
        d = count_fun(word) # Execute a search here to get d (no. of doc.) -> log(D/d) 
        print word, d
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


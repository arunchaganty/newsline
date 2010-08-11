"""
Extract keywords from news articles
"""

import nltk

__word_dist = nltk.FreqDist(nltk.corpus.reuters.words())
__special_threshold = 50

def extract(text):
    """Extract keywords from a text """
    text = nltk.Text(nltk.wordpunct_tokenize(text))
   
    # Remove stopwords
    relevant = [w for w in text if w not in nltk.corpus.stopwords.words()]

    # Tag POS
    tagged = set(nltk.pos_tag(relevant))

    # Choose proper nouns
    proper_nouns = [ w[0] for w in tagged if w[1].startswith("NNP") ]

    # Choose special words in i
    # keywords = [w[0] for w in tagged if not w[1].startswith("NNP") and __word_dist[w[0]] <= __special_threshold]
    # keywords.sort(key = lambda w: 1/float(__word_dist[w]))
    # keywords = keywords[0:2]

    # Keywords
    keywords = proper_nouns

def rank_keywords(lead_para, article, keywords):
    """Rank keywords in terms of their importance to the article."""

    # Importance of appearance in lead para
    leadFactor = 0.8

    # Calculate TF (modified)
    TF = {}

    lead_fdist = nltk.FreqDist(lead_para)
    article_fdist = nltk.FreqDist(article)

    for word in keywords:
        TF[word] = leadFactor * lead_fdist[word] / lead_fdist.N() + (1-leadFactor) * article_fdist[word] / article_fdist.N()

    # Calculate IDF

    IDF = {}

    # Get D by searching for 'a' <- really common word
    D = 0
    for word in keywords:
        IDF[word] = 0 # Execute a search here to get d (no. of doc.) -> log(D/d) 


    # Calculate TF-IDF
    score = {}
    for word in keywords:
        score[word] = TF[word]*IDF[word]

    ranked_keywords = score.items()
    ranked_keywords.sort(key = lambda kv: kv[1])

    return rank_keywords


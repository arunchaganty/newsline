#
# NLTK Based keyword extractor
#

import count_articles_threaded
import nltk

import math
import re

from Extractor import Extractor

class NLTKExtractor(Extractor):

    def get_keywords(self, article, k=5):
        """Extract keywords from an article class. 
           Return keywords and their TFs (for the article)"""

        # Remove stopwords
        relevant_title = [w for w in set(article.title) if w not in nltk.corpus.stopwords.words()]
        relevant_title = [w for w in relevant_title if not re.match("^[^a-zA-Z]+$", w)]
        relevant_lead = [w for w in set(article.lead) if w not in nltk.corpus.stopwords.words()]
        relevant_lead = [w for w in relevant_lead if not re.match("^[^a-zA-Z]+$", w)]
    
        # Choose the proper nouns from the lead paragraph 
        # Tag POS (HACK)
        relevant_lead = [w[0] for w in nltk.pos_tag(relevant_lead) if w[1].startswith("NNP") ]
    
        text = set(article.text)
    
        # Make sure that the words we use are actually present in the article.
        relevant_title = set(relevant_title).intersection(text)
        relevant_lead = set(relevant_lead).intersection(text)
    
        # Keywords
        keywords = list(relevant_lead.union(relevant_title))

        # Get TF scores
        leadFactor = 0.8
        lead_fdist = nltk.FreqDist(article.title.tokens + article.lead.tokens)
        text_fdist = nltk.FreqDist(article.text)

        tf_func = lambda word: leadFactor * lead_fdist[word] / lead_fdist.N() \
                + (1-leadFactor) * text_fdist[word] / text_fdist.N()

        keywords = [ (word, tf_func(word)) for word in keywords ]

        return keywords

    def rank_keywords(self, keywords):
        """Rank keywords in terms of their importance to the article."""
    
        # Calculate IDF
    
        # Get total documents(D) by searching for 'a' <- really common word
        # Replace with the result of 
        # D = count_fun('a')
        D = 1385541
    
        article_frequency = count_articles_threaded.count_articles([(w[0], "") for w in keywords])

        ranked_keywords = [ (word[0], word[1]*math.log(D/d)) for word,d in zip(keywords, article_frequency) ]
        ranked_keywords.sort(key = lambda kv: kv[1], reverse=True)
        
        return ranked_keywords


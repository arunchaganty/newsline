"""
Definition of the Article Class
"""
import nltk

import util

class Article:
    def __init__(self, title, lead, text):
        title, lead, text = [util.unicode_to_ascii(x) for x in [title, lead, text]]
        # lead, text = [x.lower() for x in [lead, text]]

        self.title = nltk.Text(nltk.wordpunct_tokenize(title))
        self.lead = nltk.Text(nltk.wordpunct_tokenize(lead))
        self.text = nltk.Text(nltk.wordpunct_tokenize(text))
        return

def read_article_from_file(filename):
    """ Read an article from a file. """
    s = open(filename).read()
    title, lead, text = s.split("\n\n", 2)
    return Article(title, lead, text)



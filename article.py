"""
Definition of the Article Class
"""
import nltk

class Article:
    def __init__(self, title, lead, text):
        self.title = nltk.Text(nltk.wordpunct_tokenize(title))
        self.lead = nltk.Text(nltk.wordpunct_tokenize(lead))
        self.text = nltk.Text(nltk.wordpunct_tokenize(text))
        return

def read_article_from_file(filename):
    """ Read an article from a file. """
    str = open(filename).read()
    title, lead, text = str.split("\n\n", 2)
    return Article(title, lead, text)



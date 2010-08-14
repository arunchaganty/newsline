"""
Definition of the Article Class
"""
import util

import lxml.html
import nltk

import urllib

class Article:
    def __init__(self, title, lead, text):
        title, lead, text = [util.unicode_to_ascii(x) for x in [title, lead, text]]
        # lead, text = [x.lower() for x in [lead, text]]

        self.title = nltk.Text(nltk.wordpunct_tokenize(title))
        self.lead = nltk.Text(nltk.wordpunct_tokenize(lead))
        self.text = nltk.Text(nltk.wordpunct_tokenize(text))
        return

def get_article_from_uri(uri):
    """ Read an article from a file. """
    return urllib.urlopen(uri).read()


def parse(a, is_html):
    if is_html:
        return parse_html(a)
    else:
        return parse_text(a)

def parse_text(a):
    title, lead, text = a.split("\n\n", 2)
    return Article(title, lead, text)

def parse_html(a):
    soup = lxml.html.document_fromstring(a)
    title = soup.find_class('articleHeadline')[0].text_content()

    body = soup.find_class('articleBody')
    lead = body[0].text_content()
    text = body[1].text_content()
    return Article(title, lead, text)



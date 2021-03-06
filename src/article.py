"""
Definition of the Article Class
"""
import util

import lxml.html

import urllib

class Article:
    def __init__(self, title, lead, text):
        title, lead, text = [util.unicode_to_ascii(x) for x in [title, lead, text]]
        # lead, text = [x.lower() for x in [lead, text]]

        self.title = title
        self.lead = lead
        self.text = text
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
    title = ""

    try:
        title = soup.find_class('articleHeadline')[0].text_content()
    except IndexError:
        title = soup.xpath('//head/title')[0].text_content()
   
    body = soup.find_class('articleBody')
    if body == []:
        try:
            body = soup.get_element_by_id('articleBody')
        except KeyError, e:
            body = ""

    try:
        lead = body[0].text_content()
        text = body[1].text_content()
    except IndexError, e:
        # No separate lead and text
        all_text = body[0].text_content().strip()
        lead, text = all_text.split("\n", 1)
        
    return Article(title, lead, text)



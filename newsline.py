#
# NewsLine Algorithm
#

import article
import count_articles
import extract
import util

import sys

def NewsLine(filename):
    a = article.read_article_from_file(filename)
    util.Log("Finished Reading Article.")
    k = extract.extract_keywords(a)
    util.Log("Finished Extracting Keywords.")
    ranked_keywords = extract.rank_keywords(a, k, 
        count_articles.count_articles)

    print ranked_keywords

    return

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage %s <article>"%(sys.argv[0])

    s = sys.argv[1]
    NewsLine(s)


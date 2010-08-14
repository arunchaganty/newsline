#
# NewsLine Algorithm
#

import article
import count_articles_threaded
import get_articles_threaded
import make_queries
import newsitem
import select_articles
import util

import sys
import pdb

import calais_extractor
import nltk_extractor

extractor = calais_extractor.CalaisExtractor()
#extractor = nltk_extractor.NLTKExtractor()

def NewsLine(uri, is_html=True, print_results=False):
    a = article.get_article_from_uri(uri)
    a = article.parse(a, is_html)

    return GetTimeLine(a, print_results)

def GetTimeLine(a, print_results=False):
    k = extractor.get_keywords(a)
    util.Log("Finished Extracting Keywords.")

    ranked_keywords = extractor.rank_keywords(k) 
    util.Log(ranked_keywords)

    # Expand based on subset matches of keywords
    ranked_keywords = make_queries.expand_queries_from_keywords(ranked_keywords, 4)
    ranked_keywords.sort(key=lambda x: x[1], reverse=True)
    ranked_keywords = ranked_keywords[:min(5,len(ranked_keywords))]

    articles = get_articles_threaded.get_articles([w for (w,r) in ranked_keywords])
    articles = [[newsitem.NewsItem(a) for a in group] for group in articles]

    #articles = select_best_articles.select_relevant_articles(articles, ranked_keywords)
    #articles = select_articles.select_all_articles(articles, ranked_keywords)
    articles = select_articles.select_temporal_starting_articles(articles, ranked_keywords)

    articles.sort(reverse=True)

    if print_results:
      for a in articles: print a

    return articles


def Main():
    usage = "Usage: %s [-h] <article uri>"%(sys.argv[0])
    html_flag = "-h"

    uri_is_html = False

    if len(sys.argv) < 2:
        print usage
        sys.exit(1)

    if len(sys.argv) == 2:
        if sys.argv[1] != html_flag:
            uri = sys.argv[1]
        else:
            print "No uri found."
            print usage
            sys.exit(1)
    if len(sys.argv) == 3:
        if sys.argv[1] == html_flag and sys.argv[2] != html_flag:
            uri = sys.argv[2]
            uri_is_html = True
        else:
            print "Incorrect Arguments. Maybe wrong order?"
            print usage
            sys.exit(1)

    NewsLine(uri, is_html=uri_is_html, print_results=True)
    return

if __name__ == '__main__':
    Main()

#
# NewsLine Algorithm
#

import article
import extract
import nytimes
import util

def NewsLine(filename):
    a = article.read_article_from_file(filename)
    util.Log("Finished Reading Article.")
    k = extract.extract_keywords(a)
    util.Log("Finished Extracting Keywords.")
    ranked_keywords = extract.rank_keywords(a, k, 
        nytimes.count_articles_for_keyword)

    print ranked_keywords

    return

if __name__ == '__main__':
    NewsLine("data/chernobyl-russian-fires-2010-08-11.txt")

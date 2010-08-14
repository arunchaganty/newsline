import random
import newsitem

import pdb

def select_relevant_articles(articles, ranked_keywords):
    # Sort each of the set of articles by date
    for x in articles:
        x.sort(reverse=True)

    relevances = [b for (a, b) in ranked_keywords]
    probabilites = [x/sum(relevances) for x in relevances] + [0.2] * 10

    final_articles = set()

    for i in range(len(articles)):
        for y in articles[i]:
            final_articles.add(y)
            if random.uniform(0, 1) > probabilites[i]:
                break

    return list(final_articles)

def select_all_articles(articles, ranked_keywords):
    s = set()
    for kw, group in zip(ranked_keywords,articles):
        print kw
        for a in group:
            print a
            s.add(a)
    return list(s)

def select_temporal_starting_articles(article_set, ranked_keywords):
    
    # Assign scores + Remove duplicates
    d = {}
    for articles, (kw,relevance) in zip(article_set,ranked_keywords):
        for article in articles:
            if not d.has_key(article):
                d[article] = relevance
    articles = d.items()

    # bin by time
    groups = bin_by_time(articles, lambda x: x[0].date)

    # choose most relevant article in each bin
    articles = [ max(group, key=lambda x: x[1]) for group in groups ]

    return articles

def bin_by_time(collection, key_func = lambda x: x, duration=7):
    """Group articles based on duration"""
    groups = []

    baseline = collection[0]
    group = []
    for item in collection:
        if (key_func(item) - key_func(baseline)).days <= duration:
            group.append(item)
        else:
            baseline = item
            groups.append(group)
            group = [item]

    if len(group) > 0: groups.append(group)

    return groups


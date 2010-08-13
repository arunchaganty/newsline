import yql

""" Contains the NYTimes class that searches the New York Times. 
    Example Usage:
      import nytimes
      n = nytimes.NYTimes()
      
      nytimes.get_total_number_of_articles(n.get_counts("elections", "obama"))

      n.get_results("elections", "obama").data()
"""

class NYTimes:

    def __init__(self, limit=10):
        self.__limit = limit
        self.__query_default = "select * from nyt.article.search(%d) where "%(self.__limit)
        return

    def get_query_string(self, query, title=""):
        """ Returns the query string given the query (query), and the string to
        be searched for in the title (title)."""

        title = title.strip()
        query = query.strip()

        if title != "":
            return "title:'%s' %s"%(title, query)
        else:
            return query

    def get_yql_query(self, search_in_body, search_in_title="", args={}):
        """ Returns the YQL query given the string to be searched. Also takes
            optional arguments to search in the title (and other arguments that
            NYTimes supports - see the comment on get_results. 

            The returned string must work with YQL Query. Here are a couple of
            examples of the kind of queries that we want to construct:

            select * from nyt.article.search(200) where 
            query="title:chernobyl nuclear" and rank="oldest"
            
            select * from nyt.article.search(200) where query="per_facet:[CHERNOBYL]" 
            and rank="oldest" and facets="publication_month" """

        yql_query = self.__query_default
        yql_query += """ query="%s" """%(self.get_query_string(search_in_body, search_in_title))

        for k in args:
            yql_query += """ and %s="%s" """%(k, args[k])
        return yql_query

    def execute(self, yql_query):
        y = yql.YQL()
        return y.get_results(yql_query)

    def get_results(self, search_in_body, search_in_title="", **args):
        """ Gets the results given the string to search for in the body. It takes
            an optional argument to search for a string in the title. It also
            takes optional named arguments (**args) that the NYTimes data model supports:
            http://developer.nytimes.com/docs/article_search_api/#h3-data-fields """

        yql_query = self.get_yql_query(search_in_body, search_in_title, args)
        return self.execute(yql_query)
 
    def get_counts(self, search_in_body, search_in_title="", **args):
        """ Gets a result containing the counts of matching articles across years.

            The total number of articles can be obtained by passing the result to
            get_total_number_of_articles function. """

        yql_query = self.get_yql_query(search_in_body, search_in_title, 
            args) + """ and facets="publication_year" """
        return self.execute(yql_query)


def get_total_number_of_articles(yql_result):
    """ Takes a YQLResult class obtained from a NYTimes Count, and returns the
    total number of articles."""
    try:
        publication_year = yql_result.results()['facets']['publication_year']
    except KeyError, e:
        return 0
    except StandardError, e:
        return 0
    
    try:
        return sum([int(x['count']) for x in publication_year])
    except TypeError:
        try:
            return int(publication_year['count'])
        except StandardError:
            return 0
    except StandardError:
        return 0


def count_articles_for_keyword(keyword, title_keyword=""):
    """ A helper function for the keyword ranker.  It simply takes a keyword (a
        string), and a keyword in the title (title_keyword), and returns the
        number of articles with it. """

    n = NYTimes()
    return get_total_number_of_articles(n.get_counts(keyword, title_keyword))

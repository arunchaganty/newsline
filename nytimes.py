import yql

# http://developer.nytimes.com/docs/article_search_api/#h3-data-fields
# x = a.query('select * from nyt.article.search(200) where query="title:chernobyl nuclear" and rank="oldest"')
# x = a.query('select * from nyt.article.search(200) where query="per_facet:[CHERNOBYL]" and rank="oldest" and facets="publication_month"')
 

class NYTimes:

    def __init__(self, limit=200):
        self.__limit = limit
        self.__query_default = "select * from nyt.article.search(%d) where "%(self.__limit)
        return

    def get_query_string(self, query, title=""):
        title = title.strip()
        query = query.strip()

        if title != "":
            return "title:'%s' %s"%(title, query)
        else:
            return query

    def get_yql_query(self, query, title="", args={}):
        yql_query = self.__query_default
        yql_query += """ query="%s" """%(self.get_query_string(query, title))

        for k in args:
            yql_query += """ and %s="%s" """%(k, args[k])
        return yql_query

    def get_results(self, query, title="", **args):
        yql_query = self.get_yql_query(query, title, args)
        return self.execute(yql_query)
 
    def get_counts(self, query, title="", **args):
        yql_query = self.get_yql_query(query, title, args) + """ and facets="publication_year" """
        return self.execute(yql_query)

    def execute(self, yql_query):
        y = yql.YQL()
        return y.get_results(yql_query)

        
  
  


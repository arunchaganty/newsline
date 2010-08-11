#
# Wrapper over YQL
#

from urllib import urlencode, quote_plus
import urllib2
from json import loads

import os

def init_proxy():
    # Get proxies from environment
    proxies = {}
    if os.environ.has_key("http_proxy"):
        proxies["http"] = os.environ["http_proxy"]
    if os.environ.has_key("https_proxy"):
        proxies["https"] = os.environ["https_proxy"]
    if os.environ.has_key("ftp_proxy"):
        proxies["ftp"] = os.environ["ftp_proxy"]

    # Set proxy handler
    proxy = urllib2.ProxyHandler(proxies)
    opener = urllib2.build_opener(proxy)
    urllib2.install_opener(opener)

class YQLResult:
    __jsonData = None

    def __init__(self, data):
        self.__jsonData = loads(data)["query"]

    def count(self):
        return self.__jsonData["count"]

    def lang(self):
        return self.__jsonData["lang"]

    def results(self):
        return self.__jsonData["results"]["result"]


class YQL:
    __uri = "https://query.yahooapis.com/v1/public/yql"
    __format = "json"
    __limit = "1000"

    def __init__(self):
        pass

    def get_uri(self, query):
        uri = self.__uri + "?" + urlencode({"q":query, "format":self.__format})
        return uri

    def query(self, query):
        url = self.get_uri(query)

        stream = urllib2.urlopen(url)
        data = stream.read()
        stream.close()

        result = YQLResult(data)

        return result


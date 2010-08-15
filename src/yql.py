# A Wrapper over YQL's HTTP API
# Arun, Pranesh, Sujeet, Vikram

import json
import os
import urllib
import urllib2

import signal
signal_ = signal.signal
signal.signal = lambda *args: None
import pycurl, curl
signal.signal = signal_


def init_proxy_in_urllib():
    """ Sets the environment proxies in urllib. """
    proxies = {}
    if os.environ.has_key("http_proxy"):
        proxies["http"] = os.environ["http_proxy"]
    if os.environ.has_key("https_proxy"):
        proxies["https"] = os.environ["https_proxy"]
    if os.environ.has_key("ftp_proxy"):
        proxies["ftp"] = os.environ["ftp_proxy"]
    if os.environ.has_key("socks_proxy"):
        proxies["socks"] = os.environ["socks_proxy"]

    # Set proxy handler
    proxy = urllib2.ProxyHandler(proxies)
    opener = urllib2.build_opener(proxy)
    urllib2.install_opener(opener)
    return


class YQL:
    __uri = "http://query.yahooapis.com/v1/public/yql"
    __format = "json"
    __limit = "1000"
    __env = 'store://datatables.org/alltableswithkeys'
    __curl = None

    def __init__(self):
        self.__curl = curl.Curl()
        if os.environ.has_key("socks_proxy"):
            self.__curl.set_option(pycurl.PROXY, os.environ["socks_proxy"])
            self.__curl.set_option(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5)
        self.__curl.set_option(pycurl.NOSIGNAL,1)
        return

    def get_uri(self, query, opt_params = {}):
        params = {"q": query
                 ,"format": self.__format
                 ,"env" : self.__env}

        params.update(opt_params)

        uri = self.__uri + "?" + urllib.urlencode(params)
        return uri

    def get_results(self, query, opt_params={}):
        url = self.get_uri(query, opt_params)

        data = self.__curl.get(url)

        return YQLResult(data)


class YQLResult:
    __jsonData = None

    def __init__(self, data):
        self.__jsonData = json.loads(data)["query"]

    def count(self):
        return self.__jsonData["count"]
    
    def data(self):
        return self.__jsonData

    def lang(self):
        return self.__jsonData["lang"]

    def results(self):
        return self.__jsonData["results"]


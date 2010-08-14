# Wrapper for OpenCalais
#

import urllib, urllib2
import pycurl, curl
import json
import re
import os

import pdb

from Extractor import Extractor

API_KEY="hsrw7wujsw9q5mwjujhtmfdk"
CALAIS_URL="http://api.opencalais.com/enlighten/calais.asmx/Enlighten"

class Calais(Extractor):
    __curl = None
    __params = """<c:params xmlns:c="http://s.opencalais.com/1/pred/"
            xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
        <c:processingDirectives
            c:contentType="text/raw"
            c:outputFormat="application/json">
        </c:processingDirectives>
        <c:userDirectives />
        <c:externalMetadata />
    </c:params>"""
    __pat = re.compile("<string[^>]*>(.*)</string>")

    def __init__(self):
       # Init Curl
        self.__curl = curl.Curl()
        if os.environ.has_key("socks_proxy"):
            self.__curl.set_option(pycurl.PROXY, os.environ["socks_proxy"])
            self.__curl.set_option(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5)
        self.__curl.set_option(pycurl.HTTPHEADER,["SOAPAction"])

    def analyze(self, content):

        post_data = {}
        post_data["licenseId"] = API_KEY
        post_data["paramsXML"] = self.__params
        post_data["content"] = content

        s = self.__curl.post(CALAIS_URL, post_data)
        print s
        result = self.__pat.findall(s)[0]

        return json.loads(result)
    
    def get_keywords(self, article):
        content = ' '.join(article.title.tokens + article.lead.tokens)

        results = self.analyze(content)
        # We are only interested in entities
        results = [ r for r in results.values() if r.has_key("_typeGroup") and r["_typeGroup"] == "entities" ]

        return results

    def rank_keywords(self, results, k=5):
        k = min(k, len(results))
        # Get top k most relevant keywords
        results.sort(key = lambda x: x['relevance'], reverse = True)
        results = results[:k]
        results = [ (x['name'], x['relevance']) for x in results ]

        return results 

def demo():
    c = Calais()
    content = """ China to Build State-Run Search Engine 
            SHANGHAI - In an apparent bid to extend its control over the
            Internet and cash in on the rapid growth of mobile devices,
            China plans to create its own government-controlled search
            engine."""
    return c.analyze(content)



# Wrapper for OpenCalais
#

import urllib, urllib2
import pycurl, curl
import json
import re

API_KEY="hsrw7wujsw9q5mwjujhtmfdk"
CALAIS_URL="http://api.opencalais.com/enlighten/calais.asmx/Enlighten"

class Calais:
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
        self.__curl.set_option(pycurl.PROXY, "10.6.18.143:1080")
        self.__curl.set_option(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5)
        self.__curl.set_option(pycurl.HTTPHEADER,["SOAPAction"])

    def analyze(self, content):
        post_data = {}
        post_data["licenseId"] = API_KEY
        post_data["paramsXML"] = self.__params
        post_data["content"] = content

        s = self.__curl.post(CALAIS_URL, post_data)
        result = self.__pat.findall(s)[0]

        return json.loads(result)
    
    def get_keywords(self, results, k=5):
        # We are only interested in entities
        results = [ r for r in results if r.has_key("_typeGroup") and r["_typeGroup"] == "entities" ]

        # Get top k most relevant keywords
        results = results.sort(key = lambda x: x['relevance'], reverse = True)[:k]
        results = [ (x['name'], x['relevance']) for x in results ]

        return results


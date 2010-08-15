# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from json import dumps as json_dumps 

from server import settings

from server.newsline import newsline

def render_to_response(request, filename, ctx={}):
    context =  RequestContext (request,
            {'user':request.user,
            'SITE_URL':settings.SITE_URL,
            'MEDIA_URL':settings.MEDIA_URL,
            })
    return render_to_response_(filename, ctx, context)

def api(request):
    reply = {}
    if request.GET:
        try:
            if not request.GET.has_key("url"):
                raise ArgumentException("POST argument 'url' required")

            url = request.GET["url"]
            if not newsline.CheckUri(url):
                raise ArgumentException("'url' not from recognized news site")

            data = newsline.NewsLine(url, is_html=True)
            # json understands dicts
            reply["data"] = map(lambda x: x.toDict(), data)
        except StandardError as e:
            reply["error"] = e.message
    else:
        reply["pong"] = ""

    data = json_dumps(reply)
    print data

    # Wrap response in a function callback (jsonp)
    if request.GET and request.GET.has_key("callback"):
        data = "%s(%s)"%(request.GET["callback"],data)

    response = HttpResponse(data, mimetype="application/json")

    return response


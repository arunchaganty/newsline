# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from json import dumps as json_dumps 

from server import settings

#from server import newsline

def render_to_response(request, filename, ctx={}):
    context =  RequestContext (request,
            {'user':request.user,
            'SITE_URL':settings.SITE_URL,
            'MEDIA_URL':settings.MEDIA_URL,
            })
    return render_to_response_(filename, ctx, context)

def api(request):
    reply = {}
    if request.POST:
        if not request.POST.has_key("url"):
            reply["error"] = "POST argument 'url' required"
        else:
            url = request.POST["url"]
            #if not newsline.check_supports(url):
            #    reply["error"] = "'url' not from recognized news site"
            #else:
            #    #data = newsline.get_causal_articles(request)
            #    reply["data"] = data
            reply["data"] = url
    else:
        reply["error"] = "POST argument 'url' required"

    print json_dumps(reply)
    response = HttpResponse(json_dumps(reply), mimetype="application/json")

    return response


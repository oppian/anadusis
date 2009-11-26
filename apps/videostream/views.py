from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from models import *

def latest(request, template_name="videostream/latest.html"):
    videos = VideoStream.objects.filter(is_public=True)
    return render_to_response(template_name, {
        "latest": videos,
    }, context_instance=RequestContext(request))
    
def owned(request, template_name="videostream/owned.html"):
    videos = VideoStream.objects.filter(author=request.user)
    return render_to_response(template_name, {
        "latest": videos,
    }, context_instance=RequestContext(request))
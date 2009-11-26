from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from models import *

from friends import models as friends

def latest(request, template_name="videostream/latest.html"):
    videos = VideoStream.objects.filter(is_public=True)
    return render_to_response(template_name, {
        "latest": videos,
    }, context_instance=RequestContext(request))
    
def yourvideos(request, template_name="videostream/yourvideos.html"):
    videos = VideoStream.objects.filter(author=request.user)
    return render_to_response(template_name, {
        "latest": videos,
    }, context_instance=RequestContext(request))
    
def friendsvideo(request, template_name="videostream/friends.html"):
    print request.user
    friendships = friends.Friendship.objects.friends_for_user(request.user)
    friend_list = []
    for friendship in friendships:
        print friendship
        friend_list.append(friendship['friend'])
        
    videos = VideoStream.objects.filter(is_public=True, author__in=friend_list).exclude(author=request.user)
    return render_to_response(template_name, {
        "latest": videos,
    }, context_instance=RequestContext(request))
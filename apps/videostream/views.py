from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect, get_host
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext, RequestContext
from django.utils.translation import ugettext_lazy as _
from forms import *
from friends import models as friends
from models import *

@login_required
def upload(request, form_class=VideoUploadForm,
        template_name="videostream/upload.html", group_slug=None, bridge=None):
    """
    upload form for videos
    """

    if bridge:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404
    else:
        group = None

    video_form = form_class()
    if request.method == 'POST':
        if request.POST.get("action") == "upload":
            video_form = form_class(request.user, request.POST, request.FILES)
            if video_form.is_valid():
                video = video_form.save(commit=False)
                video.author = request.user
                video.encode = True
                video.save()

                # in group context we create a Pool object for it
                if group:
                    pool = Pool()
                    pool.video = video
                    group.associate(pool)
                    pool.save()

                request.user.message_set.create(message=_("Successfully uploaded video '%s'") % video.title)

                return redirect(video)

    return render_to_response(template_name, {
        "group": group,
        "video_form": video_form,
    }, context_instance=RequestContext(request))

@login_required
def yourvideos(request, template_name="videostream/yourvideos.html", group_slug=None, bridge=None):
    """
    videos for the currently authenticated user
    """
    
    if bridge:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404
    else:
        group = None
    
    videos = VideoStream.objects.filter(author=request.user)
    
    if group:
        videos = group.content_objects(videos)
    
    videos = videos.order_by("-date_added")
    
    return render_to_response(template_name, {
        "group": group,
        "videos": videos,
    }, context_instance=RequestContext(request))

@login_required
def videos(request, template_name="videostream/latest.html", group_slug=None, bridge=None):
    """
    latest videos
    """
    
    if bridge:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404
    else:
        group = None
    
    videos = VideoStream.objects.filter(
        Q(is_public=True) |
        Q(is_public=False, author=request.user)
    )
    
    for v in videos:
        print v
    
    if group:
        videos = group.content_objects(videos)
    
    videos = videos.order_by("-date_added")
    
    return render_to_response(template_name, {
        "group": group,
        "videos": videos,
    }, context_instance=RequestContext(request))

@login_required
def details(request, slug, template_name="videostream/details.html", group_slug=None, bridge=None):
    """
    show the video details
    """
    
    if bridge:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404
    else:
        group = None
    
    videos = VideoStream.objects.all()
    
    if group:
        videos = group.content_objects(videos)
    
    video = get_object_or_404(videos, slug=slug)
    
    # check if public or owned by self
    if not video.is_public and request.user != video.author:
        raise Http404
    
    if video.author == request.user:
        is_me = True
    else:
        is_me = False
        
    if video.flvfile:
        video.increment_count()
    
    return render_to_response(template_name, {
        "group": group,
        "video": video,
        "is_me": is_me,
    }, context_instance=RequestContext(request))
    
@login_required
def membervideos(request, username, template_name="videostream/membervideos.html", group_slug=None, bridge=None):
    """
    Get the members videos and display them
    """
    
    if bridge:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404
    else:
        group = None
    
    user = get_object_or_404(User, username=username)
    
    videos = VideoStream.objects.filter(
        author__username = username,
        is_public = True,
    )
    
    if group:
        videos = group.content_objects(videos)
    
    videos = videos.order_by("-date_added")
    
    return render_to_response(template_name, {
        "group": group,
        "videos": videos,
    }, context_instance=RequestContext(request))
    
@login_required
def edit(request, slug, form_class=VideoEditForm,
        template_name="videostream/edit.html", group_slug=None, bridge=None):
    
    if bridge:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404
    else:
        group = None
    
    videos = VideoStream.objects.all()
    
    if group:
        videos = group.content_objects(videos)
    
    video = get_object_or_404(videos, slug=slug)

    if request.method == "POST":
        if video.author != request.user:
            request.user.message_set.create(message="You can't edit videos that aren't yours")
            
            include_kwargs = {"slug": video.slug}
            if group:
                redirect_to = bridge.reverse("video_details", group, kwargs=include_kwargs)
            else:
                redirect_to = reverse("video_details", kwargs=include_kwargs)
            
            return HttpResponseRedirect(redirect_to)
        
        if request.POST["action"] == "update":
            video_form = form_class(request.user, request.POST, instance=video)
            if video_form.is_valid():
                videoobj = video_form.save(commit=False)
                videoobj.save()
                
                request.user.message_set.create(message=_("Successfully updated video '%s'") % video.title)
                
                include_kwargs = {"slug": video.slug}
                if group:
                    redirect_to = bridge.reverse("video_details", group, kwargs=include_kwargs)
                else:
                    redirect_to = reverse("video_details", kwargs=include_kwargs)
                
                return HttpResponseRedirect(redirect_to)
        else:
            video_form = form_class(instance=video)

    else:
        video_form = form_class(instance=video)

    return render_to_response(template_name, {
        "group": group,
        "video_form": video_form,
        "video": video,
    }, context_instance=RequestContext(request))
    
@login_required
def destroy(request, id, group_slug=None, bridge=None):
    
    if bridge:
        try:
            group = bridge.get_group(group_slug)
        except ObjectDoesNotExist:
            raise Http404
    else:
        group = None
    
    videos = VideoStream.objects.all()
    
    if group:
        videos = group.content_objects(videos)
    
    video = get_object_or_404(videos, id=id)
    title = video.title
    
    if group:
        redirect_to = bridge.reverse("videos_yours", group)
    else:
        redirect_to = reverse("videos_yours")
    
    if video.author != request.user:
        request.user.message_set.create(message="You can't delete videos that aren't yours")
        return HttpResponseRedirect(redirect_to)

    if request.method == "POST" and request.POST["action"] == "delete":
        video.delete()
        request.user.message_set.create(message=_("Successfully deleted video '%s'") % title)
    
    return HttpResponseRedirect(redirect_to)

@login_required
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

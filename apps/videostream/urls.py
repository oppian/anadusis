# -*- coding: utf-8 -*-

# © Copyright 2009 Andre Engelbrecht. All Rights Reserved.
# This script is licensed under the BSD Open Source Licence
# Please see the text file LICENCE for more information
# If this script is distributed, it must be accompanied by the Licence

from django.conf.urls.defaults import *
from videostream.models import VideoStream
from videostream.feeds import LatestStream
from views import *


feeds = {
    'latest':  LatestStream,        
}

urlpatterns = patterns('',
    # all videos or latest videos
    url(r'^$', videos, name='videos'),
    # a video details
    url(r'^details/(?P<slug>.*)/$', details, name="video_details"),
    # upload videos
    url(r'^upload/$', upload, name="videos_upload"),
    # your videos
    url(r'^yourvideos/$', yourvideos, name='videos_yours'),
    # a members videos
    url(r'^member/(?P<username>[\w]+)/$', membervideos, name='videos_member'),
    # destory video
    url(r'^destroy/(?P<id>\d+)/$', destroy, name='video_destroy'),
    # edit video
    url(r'^edit/(?P<slug>.*)/$', edit, name='video_edit'),
    # friends videos
    url(r'^friends/$', friendsvideo, name='videos_friends'),
    
)


urlpatterns += patterns('django.contrib.syndication.views',
        (r'^feeds/(?P<url>.*)/$', 'feed', {'feed_dict': feeds}),
)

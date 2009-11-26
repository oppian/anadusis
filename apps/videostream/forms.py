from django import forms
from datetime import datetime
from django.utils.translation import ugettext_lazy as _

from models import VideoStream

class VideoUploadForm(forms.ModelForm):
    
    class Meta:
        model = VideoStream
        exclude = ('author', 'slug', 'featured', 'flvfile', 'thumbnail', 'encode')


    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(VideoUploadForm, self).__init__(*args, **kwargs)

class VideoEditForm(forms.ModelForm):
    
    class Meta:
        model = VideoStream
        exclude = ('author', 'slug', 'featured', 'flvfile', 'thumbnail', 'encode', 'videoupload')
        
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(VideoEditForm, self).__init__(*args, **kwargs)

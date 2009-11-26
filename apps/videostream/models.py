from django.conf import settings
from django.contrib.auth import models as auth
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import AutoSlugField
import datetime


# use Django-tagging for tags. If Django-tagging cannot be found, create our own
# I did not author this little snippet, I found it somewhere on the web,
# and cannot remember where exactly it was.
try:
    from tagging.fields import TagField
    tagfield_help_text = 'Separate tags with spaces, put quotes around multiple-word tags.'
except ImportError:
    class TagField(models.CharField):
        def __init__(self, **kwargs):
            default_kwargs = {'max_length': 255, 'blank': True}
            default_kwargs.update(kwargs)
            super(TagField, self).__init__(**default_kwargs)
        def get_internal_type(self):
            return 'CharField'
    tagfield_help_text = 'Django-tagging was not found, tags will be treated as plain text.'
# End tagging snippet

class VideoStream(models.Model):
    """ Our standard VideoStream class
    """
    title = models.CharField( max_length=255, help_text="A nice title for the video clip" )
    slug = AutoSlugField(populate_from='title')
    description = models.TextField( null=True, blank=True, 
            help_text="A short caption about the video")
    
    # Publication details
    is_public = models.BooleanField( default=False, help_text=_('Public videos will be displayed in the default views.'))
    date_added = models.DateTimeField(_('date added'), default=datetime.datetime.now, editable=False)
    featured = models.BooleanField( default=False )
    tags = TagField( help_text=tagfield_help_text )
    enable_comments = models.BooleanField( default=False )
    author = models.ForeignKey(auth.User, related_name="added_videos")

    # Video File field
    videoupload = models.FileField( upload_to="videos/source/", null=True, blank=True,
            help_text="Make sure that the video you are uploading has a audo bitrate of at least 16. The encoding wont function on a lower audio bitrate." )

    flvfile = models.FileField( upload_to="videos/flv/", null=True, blank=True,
            help_text="If you already have an encoded flash video, upload it here (no encoding needed).")

    thumbnail = models.ImageField( blank=True, null=True, 
            upload_to="videos/thumbnails/",
            help_text="If you uploaded a flv clip that was already encoded, you will need to upload a thumbnail as well. If you are planning use django-video to encode, you dont have to upload a thumbnail, as django-video will create it for you")

    # This option allows us to specify whether we need to encode the clip (manage.py encode)
    encode = models.BooleanField( default=False,
            help_text="Encode or Re-Encode the clip. If you only wanted to change some information on the item, and do not want to encode the clip again, make sure this option is not selected." )
    
    view_count = models.PositiveIntegerField(default=0, editable=False)

    def __unicode__(self):
        return "%s" % self.title

    @models.permalink
    def get_absolute_url(self):
        return ("video_details", [self.slug])

    def get_player_size(self):
        """ this method returns the styles for the player size
        """
        size = getattr(settings, 'VIDEOSTREAM_SIZE', '320x240').split('x')
        return "width: %spx; height: %spx;" % (size[0], size[1])
    
    def increment_count(self):
        self.view_count += 1
        self.save()
    
class Pool(models.Model):
    """
    model for a video to be applied to an object
    """

    video = models.ForeignKey(VideoStream)
    content_type = models.ForeignKey(ContentType, related_name='video_pool')
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    created_at = models.DateTimeField(_('created_at'), default=datetime.datetime.now)

    class Meta:
        # Enforce unique associations per object
        unique_together = (('video', 'content_type', 'object_id'),)
        verbose_name = _('video pool')
        verbose_name_plural = _('video pools')

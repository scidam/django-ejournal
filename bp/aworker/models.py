from __future__ import unicode_literals

import datetime
from uuid import uuid4

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _


class AbstractUserMixin(models.Model):
    firstname = models.CharField(max_length=100)
    email = models.EmailField()
    
 
class Author(AbstractUserMixin):
    pass
 
class Reviewer(AbstractUserMixin):
    pass
 
class Editor(AbstractUserMixin):
    pass
 
class Article(models.Model):
    pass

@python_2_unicode_compatible
class Invitation(models.Model):
    created = models.DateTimeField(auto_now=True, verbose_name=_('Created'))
    duration = models.IntegerField(default=86400,
                                   help_text=_('Duration in sec.'),
                                   verbose_name=_('Duration'))
    code = models.CharField(max_length=32, default=uuid4().hex, blank=True)

    def __str__(self):
        return 'Created: %s, duration: %s sec.'%(self.created, self.duration)

    @property
    def is_expired(self):
        return False if self.created <= timezone.now() <= self.created + datetime.timedelta(seconds=self.duration) else True
 
class ArtExtra(models.Model):
    pass
 
class Issue(models.Model):
    pass
 
class Review(models.Model):
    pass
 
class PaperSource(models.Model):
    pass
 
class Vote(models.Model):
    pass
 
class Answer(models.Model):
    pass


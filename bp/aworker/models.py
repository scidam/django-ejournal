from __future__ import unicode_literals

import datetime
from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _

@python_2_unicode_compatible
class AbstractUserMixin(models.Model):
    ROLE_CHOICES = (('AU', _('Author')),
                    ('ED', _('Editor')),
                    ('RE', _('Reviewer'))
                    )
    firstname = models.CharField(max_length=100)
    email = models.EmailField(blank=False, unique=True, verbose_name=_('Email'))
    secondname = models.CharField(max_length=100, blank=True, default='',
                                  verbose_name=_('Family name'))
    thirdname = models.CharField(max_length=100, blank=True, default='',
                                 verbose_name=_('Last name'))
    country = models.CharField(max_length=3, blank=True,
                               default='', verbose_name=_('Country code')
                               )
    position = models.CharField(max_length=255, default='', verbose_name=_('Position'),
                                blank=True)
    zipcode = models.CharField(max_length=10, default='', verbose_name=_('Zip code'),
                               blank=True
                               )
    organization = models.CharField(max_length=500, default='',
                                    verbose_name=_('Organization'),
                                    blank=True)
    address = models.CharField(max_length=300, default='', blank=True,
                               verbose_name=_('Address'))
    city = models.CharField(max_length=100, default='', blank=True,
                            verbose_name=_('City'))
    role = models.CharField(max_length=2, choices=ROLE_CHOICES, default=ROLE_CHOICES[0][0])
    phone = models.CharField(max_length=15, default='', blank=True)

    user = models.ForeignKey(User, null=True, blank=True, editable=False)

    def __str__(self):
        return ''

    def save(self, *args, **kwargs):
        user = User.objects.create(email=self.email, username=uuid4().hex[:12])
        self.user = user
        super(AbstractUserMixin, self).save(*args, **kwargs)

    @property
    def is_editor(self):
        return True if 'ED' in self.role else False

    @property
    def is_reviewer(self):
        return True if 'RE' in self.role else False


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


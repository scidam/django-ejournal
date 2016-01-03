from __future__ import unicode_literals

import datetime
import hashlib
import os
from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _


@python_2_unicode_compatible
class AbstractUserMixin(models.Model):
    ROLE_CHOICES = (('AU', _('Author')),
                    ('ED', _('Editor')),
                    ('RE', _('Reviewer'))
                    )
    firstname = models.CharField(max_length=100, verbose_name=_('First name'))
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

    def delete(self, *args, **kwargs):
        if self.user:
            self.user.delete()
        super(AbstractUserMixin, self).delete(*args, **kwargs)

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
    role = models.CharField(max_length=2, choices=AbstractUserMixin.ROLE_CHOICES,
                            default=AbstractUserMixin.ROLE_CHOICES[0][0]
                            )


    def __str__(self):
        return 'Created: %s, duration: %s sec.'%(self.created, self.duration)

    @property
    def is_expired(self):
        return False if (self.created <= timezone.now()) and (timezone.now() <= self.created + datetime.timedelta(seconds=self.duration)) else True


class ArtExtra(models.Model):
    udk = models.CharField(max_length=50, blank=True, default='')
    doi = models.CharField(max_length=50, blank=True, default='')
    pages = models.CharField(max_length=10, blank=False, default='')
    permalink = models.CharField(max_length=255, blank=True, default='')

class Issue(models.Model):
    coauthors = models.ManyToManyField(AbstractUserMixin, null=True, blank=True, verbose_name=_('Authors'), related_name='issues_all')
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'), blank=True, default=timezone.now())
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'), blank=True, default=timezone.now())
    paper = models.ForeignKey(Article, null=True, blank=True, verbose_name=_('Paper'))
    author = models.OneToOneField(AbstractUserMixin, blank=True, null=True, verbose_name=_('Main author'), related_name='issues')

@python_2_unicode_compatible
class Review(models.Model):
    file = models.FileField(upload_to='reviews/%Y/%m/%d/', null=True, blank=True)
    description = models.TextField(default='', blank=True, verbose_name=_('Description'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'), blank=True, default=timezone.now())
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'), blank=True, default=timezone.now())
    issue = models.ForeignKey(Issue, null=True, blank=True, verbose_name=_('Issue'), related_name='reviews')
    reviewer = models.ForeignKey(Reviewer, null=True, blank=True, verbose_name=_('Reviewer'), related_name='reviews')

    def __str__(self):
        res = ''
        if self.reviewer:
            res += self.reviewer.firstname.title()
            if self.reviewer.secondname:
                res += ' ' + self.reviewer.secondname.strip()[0].capitalize()+'.: '
        res += str(self.updated)
        return res


@python_2_unicode_compatible
class PaperSource(models.Model):
    file = models.FileField(upload_to='sources/%Y/%m/%d/', null=True, blank=False)
    description = models.TextField(default='', blank=True, verbose_name=_('Description'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'), blank=True, default=timezone.now())
    issue = models.ForeignKey(Issue, related_name='sources', null=True, blank=True, verbose_name=('Issue'))
    hashcode = models.CharField(default='', blank=True, verbose_name=_('Hash'), max_length=40)
    removed = models.BooleanField(default=False, blank=True, verbose_name=_('Remove'))
    owner = models.OneToOneField(AbstractUserMixin, null=True, blank=False, verbose_name=_('Owner'), related_name='sources')

    def __str__(self):
        res = ''
        if self.description:
            res += self.description[:30]
        if self.file:
            res += ' (file: %s)'%self.file.filename
        return res

    @property
    def filename(self):
        if self.file:
            return os.path.basename(self.file.name)
        else:
            return ''

    @property
    def modified(self):
        if not self.hashcode:
            return False
        if self.hashcode != self.current_hash:
            return True

    @property
    def current_hash(self):
        m = hashlib.sha1()
        if self.description:
            m.update(self.description)
        if self.file.name:
            self.file.seek(0)
            m.update(self.file.read())
        return m.hexdigest()


@python_2_unicode_compatible
class Vote(models.Model):
    issue = models.ForeignKey(Issue, related_name='votes', default=None, null=True, verbose_name=_('Issue'))
    vote = models.BooleanField(default=False, blank=False, verbose_name=_('Vote'))
    comment = models.TextField(default='', blank=True, verbose_name=_('Comment'))
    editor = models.OneToOneField(Editor, null=True, verbose_name=_('Editor'), blank=False)
    date = models.DateTimeField(auto_now=True, default=timezone.now())

    def __str__(self):
        if self.vote:
            res = _('Accepted')
        else:
            res = _('Discarded')
        res += ': %s'%self.date
        return res

class Answer(models.Model):
    pass


def compute_hash_on_paperissue(sender, instance, *args, **kwargs):
    if not instance.hashcode:
        instance.hashcode = instance.current_hash


def clean_files_paperissue(sender, instance, *args, **kwargs):
    try:
        os.remove(os.path.join(settings.MEDIA_ROOT, instance.file.path))
    except:
        pass

pre_save.connect(compute_hash_on_paperissue, sender=PaperSource)
post_delete.connect(clean_files_paperissue, sender=PaperSource)

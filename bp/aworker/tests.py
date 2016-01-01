from django.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from .models import (Article, Invitation, Author,
                     Reviewer, Editor, SciField, Issue,
                     ArtExtra,
                     Votes)


class AuthorTest(TestCase):
    '''Basic author behaviour and properties
    '''

    def setUp(self):
        auth1 = Author.objects.create(firstname='John', # required
                                      secondname='Doe',
                                      thirdname='',
                                      country_code='US',
                                      email='some@example.com', # required
                                      phone='',
                                      position='',
                                      organization='',
                                      zipcode='',
                                      address='',
                                      city='',
                                      role='AU'
                                      )

        auth2 = Author.objects.create(firstname='John',
                                      secondname='Doe',
                                      thirdname='',
                                      country_code='US',
                                      email='some-example.com', # use validator
                                      phone='', # use validator
                                      position='',
                                      organization='',
                                      zipcode='', # use validator
                                      address='',
                                      city='',
                                      role='AU'
                                      )

    def test_author_valid(self):
        ''' Test for auth1 assumed to be valid one'''
        self.assertIsInstance(self.auth1.user, User)

    def test_author_invalid(self):
        ''' auth2 is invalid instance'''
        self.assertRaises(ValidationError, self.auth2.clean())

    def test_author_username(self):
        self.assertEqual(self.auth1.email, self.auth1.user.username)

    def test_author_notstaff(self):
        self.assertFalse(self.auth1.user.is_staff)

    def test_is_author(self):
        self.assertTrue(self.auth1.is_author)

    def test_is_editor(self):
        self.assertFalse(self.auth1.is_editor)


class EditorTest(TestCase):
    '''Basic Editor behaviour'''

    def setUp(self):
        rev = Author.objects.create(firstname='John', # required
                                      secondname='Doe',
                                      thirdname='',
                                      country_code='US',
                                      email='some@example.com', # required
                                      phone='',
                                      position='',
                                      organization='',
                                      zipcode='',
                                      address='',
                                      city='',
                                      role='ED'
                                      )

    def test_is_author(self):
        self.assertTrue(self.rev.is_author)

    def test_is_editor(self):
        self.assertTrue(self.rev.is_editor)


class ReviewerTest(TestCase):
    def setUp(self):
        rev = Reviewer.objects.create(firstname='John', # required
                                      secondname='Doe',
                                      thirdname='',
                                      country_code='US',
                                      email='some@example.com', # required
                                      phone='',
                                      position='',
                                      organization='',
                                      zipcode='',
                                      address='',
                                      city='',
                                      role='RE'
                                      )

    def test_is_author(self):
        raise NotImplemented

    def test_is_editor(self):
        self.assertFalse(self.rev.is_editor)


class VotesTest(TestCase):
    '''Votes for the issue pending to publish.

    Votes is used by the editorial board staff for pending the issue to publising.
    '''

    def setUp(self):
        self.vt = Vote.objects.create(vote=True,
                                      editor=Editor.objects.create(role='ED'),
                                      comment='',
                                      issue=Issue.objects.create()
                                      )

    def test_vote_completeness(self):
        '''Vote instance assumed to have the following additional field:
        date - date of voting
        '''
        self.assertIsNotNone(self.vt.editor)
        self.assertTrue(self.vt.vote)
        self.assertIsNotNone(self.comment)
        self.assertIsNotNone(self.editor)
        self.assertIsNotNone(self.date)


class ArticleTests(TestCase):
    '''Articles that are already published
    '''
    def setUp(self):
        art = Article.objects.create(name='About winds influences on the spiritual life of the clergy?',
                                     published=True,
                                     pub_date=timezone.now(),
                                     authors=Author.objects.create(name='John Doe'),
                                     extrainfo=ArtExtra.objects.create()
                                     )



class InvitationTests(TestCase):
    def setUp(self):
        invite = Invitation.objects.create()
        
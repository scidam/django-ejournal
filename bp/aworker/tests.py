from django.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from .models import Article, Invitation, Author, Reviewer, Editor, SciField, Issue, ArtExtra


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
        
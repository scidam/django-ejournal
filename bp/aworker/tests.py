from django.auth.models import User
from django.test import TestCase
from django.utils import timezone

from .models import Article, Invitation, Author, Reviewer, Editor, SciField, Issue, ArtExtra


#Create your tests here.
class AuthorTest(TestCase):
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
                                      city=''
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
                                      city=''
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


class ArticleTests(TestCase):
    '''Articles that are already published
    '''
    def setUp(self):
        art = Article.objects.create(name='About winds influences on the spiritual life of the clergy?',
                                     published=True,
                                     pub_date=timezone.now(),
                                     authors=Author.objects.create(name='John Doe'),
                                     extrainfo=ArtExtra.objects.create(),
                                     
                               
                               


class InvitationTests(TestCase):
    def setUp(self):
        invite = Invitation.objects.create()
        
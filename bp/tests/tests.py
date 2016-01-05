

from aworker.forms import ArtExtraForm, ArticleForm, AbstractUserForm
from aworker.models import (Article, Invitation, Author,
                     Reviewer, Editor, Issue,
                     ArtExtra, Review, PaperSource,
                     Vote, Answer, AbstractUserMixin, Coauthor)
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.test import TestCase
from django.utils import timezone


class AbstractUserMixinTest(TestCase):
    '''Basic author behaviour and properties
    '''

    def setUp(self):
        self.auth1 = Author.objects.create(firstname='John', # required
                                      secondname='Doe',
                                      thirdname='',
                                      country='US',
                                      email='some@example.com', # required
                                      phone='',
                                      position='',
                                      organization='',
                                      zipcode='',
                                      address='',
                                      city='',
                                      role='AU'
                                      )

        self.auth2 = Author.objects.create(firstname='John',
                                      secondname='Doe',
                                      thirdname='',
                                      country='US',
                                      email='some-example.com', # use validator
                                      phone='', # use validator
                                      position='',
                                      organization='',
                                      zipcode='', # use validator
                                      address='',
                                      city='',
                                      role='AU'
                                      )

    def test_author_has_user(self):
        ''' Test for auth1 assumed to be valid one'''
        self.assertIsInstance(self.auth1.user, User)

    def test_author_user_attrs(self):
        self.assertTrue(AbstractUserMixin._meta.get_field('user').null)

    def test_author_user_non_editable(self):
        self.assertFalse(AbstractUserMixin._meta.get_field('user').editable)

    def test_author_email_mandatory(self):
        self.assertFalse(AbstractUserMixin._meta.get_field('email').blank)

    def test_author_email_unique(self):
        self.assertTrue(AbstractUserMixin._meta.get_field('email').unique)

    def test_author_email_default(self):
        self.assertEqual(AbstractUserMixin._meta.get_field('email').default, '')

    def test_author_email_type(self):
        self.assertIsInstance(AbstractUserMixin._meta.get_field('email'), models.EmailField)

    def test_author_role_default(self):
        self.assertEqual(AbstractUserMixin._meta.get_field('role').default, 'AU')

    def test_author_role_mandatory(self):
        self.assertFalse(AbstractUserMixin._meta.get_field('role').blank)

    def test_author_role_attribute(self):
        self.assertIsNotNone(AbstractUserMixin._meta.get_field('role').choices)

    def test_author_firstname_mandatory(self):
        self.assertFalse(AbstractUserMixin._meta.get_field('firstname').blank)

    def test_author_firstname_default(self):
        self.assertEqual(AbstractUserMixin._meta.get_field('firstname').default, '')

    def test_author_firstname_type(self):
        self.assertIsInstance(AbstractUserMixin._meta.get_field('firstname'), models.CharField)

    def test_author_firstname_maxlen(self):
        self.assertGreater(AbstractUserMixin._meta.get_field('firstname').max_length, 50)

    def test_author_secondname_nonmandatory(self):
        self.assertTrue(AbstractUserMixin._meta.get_field('secondname').blank)

    def test_author_secondname_default(self):
        self.assertEqual(AbstractUserMixin._meta.get_field('secondname').default, '')

    def test_author_secondname_type(self):
        self.assertIsInstance(AbstractUserMixin._meta.get_field('secondname'), models.CharField)

    def test_author_secondname_maxlen(self):
        self.assertGreater(AbstractUserMixin._meta.get_field('secondname').max_length, 50)

    def test_author_thirdname_nonmandatory(self):
        self.assertTrue(AbstractUserMixin._meta.get_field('thirdname').blank)

    def test_author_thirdname_default(self):
        self.assertEqual(AbstractUserMixin._meta.get_field('thirdname').default, '')

    def test_author_thirdname_type(self):
        self.assertIsInstance(AbstractUserMixin._meta.get_field('thirdname'), models.CharField)

    def test_author_thirdname_maxlen(self):
        self.assertGreater(AbstractUserMixin._meta.get_field('thirdname').max_length, 50)

    def test_author_country_code_type(self):
        self.assertIsInstance(AbstractUserMixin._meta.get_field('country'), models.CharField)

    def test_author_country_non_mandatory(self):
        self.assertTrue(AbstractUserMixin._meta.get_field('country').blank)

    def test_author_country_maxlen(self):
        self.assertEqual(AbstractUserMixin._meta.get_field('country').max_length, 3)

    def test_author_country_default(self):
        self.assertEqual(AbstractUserMixin._meta.get_field('country').default, '')

    def test_author_phone_nonmandatory(self):
        self.assertTrue(AbstractUserMixin._meta.get_field('phone').blank)

    # TODO: Probably, it should be replaced with third-party phone-number-field for Django

    def test_author_phone_formvalidation(self):
        self.assertFalse(AbstractUserForm(instance=self.auth1).is_valid())
        self.assertTrue(issubclass(AbstractUserForm, forms.ModelForm))
        f = AbstractUserForm({'firstname' : 'John', 'email':
                              'sample@mail.com', 'phone':'+11051565415',
                              'zipcode': '12321', 'role':'AU'},
                             instance=self.auth1)
        self.assertTrue(f.is_valid())
        f = AbstractUserForm({'firstname' : 'John', 'email':
                              'sample@mail.com', 'phone':'+748d83s323',
                              'zipcode': '12321','role':'AU'},
                             instance=self.auth1)
        self.assertFalse(f.is_valid())

    def test_author_phone_maxlen(self):
        self.assertGreater(AbstractUserMixin._meta.get_field('phone').max_length, 15)

    def test_author_phone_default(self):
        self.assertEqual(AbstractUserMixin._meta.get_field('phone').default, '')

    def test_zipcode_nonmandatory(self):
        self.assertTrue(AbstractUserMixin._meta.get_field('zipcode').blank)

    def test_zipcode_length(self):
        self.assertEqual(AbstractUserMixin._meta.get_field('zipcode').max_length, 10)

    def test_zipcode_default(self):
        self.assertEqual(AbstractUserMixin._meta.get_field('zipcode').default, '')

    def test_zipcode_form_validation(self):
        self.assertFalse(AbstractUserForm(instance=self.auth1).is_valid())
        f = AbstractUserForm({'firstname' : 'John', 'email': 'sample@mail.com', 'phone':'+11051565415',
                              'zipcode': '690125', 'role': 'AU'},
                             instance=self.auth1)
        self.assertTrue(f.is_valid())
        f = AbstractUserForm({'firstname' : 'John', 'email': 'sample@mail.com', 'phone':'+11051565415',
                              'zipcode': '69O125', 'role': 'AU'},
                             instance=self.auth1)
        self.assertFalse(f.is_valid())


    def test_author_invalid(self):
        ''' auth2 is invalid instance'''
        self.assertRaises(ValidationError, self.auth2.clean())

    def test_author_username(self):
        self.assertEqual(self.auth1.email, self.auth1.user.email)

    def test_author_notstaff(self):
        self.assertFalse(self.auth1.user.is_staff)

    def test_is_editor(self):
        self.assertFalse(self.auth1.is_editor)


class EditorTest(TestCase):
    '''Basic Editor behaviour'''

    def setUp(self):
        self.rev = Author.objects.create(firstname='John', # required
                                      secondname='Doe',
                                      thirdname='',
                                      country='US',
                                      email='some@example.com', # required
                                      phone='',
                                      position='',
                                      organization='',
                                      zipcode='',
                                      address='',
                                      city='',
                                      role='ED'
                                      )

    def test_is_editor(self):
        self.assertTrue(self.rev.is_editor)


class ReviewerTest(TestCase):
    def setUp(self):
        self.rev = Reviewer.objects.create(firstname='John', # required
                                      secondname='Doe',
                                      thirdname='',
                                      country='US',
                                      email='some@example.com', # required
                                      phone='',
                                      position='',
                                      organization='',
                                      zipcode='',
                                      address='',
                                      city='',
                                      role='RE'
                                      )

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
        self.assertIsNotNone(self.vt.comment)
        self.assertIsNotNone(self.vt.editor)
        self.assertIsNotNone(self.vt.date)

    def test_vote_type(self):
        self.assertIsInstance(Vote._meta.get_field('vote'), models.BooleanField)

    def test_vote_default_value(self):
        self.assertFalse(Vote._meta.get_field('vote').default)

    def test_vote_comment_type(self):
        self.assertIsInstance(Vote._meta.get_field('comment'), models.TextField)

    def test_vote_comment_default(self):
        self.assertEqual(Vote._meta.get_field('comment').default, '')

    def test_vote_optional(self):
        self.assertTrue(Vote._meta.get_field('vote').blank)

    def test_vote_date_update(self):
        self.assertTrue(Vote._meta.get_field('date').auto_now)
        self.assertFalse(Vote._meta.get_field('date').auto_now_add)

    def test_vote_editor_type(self):
        self.assertIsInstance(Vote._meta.get_field('editor'), models.ForeignKey)

    def test_vote_editor_nonmandatory(self):
        self.assertFalse(Vote._meta.get_field('editor').blank)
        self.assertTrue(Vote._meta.get_field('editor').null)

    def test_vote_editor_related(self):
        self.assertEqual(Vote._meta.get_field('editor').related_query_name(), 'votes')

    def test_vote_issue_type(self):
        self.assertIsInstance(Vote._meta.get_field('issue'), models.ForeignKey)
        self.assertTrue(Vote._meta.get_field('issue').null)
        self.assertTrue(Vote._meta.get_field('issue').blank)

    def test_vote_issue_related(self):
        self.assertEqual(Vote._meta.get_field('issue').related_query_name(), 'votes')


class PaperSourceTests(TestCase):
    '''Source of each paper. It is used by the Issue instance.
    '''
    def setUp(self):
        self.papersource = PaperSource.objects.create(owner=Author.objects.create())
        self.papersource1 = PaperSource.objects.create(description='new1')
        self.papersource2 = PaperSource.objects.create(description='new')
        self.papersource3 = PaperSource.objects.create(file=SimpleUploadedFile('new.txt','new'))

    def test_paper_file_mandatory(self):
        self.assertTrue(PaperSource._meta.get_field('file').null)
        self.assertFalse(PaperSource._meta.get_field('file').blank)

    def test_paper_description_type(self):
        self.assertIsInstance(PaperSource._meta.get_field('description'), models.TextField)

    def test_paper_description_default(self):
        self.assertEqual(PaperSource._meta.get_field('description').default, '')

    def test_paper_description_non_mandatory(self):
        self.assertTrue(PaperSource._meta.get_field('description').blank)

    def test_paper_created_type(self):
        self.assertIsInstance(PaperSource._meta.get_field('created'), models.DateTimeField)

    def test_paper_created_attribute(self):
        self.assertTrue(PaperSource._meta.get_field('created').auto_now_add)

    def test_paper_removed_default(self):
        self.assertFalse(PaperSource._meta.get_field('removed').default)

    def test_paper_removed_nonmandatory(self):
        self.assertTrue(PaperSource._meta.get_field('removed').blank)

    def test_paper_removed_type(self):
        self.assertIsInstance(PaperSource._meta.get_field('removed'), models.BooleanField)

    def test_paper_issue_mandatory(self):
        self.assertFalse(PaperSource._meta.get_field('issue').blank)
        self.assertTrue(PaperSource._meta.get_field('issue').null)

    def test_paper_issue_type(self):
        self.assertIsInstance(PaperSource._meta.get_field('issue'), models.ForeignKey)

    def test_paper_issue_related_name(self):
        self.assertEqual(PaperSource._meta.get_field('issue').related_query_name(), 'sources')

    def test_paper_owner_type(self):
        self.assertIsInstance(PaperSource._meta.get_field('owner'), models.ForeignKey)

    def test_paper_owner_mandatory(self):
        self.assertFalse(PaperSource._meta.get_field('owner').blank)
        self.assertTrue(PaperSource._meta.get_field('owner').null)

    def test_paper_owner_instance_type(self):
        self.assertIsInstance(self.papersource.owner, AbstractUserMixin)

    def test_paper_owner_related(self):
        self.assertEqual(PaperSource._meta.get_field('owner').related_query_name(),'sources')

    def test_paper_source_completeness(self):
        self.assertIsNotNone(self.papersource.file)
        self.assertIsNone(self.papersource.file.name)
        self.assertEqual(self.papersource.description, '')
        self.assertIsNotNone(self.papersource.created)
        self.assertIsNone(self.papersource.issue)
        self.assertIsNotNone(self.papersource.hashcode)
        self.assertFalse(self.papersource.removed)
        self.assertIsNotNone(self.papersource.owner)

    def test_paper_source_hash_changed(self):
        self.assertNotEqual(self.papersource.hashcode, self.papersource1.hashcode)

    def test_paper_source_equal(self):
        self.assertNotEqual(self.papersource1.hashcode, self.papersource2.hashcode)

    def test_paper_with_file(self):
        self.assertEqual(self.papersource3.hashcode, self.papersource2.hashcode)

    def test_length_hashcode(self):
        self.assertEqual(len(self.papersource1.hashcode), 40)


class CoauthorModelTests(TestCase):
    def setUp(self):
        self.author = Author.objects.create(firstname='Mike', email='author@mail.com')

    def test_coauthor_firstname_type(self):
        self.assertIsInstance(Coauthor._meta.get_field('firstname'), models.CharField)

    def test_coauthor_firstname_maxlen(self):
        self.assertEqual(Coauthor._meta.get_field('firstname').max_length, 100)

    def test_coauthor_firstname_mandatory(self):
        self.assertFalse(Coauthor._meta.get_field('firstname').blank)

    def test_coauthor_firstname_default(self):
        self.assertEqual(Coauthor._meta.get_field('firstname').default, '')

    def test_coauthor_secondname_type(self):
        self.assertIsInstance(Coauthor._meta.get_field('secondname'), models.CharField)

    def test_coauthor_secondname_maxlen(self):
        self.assertEqual(Coauthor._meta.get_field('secondname').max_length, 100)

    def test_coauthor_secondname_nonmandatory(self):
        self.assertTrue(Coauthor._meta.get_field('secondname').blank)

    def test_coauthor_secondname_default(self):
        self.assertEqual(Coauthor._meta.get_field('secondname').default, '')

    def test_coauthor_thirdname_type(self):
        self.assertIsInstance(Coauthor._meta.get_field('thirdname'), models.CharField)

    def test_coauthor_thirdname_maxlen(self):
        self.assertEqual(Coauthor._meta.get_field('thirdname').max_length, 100)

    def test_coauthor_thirdname_nonmandatory(self):
        self.assertTrue(Coauthor._meta.get_field('thirdname').blank)

    def test_coauthor_thirdname_default(self):
        self.assertEqual(Coauthor._meta.get_field('thirdname').default, '')

    def test_coauthor_email_type(self):
        self.assertIsInstance(Coauthor._meta.get_field('email'), models.EmailField)

    def test_coauthor_email_nonmandatory(self):
        self.assertTrue(Coauthor._meta.get_field('email').blank)

    def test_coauthor_email_default(self):
        self.assertEqual(Coauthor._meta.get_field('email').default,'')

    def test_coauthor_organization_type(self):
        self.assertIsInstance(Coauthor._meta.get_field('organization'), models.CharField)

    def test_coauthor_organization_maxlen(self):
        self.assertEqual(Coauthor._meta.get_field('organization').max_length, 500)

    def test_coauthor_organization_nonmandatory(self):
        self.assertTrue(Coauthor._meta.get_field('organization').blank)

    def test_coauthor_organization_default(self):
        self.assertEqual(Coauthor._meta.get_field('organization').default, '')

    def test_coauthor_author_field_type(self):
        self.assertIsInstance(Coauthor._meta.get_field('author'), models.ForeignKey)

    def test_coauthor_author_mandatory(self):
        self.assertFalse(Coauthor._meta.get_field('author').blank)
        self.assertTrue(Coauthor._meta.get_field('author').null)

    def test_coauthor_object_creation(self):
        coauth = Coauthor.objects.create(author=self.author, firstname='Bubble',
                                         secondname='gum', email='mail@mail.com')
        self.assertIsInstance(coauth, Coauthor)

    def test_coauthor_issue_type(self):
        self.assertIsInstance(Coauthor._meta.get_field('issue'), models.ForeignKey)

    def test_coauthor_issue_mandatory(self):
        self.assertFalse(Coauthor._meta.get_field('issue').blank)
        self.assertTrue(Coauthor._meta.get_field('issue').null)

    def test_coauthor_issue_related_name(self):
        self.assertTrue(Coauthor._meta.get_field('issue').related_query_name(), 'coauthors')


class IssueTest(TestCase):
    '''Initially issue is created by the author
    '''

    def setUp(self):
        author = Author.objects.create(firstname='Mike', email='author@mail.com')
        reviwer = Reviewer.objects.create(firstname='John', email='sample@mail.com')
        editor = Editor.objects.create(firstname='John', email='editor@mail.com')
        editor1 = Editor.objects.create(firstname='John', email='editor1@mail.com')
        self.issue = Issue.objects.create()
        rev1 = Review.objects.create(reviewer=reviwer, issue=self.issue)
        rev2 = Review.objects.create(reviewer=reviwer, issue=self.issue)
        rev3 = Review.objects.create(reviewer=reviwer, issue=self.issue)
        self.issue.author = author
        self.issue.save()
        vote1 = Vote.objects.create(editor=editor, vote=True, issue=self.issue)
        vote2 = Vote.objects.create(editor=editor1, vote=False, issue=self.issue)
        vote1.save()
        vote2.save()
        answer1 = Answer.objects.create(review=rev1)
        answer2 = Answer.objects.create(review=rev3)
        self.reviewer = reviwer
        p1 = PaperSource.objects.create(issue=self.issue, description='Just empty')
        p2 = PaperSource.objects.create(issue=self.issue, description='Another empty')

    def test_issue_completeness(self):
        self.assertIsNotNone(self.issue.created)
        self.assertIsNotNone(self.issue.reviews)
        self.assertIsNotNone(self.issue.updated)
        self.assertIsInstance(self.issue.paper, Article) # Link to the article instance! output paper
        self.assertIsNotNone(self.issue.sources)

    def test_issue_created_type(self):
        self.assertIsInstance(Issue._meta.get_field('created'), models.DateTimeField)

    def test_issue_created_autofield(self):
        self.assertTrue(Issue._meta.get_field('created').auto_now_add)

    def test_issue_author_type(self):
        self.assertIsInstance(Issue._meta.get_field('author'), models.ForeignKey)
        self.assertIsInstance(self.issue.author, AbstractUserMixin)

    def test_issue_author_attributes(self):
        self.assertFalse(Issue._meta.get_field('author').blank)
        self.assertTrue(Issue._meta.get_field('author').null)

    def test_issue_author_related_name(self):
        self.assertEqual(Issue._meta.get_field('author').related_query_name(), 'issues')

    def test_issue_reviewers_type(self):
        self.assertIsInstance(Issue._meta.get_field('reviewers'), models.ManyToManyField)

    def test_issue_reviewers_attributes(self):
        self.assertTrue(Issue._meta.get_field('reviewers').blank)
        self.assertTrue(Issue._meta.get_field('reviewers').null)

    def test_issue_reviewers_add_reviewer(self):
        self.assertFalse(self.issue.reviewers.exists())
        self.issue.reviewers.add(self.reviewer)
        self.issue.save()
        self.assertTrue(self.issue.reviewers.exists())
        self.assertIn(self.reviewer, self.issue.reviewers.all())
        self.assertEqual(self.issue.reviewers.count(), 1)


    def test_issue_deletion(self):
        '''
        Issue could be deleted if no reviewers were attached to it.
        This test tries to delete issue instance with reviewers and without ones.
        '''



class ArticleTests(TestCase):
    '''Articles that are already published
    '''

    def setUp(self):
        self.art = Article.objects.create(name='About winds influences on the spiritual life of the clergy?',
                                     published=True,
                                     pub_date=timezone.now(),
                                     authors=Author.objects.create(firstname='John Doe', email='me@mail.com'),
                                     extrainfo=ArtExtra.objects.create()
                                     )

    def test_article_is_extrainfor_null_true(self):
        self.assertTrue(Article._meta.get_field('extrainfo').null)
        self.assertTrue(Article._meta.get_field('extrainfo').blank)

    def test_article_default_published_false(self):
        self.assertFalse(Article._meta.get_field('published').null)

    def test_article_authors_null_true(self):
        self.assertTrue(Article._meta.get_field('authors').null)
        self.assertTrue(Article._meta.get_field('authors').blank)

    def test_article_name_required(self):
        self.assertFalse(Article._meta.get_field('name').blank)
        self.assertGreater(len(self.art.name)>10)

    def test_article_str_method(self):
        res = self.art.name[:30]+' ...:'+ 'Published: %s'%(self.art.pub_date if self.art.pub_date else False,)
        self.assertEqual(str(self.art), res)

    def test_article_keywords(self):
        self.assertFalse(Article._meta.get_field('keywords').blank)

    def test_article_keywords_validation(self):
        art_form = ArticleForm(instance=self.art)
        self.assertFalse(art_form.is_valid())
        bound_art_form = ArticleForm({'name': 'test', 'abstract':'Test', 'keywords':'one,two,three'}, instance=self.art)
        self.assertTrue(bound_art_form.is_valid())
        bound_art_form = ArticleForm({'name': 'test', 'abstract':'Test', 'keywords':''}, instance=self.art)
        self.assertFalse(bound_art_form.is_valid())

    def test_article_keywords_length(self):
        self.assertEqual(Article._meta.get_field('keywords').max_length, settings.EJOURNAL_MAX_KEYWORDS_LENGTH)

    def test_article_description_length(self):
        self.assertEqual(Article._meta.get_field('description').max_length, settings.EJOURNAL_MAX_DESCRIPTION_LENGTH)

    def test_article_description_non_mandatory(self):
        self.assertTrue(Article._meta.get_field('description').blank)
        self.assertEqual(Article._meta.get_field('description').default, '')

    def test_article_pub_date_field_type(self):
        self.assertIsInstance(Article._meta.get_field('pub_date'), models.DateField)

    def test_article_pub_date_non_mandatory(self):
        self.assertTrue(Article._meta.get_field('pub_date').blank)


class ArtExtraTests(TestCase):

    def setUp(self):
        self.artextra = ArtExtra.objects.create(doi='', udk='', pages='', permalink='')
        self.validdoi = ArtExtra.objects.create(doi='10.2344/254', udk='527.03', pages='', permalink='')

    def test_artextra_completeness(self):
        self.assertEqual(self.artextra.doi, '')
        self.assertEqual(self.artextra.udk, '')
        self.assertEqual(self.artextra.pages, '')
        self.assertEqual(self.artextra.permalink, '')

    def test_doi_is_valid(self):
        artextra_form = ArtExtraForm(instance=self.artextra)
        self.assertFalse(artextra_form.is_valid()) # pages assumed to be mandatory
        bound_artextra_form = ArtExtraForm({'doi':'10.17581/bp.2016.05102', 'udk':'', 'pages':'1-2'}, instance=self.artextra)
        self.assertTrue(bound_artextra_form.is_valid())
        bound_artextra_form = ArtExtraForm({'doi':'//df//sdf', 'udk':'', 'pages':'1-2'}, instance=self.artextra)
        self.assertFalse(bound_artextra_form.is_valid())

    def test_udk_is_valid(self):
        artextra_form = ArtExtraForm(instance=self.artextra)
        self.assertFalse(artextra_form.is_valid()) # pages assumed to be mandatory
        bound_artextra_form = ArtExtraForm({'doi':'', 'udk':'518', 'pages':'1-2'}, instance=self.artextra)
        self.assertTrue(bound_artextra_form.is_valid())
        bound_artextra_form = ArtExtraForm({'doi':'', 'udk':'buba', 'pages':'1-2'}, instance=self.artextra)
        self.assertFalse(bound_artextra_form.is_valid())

    def test_doi_max_length(self):
        self.assertGreater(ArtExtra._meta.get_field('doi').max_length, 30)

    def test_udk_max_length(self):
        self.assertGreater(ArtExtra._meta.get_field('udk').max_length, 30)

    def test_pages_mandatory(self):
        self.assertGreater(ArtExtra._meta.get_field('pages').max_length, 9)
        self.assertFalse(ArtExtra._meta.get_field('pages').blank)

    def test_permalink_optional(self):
        self.assertTrue(ArtExtra._meta.get_field('permalink').blank)
        self.assertGreater(ArtExtra._meta.get_field('permalink').max_length, 200)


class ReviewTests(TestCase):
    def setUp(self):
        self.issue = Issue.objects.create()
        self.reviewer = Reviewer.objects.create(firstname='John', email='sample@mail.com',
                                                secondname='Doe')
        self.review = Review.objects.create(reviewer=self.reviewer, issue=self.issue,
                                            description='nothing')

    def test_str_method(self):
        self.assertEqual(str(self.review), 'John D.: %s'%self.review.updated)

    def test_review_completeness(self):
        self.assertIsNotNone(self.review.file)
        self.assertEqual(self.review.description, 'nothing')
        self.assertIsNotNone(self.review.reviewer)
        self.assertIsNotNone(self.review.created)
        self.assertIsNotNone(self.review.updated)
        self.assertIsNotNone(self.review.issue)

    def test_review_file_attributes(self):
        self.assertTrue(Review._meta.get_field('file').null)
        self.assertTrue(Review._meta.get_field('file').blank)

    def test_review_issue_attributes(self):
        self.assertTrue(Review._meta.get_field('issue').null)
        self.assertTrue(Review._meta.get_field('issue').blank)

    def test_review_description_attributes(self):
        self.assertTrue(Review._meta.get_field('description').blank)
        self.assertIsInstance(Review._meta.get_field('description'), models.TextField)

    def test_review_reviewer_attributes(self):
        self.assertTrue(Review._meta.get_field('reviewer').null)
        self.assertTrue(Review._meta.get_field('reviewer').blank)


class AnswerTests(TestCase):

    def setUp(self):
        self.author = Author.objects.create(firstname='Mike', email='iamauthor@mail.com', secondname='Form')
        self.issue = Issue.objects.create(author = self.author)
        self.reviewer = Reviewer.objects.create(firstname='John', email='sample@mail.com',
                                                secondname='Doe')
        self.review = Review.objects.create(reviewer=self.reviewer, issue=self.issue,
                                            description='nothing')
        self.attach1 = PaperSource.objects.create(owner=self.author, description='First mentioned')
        self.attach2 = PaperSource.objects.create(owner=self.author, description='Another note')
        self.answer = Answer.objects.create(review=self.review, description='I am right!')

    def test_m2m_add_on_attachment(self):
        self.answer.attachments.add(self.attach1)
        self.answer.attachments.add(self.attach2)
        self.answer.save()
        # testing for listing all attachments
        self.assertIn(self.attach1, self.answer.attachments.all())
        self.assertIn(self.attach2, self.answer.attachments.all())

    def test_str_method_on_answer(self):
        self.assertEqual(str(self.answer), 'By Mike F.: %s'%self.answer.created)

    def test_answer_completeness(self):
        # Just to test existing fields
        self.assertIsNotNone(self.answer.created)
        self.assertIsNotNone(self.answer.attachments)
        self.assertIsNotNone(self.answer.review)
        self.assertEqual(self.answer.description, 'I am right!')
        self.assertIsNone(self.answer.file.name)

    def test_answer_created(self):
        self.assertTrue(Answer._meta.get_field('created').auto_now_add)

    def test_answer_review_type(self):
        self.assertIsInstance(Answer._meta.get_field('review'), models.OneToOneField)

    def test_answer_file_nonmandatory(self):
        self.assertTrue(Answer._meta.get_field('file').blank)
        self.assertTrue(Answer._meta.get_field('file').null)

    def test_answer_description_type(self):
        self.assertIsInstance(Answer._meta.get_field('description'), models.TextField)

    def test_answer_description_nonmandatory(self):
        self.assertTrue(Answer._meta.get_field('description').blank)

    def test_answer_description_default(self):
        self.assertEqual(Answer._meta.get_field('description').default, '')

    def test_answer_review_mandatory(self):
        self.assertFalse(Answer._meta.get_field('review').blank)
        self.assertTrue(Answer._meta.get_field('review').null)


class InvitationTests(TestCase):

    def setUp(self):
        self.inv = Invitation.objects.create(duration=86400*5)
        self.invexp = Invitation.objects.create(duration=0)
        import time
        time.sleep(1)

    def test_invitation(self):
        self.assertEqual(len(self.inv.code), 32)
        self.assertEqual(self.inv.duration, 86400*5)

    def test_is_expired(self):
        self.assertFalse(self.inv.is_expired)

    def test_is_expired_true(self):
        self.assertTrue(self.invexp.is_expired)

    def test_invitation_role(self):
        '''Each invitation has roles:
        Editor invitation
        Reviewer invitation
        '''
        self.assertIsInstance(Invitation._meta.get_field('role'), models.CharField)
        self.assertFalse(Invitation._meta.get_field('role').blank)
        self.assertIsNotNone(Invitation._meta.get_field('role').choices)

from django.db import models

# Create your models here.

class AbstractUserMixin(models.Model):
    pass

class Author(AbstractUserMixin):
    pass

class Reviewer(AbstractUserMixin):
    pass

class Editor(AbstractUserMixin):
    pass

class Article(models.Model):
    pass

class Invitation(models.Model):
    pass


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


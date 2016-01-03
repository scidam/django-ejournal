from django import forms
from .models import Article, ArtExtra


class ArticleForm(forms.ModelForm):
    class __Meta__:
        model = Article

class ArtExtraForm(forms.ModelForm):
    class __Meta__:
        model = ArtExtra

from django import forms
from .models import Article, ArtExtra


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article

class ArtExtraForm(forms.ModelForm):
    class Meta:
        model = ArtExtra
        fields = ['doi', 'udk', 'pages', 'permalink']

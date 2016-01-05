import re

from django import forms
from django.utils.translation import ugettext as _

from .models import Article, ArtExtra, AbstractUserMixin


doi_pat = re.compile(r'10\.\d{4,}\/bp\.\d{4}\.\d{4,}')
udk_pat = re.compile(r'[0-9]+[;\:\.0-9]+')


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article


class ArtExtraForm(forms.ModelForm):
    class Meta:
        model = ArtExtra
        fields = ['doi', 'udk', 'pages', 'permalink']

    def clean_doi(self):
        data = self.cleaned_data.get('doi')
        if data:
            if not doi_pat.match(data):
                raise forms.ValidationError(_("Improper format of DOI"), code='invalid')
        return data

    def clean_udk(self):
        data = self.cleaned_data.get('udk')
        if data:
            if not udk_pat.match(data):
                raise forms.ValidationError(_("Improper format of UDK"), code='invalid')
        return data


class AbstractUserForm(forms.ModelForm):
    class Meta:
        model = AbstractUserMixin

import re

from django import forms
from django.utils.translation import ugettext as _

from .models import Article, ArtExtra, AbstractUserMixin


doi_pat = re.compile(r'\s?10\.\d{4,}\/bp\.\d{4}\.\d{4,}\s?$')
udk_pat = re.compile(r'\s?[0-9]+[;\:\.0-9]+\s?$')
zipcode_pat = re.compile(r'\s?\d+\s?$')
phone_pat = re.compile(r'\s?\+?\d[\d\-]+\s?$')

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
        fields = '__all__'

    def clean_zipcode(self):
        data = self.cleaned_data.get('zipcode')
        if data:
            if not zipcode_pat.match(data):
                raise forms.ValidationError(_("Improper format of zipcode"), code='invalid')
        return data

    def clean_phone(self):
        data = self.cleaned_data.get('phone')
        if data:
            if not phone_pat.match(data):
                raise forms.ValidationError(_("Improper format of phone"), code='invalid')
        return data
    

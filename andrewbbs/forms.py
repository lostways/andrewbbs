from django import forms

from .models import AccessCode

class AccessCodeForm(forms.ModelForm):
    class Meta:
        model = AccessCode
        fields = ['code']
        labels = {'code': ''}


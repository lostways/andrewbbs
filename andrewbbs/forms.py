from django import forms

class AccessCodeForm(forms.Form):
   code = forms.CharField(max_length=100, label="") 


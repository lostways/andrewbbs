import re
from django import forms
from django.forms import ModelForm

from .models import Member

class AccessCodeForm(forms.Form):
   code = forms.CharField(max_length=100, label="") 

class MemberForm(ModelForm):
   def clean_phone(self):
      data = self.cleaned_data['phone']
      return re.sub(r'\D', '', data)

   class Meta:
      model = Member
      fields = ['handle', 'phone', 'first_name', 'last_name', 'zip']
      labels = {
         'handle': 'Handle',
         'phone': 'Mobile #',
         'first_name': 'First Name',
         'last_name': 'Last Name',
         'zip': 'Zip',
      }
      widgets = {
         'handle': forms.TextInput(attrs={'placeholder': 'Handle'}),
         'phone': forms.TextInput(attrs={'placeholder': 'Phone'}),
         'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
         'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
         'zip': forms.TextInput(attrs={'placeholder': 'Zip'}),
      }

class LoginForm(forms.Form):
   handle = forms.CharField(max_length=100, label="Handle")
   def clean_handle(self):
      handle = self.cleaned_data.get('handle')
      member = Member.objects.filter(handle=handle)
      if not member.exists():
         raise forms.ValidationError("Handle not found")
      return handle

class OTPForm(forms.Form):
   code = forms.CharField(max_length=6, label="Code")
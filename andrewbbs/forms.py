from django import forms

class AccessCodeForm(forms.Form):
   code = forms.CharField(max_length=100, label="") 

class MemberForm(forms.Form):
   handle = forms.CharField(max_length=100, label="Your Handle", required=True)
   phone = forms.CharField(max_length=100, label="Mobile #", required=True) 
   first_name = forms.CharField(max_length=100, label="First Name", required=False) 
   last_name = forms.CharField(max_length=100, label="Last Name", required=False)
   zip = forms.CharField(max_length=100, label="Zipcode", required=False) 


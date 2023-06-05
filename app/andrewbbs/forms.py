import re
from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from .models import Message

User = get_user_model()


class MessageForm(forms.Form):
    recipient = forms.CharField(max_length=100, label="To Handle")
    subject = forms.CharField(
        widget=forms.TextInput({"size": 80, "class": "width-full"}),
        max_length=80,
        label="Subject",
    )
    body = forms.CharField(
        widget=forms.Textarea({"class": "width-full", "cols": 40}),
        max_length=1024,
        label="Message",
    )

    # find recipient and validate that they exist
    def clean_recipient(self):
        recipient = self.cleaned_data.get("recipient")
        if not User.objects.filter(handle=recipient).exists():
            raise forms.ValidationError("Handle not found")
        return recipient


class AccessCodeForm(forms.Form):
    code = forms.CharField(max_length=100, label="")


class MemberForm(ModelForm):
    class Meta:
        model = User
        fields = ["handle", "phone", "first_name", "last_name", "zip"]
        labels = {
            "handle": "Handle",
            "phone": "Mobile #",
            "first_name": "First Name",
            "last_name": "Last Name",
            "zip": "Zip",
        }
        widgets = {
            "handle": forms.TextInput(attrs={"placeholder": "Handle"}),
            "phone": PhoneNumberPrefixWidget(
                country_choices=[("US", "+1")], attrs={"placeholder": "Mobile #"}
            ),
            "first_name": forms.TextInput(attrs={"placeholder": "First Name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last Name"}),
            "zip": forms.TextInput(attrs={"placeholder": "Zip"}),
        }


class LoginForm(forms.Form):
    handle = forms.CharField(max_length=100, label="Handle")

    def clean_handle(self):
        handle = self.cleaned_data.get("handle")
        member = User.objects.filter(handle=handle)
        if not member.exists():
            raise forms.ValidationError("Handle not found")
        return handle


class OTPForm(forms.Form):
    code = forms.CharField(max_length=6, label="Code")

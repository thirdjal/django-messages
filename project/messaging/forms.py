from django import forms

from .models import Message


class AttachmentForm(forms.Form):
    attachments = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True, "class": "custom-file-input"}))  # attrs={"class": "custom-file-input"}


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ("subject", "body", "parent")
        widgets = {
            "subject": forms.TextInput(attrs={"class": "form-control"}),
            "body": forms.HiddenInput(),
            "parent": forms.HiddenInput()
        }

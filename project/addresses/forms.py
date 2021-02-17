from django import forms

from .models import Address, Email, Phone


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = (
            "type",
            "street",
            "street2",
            "city",
            "state",
            "zip_code",
            "is_published",
        )


class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ("type", "address", "is_published", "is_subscribed")


class PhoneForm(forms.ModelForm):
    class Meta:
        model = Phone
        fields = ("type", "number", "is_published")

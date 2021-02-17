from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import Member


class MemberChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Member


class MemberCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Member
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "middle_name",
            "last_name",
            "nickname",
            "gender",
        )

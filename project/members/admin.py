from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from project.addresses.forms import AddressForm, EmailForm, PhoneForm
from project.addresses.models import Address, Email, Phone

from .forms import MemberChangeForm, MemberCreationForm
from .models import Family, Member


class AddressInline(admin.StackedInline):
    form = AddressForm
    model = Address
    extra = 0


class EmailInline(admin.TabularInline):
    form = EmailForm
    model = Email
    extra = 0


class PhoneInline(admin.TabularInline):
    form = PhoneForm
    model = Phone
    extra = 0


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    search_fields = ["members__first_name", "members__last_name", "members__nickname"]


@admin.register(Member)
class MemberAdmin(UserAdmin):
    add_form = MemberCreationForm
    form = MemberChangeForm
    autocomplete_fields = ["family"]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("first_name", "middle_name", "last_name"),
                    ("nickname", "family"),
                    "gender",
                    "email",
                    "photo",
                )
            },
        ),
        (
            _("Important dates"),
            {
                "classes": ("collapse",),
                "fields": ("last_login", "date_joined"),
            },
        ),
        (
            _("Login Information"),
            {
                "classes": ("collapse",),
                "fields": ("username", "password"),
            },
        ),
        (
            _("Permissions"),
            {
                "classes": ("collapse",),
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    ("first_name", "middle_name", "last_name"),
                    "nickname",
                    "gender",
                    "email",
                )
            },
        ),
    ) + UserAdmin.add_fieldsets

    inlines = [EmailInline, PhoneInline, AddressInline]

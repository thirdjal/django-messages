from django.contrib import admin
from django.utils.translation import gettext as _

from .forms import AddressForm, EmailForm, PhoneForm
from .models import Address, Category, Email, Phone, Venue, Website


class AddressInline(admin.StackedInline):
    model = Address
    form = AddressForm
    extra = 0


class EmailInline(admin.TabularInline):
    model = Email
    form = EmailForm
    extra = 0


class PhoneInline(admin.TabularInline):
    model = Phone
    form = PhoneForm
    extra = 0


class WebsiteInline(admin.TabularInline):
    model = Website
    # form = WebsiteForm
    extra = 0


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    form = AddressForm
    list_display = ("__str__", "is_published", "member", "venue")
    list_filter = ("is_published", "city", "state", "zip_code")
    search_fields = (
        "street",
        "city",
        "state",
        "zip_code",
        "member__first_name",
        "member__nickname",
        "member__last_name",
        "venue__name",
    )


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    form = EmailForm
    list_display = ("address", "is_published", "is_subscribed", "member", "venue")
    list_filter = ("is_published", "is_subscribed")
    search_fields = (
        "address",
        "member__first_name",
        "member__nickname",
        "member__last_name",
        "venue__name",
    )


@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    form = PhoneForm
    list_display = ("number", "is_published", "member", "venue")
    list_filter = ("is_published",)
    search_fields = (
        "number",
        "member__first_name",
        "member__nickname",
        "member__last_name",
        "venue__name",
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    filter_horizontal = ["categories"]
    inlines = [AddressInline, EmailInline, PhoneInline, WebsiteInline]
    list_display = ("name", "get_category_list")
    list_filter = (
        "categories",
        "addresses__city",
        "addresses__state",
        "addresses__zip_code",
    )
    search_fields = ("name",)

    def get_category_list(self, obj):
        return ", ".join(category.name for category in obj.categories.all())

    get_category_list.short_description = _("categories")

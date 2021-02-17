from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from localflavor.us.models import STATE_CHOICES, USStateField, USZipCodeField
from phonenumber_field.modelfields import PhoneNumberField


User = get_user_model()


class Category(models.Model):
    name = models.CharField(_("name"), max_length=128)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Venue(models.Model):
    name = models.CharField(_("name"), max_length=128)
    categories = models.ManyToManyField(Category, related_name="venues")

    class Meta:
        ordering = ["name"]
        verbose_name = _("Venue")
        verbose_name_plural = _("Venues")

    def __str__(self):
        return self.name


class Address(models.Model):
    class Type(models.TextChoices):
        HOME = "H", _("Home")
        WORK = "W", _("Work")
        OTHER = "O", _("Other")

    type = models.CharField(
        _("address type"), max_length=1, choices=Type.choices, blank=True
    )
    street = models.CharField(_("street"), max_length=128)
    street2 = models.CharField(_("unit/apartment/suite"), max_length=128, blank=True)
    city = models.CharField(_("city"), max_length=62)
    state = USStateField(_("state"), choices=STATE_CHOICES)
    zip_code = USZipCodeField(_("ZIP code"))

    is_published = models.BooleanField(
        _("published"),
        default=True,
        help_text=_("Show this address to other members of the pack in the directory"),
    )
    member = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="addresses", blank=True, null=True
    )
    venue = models.ForeignKey(
        Venue, on_delete=models.CASCADE, related_name="addresses", blank=True, null=True
    )

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    def __str__(self):
        return self.get_single_line()

    def get_single_line(self):
        if self.street2:
            return f"{self.street} {self.street2}, {self.city}, {self.state}, {self.zip_code}"
        if self.street:
            return f"{self.street}, {self.city}, {self.state}, {self.zip_code}"


class Email(models.Model):
    class Type(models.TextChoices):
        HOME = "H", _("home")
        WORK = "W", _("work")
        OTHER = "O", _("other")

    type = models.CharField(
        _("email type"), max_length=1, choices=Type.choices, blank=True
    )
    address = models.EmailField(_("email address"))

    is_published = models.BooleanField(
        _("published"),
        default=True,
        help_text=_("Show this address to other members of the pack in the directory"),
    )
    is_subscribed = models.BooleanField(
        _("subscribed"),
        default=True,
        help_text=_("Subscribe to periodical e-mails form the pack at this address"),
    )
    member = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="emailaddresses",
        blank=True,
        null=True,
    )
    venue = models.ForeignKey(
        Venue,
        on_delete=models.CASCADE,
        related_name="emailaddresses",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("Email Address")
        verbose_name_plural = _("Email Addresses")

    def __str__(self):
        return self.address


class Phone(models.Model):
    class Type(models.TextChoices):
        HOME = "H", _("home")
        MOBILE = "M", _("mobile")
        WORK = "W", _("work")
        OTHER = "O", _("other")

    type = models.CharField(
        _("phone type"), max_length=1, choices=Type.choices, blank=True
    )
    number = PhoneNumberField(_("phone number"))

    is_published = models.BooleanField(
        _("published"),
        default=True,
        help_text=_("Show this number to other members of the pack in the directory"),
    )
    member = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="phonenumbers",
        blank=True,
        null=True,
    )
    venue = models.ForeignKey(
        Venue,
        on_delete=models.CASCADE,
        related_name="phonenumbers",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("Phone Number")
        verbose_name_plural = _("Phone Numbers")

    def __str__(self):
        return self.number.as_national


class Website(models.Model):

    url = models.URLField(_("Website URL"))
    venue = models.ForeignKey(
        Venue, on_delete=models.CASCADE, related_name="websites", blank=True, null=True
    )

    class Meta:
        verbose_name = _("Website")
        verbose_name_plural = _("Websites")

    def __str__(self):
        return self.url

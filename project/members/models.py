from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models import Count
from django.urls import reverse_lazy
from django.utils.translation import gettext as _


def get_photo_upload_path(instance, filename):
    return f"members/headshots/{instance.username}/{filename}"


class Family(models.Model):
    class Meta:
        verbose_name = _("family")
        verbose_name_plural = _("families")

    def __str__(self):
        if self.members.exists():
            return _("%(last_names)s Family") % {
                "last_names": "/".join(
                    self.members.values_list("last_name", flat=True)
                    .annotate(count=Count("last_name"))
                    .filter(count=1)
                )
            }

        else:
            return _("Empty Family")

    def get_adults(self):
        return self.members.filter(role__in=[Member.Role.PARENT, Member.Role.GUARDIAN])

    def get_children(self):
        return self.members.filter(role=Member.Role.SCOUT)


class MemberManager(UserManager):
    def create_user(
        self, username, first_name, last_name, email=None, password=None, **extra_fields
    ):
        return super().create_user(
            username,
            email,
            password,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )

    def create_superuser(
        self, username, first_name, last_name, email=None, password=None, **extra_fields
    ):
        return super().create_superuser(
            username,
            email,
            password,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )


class Member(AbstractUser):
    class Gender(models.TextChoices):
        MALE = "M", _("Boy")
        FEMALE = "F", _("Girl")
        NON_BINARY = "NB", _("Non-binary")
        OTHER = "O", _("Prefer not to say")

    class Role(models.TextChoices):
        SCOUT = "S", _("Child")
        PARENT = "P", _("Parent")
        GUARDIAN = "G", _("Guardian")
        OTHER = "E", _("Extended Family")
        FRIEND = "F", _("Friend of the Family")

    first_name = models.CharField(_("first name"), max_length=150)
    middle_name = models.CharField(_("middle_name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150)
    nickname = models.CharField(_("nickname"), max_length=150, blank=True)

    gender = models.CharField(_("gender"), max_length=2, choices=Gender.choices)
    family = models.ForeignKey(
        Family,
        on_delete=models.PROTECT,
        related_name="members",
        related_query_name="families",
        blank=True,
        null=True,
    )
    photo = models.ImageField(
        _("photo"),
        upload_to=get_photo_upload_path,
        default="img/generic.png",
        help_text=_(
            "We use profile photos in the Pack Directory to help members match "
            "names with faces. A good photo is taken from the shoulders up and "
            "with the face clearly visible. Photos are available only for Pack "
            "members and are not shared."
        ),
    )

    objects = MemberManager()

    REQUIRED_FIELDS = ["first_name", "last_name", "gender", "email"]

    class Meta:
        verbose_name = _("Member")
        verbose_name_plural = _("Members")

    def __str__(self):
        return self.get_full_name()

    def get_absolute_url(self):
        return reverse_lazy("members:detail", kwargs={"slug": self.username})

    def get_full_name(self):
        """
        Return the preferred name plus the last name with a space between
        """
        return f"{self.get_short_name()} {self.last_name}"

    def get_short_name(self):
        """
        Return either the nickname or first_name for the member.
        """
        return self.nickname or self.first_name

from django.db import models
from django.urls import reverse
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _


class PageQuerySet(models.QuerySet):
    def with_content_blocks(self, user):
        return self.prefetch_related(
            models.Prefetch(
                "content_blocks", queryset=ContentBlock.objects.get_visible(user=user)
            )
        )


class PageManager(models.Manager):
    def get_queryset(self):
        return PageQuerySet(self.model, using=self.db)

    def with_content_blocks(self, user):
        return self.get_queryset().with_content_blocks(user=user)


class Page(models.Model):
    class Base(models.TextChoices):
        HOME = "HOME", _("Home Page")
        ABOUT = "ABOUT", _("About Us")
        CONTACT = "CONTACT", _("Contact Form")
        REGISTER = "REGISTER", _("New Member Registration")

    title = models.CharField(_("page title"), max_length=128)
    slug = models.SlugField(_("slug"), unique=True, blank=True, null=True)

    shown_in_navbar = models.BooleanField(_("include in navigation"), default=False)
    base = models.CharField(
        _("base page"),
        max_length=8,
        choices=Base.choices,
        blank=True,
        null=True,
        unique=True,
    )

    objects = PageManager()

    class Meta:
        verbose_name = _("Web Page")
        verbose_name_plural = _("Web Pages")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if self.base == Page.Base.HOME:
            return reverse("pages:home")
        elif self.base == Page.Base.ABOUT:
            return reverse("pages:about")
        elif self.base == Page.Base.CONTACT:
            return reverse("pages:contact")
        elif self.base == Page.Base.REGISTER:
            return reverse("pages:register")
        else:
            return reverse("pages:detail", kwargs={"slug": self.slug})


class ContentBlockQuerySet(models.QuerySet):
    def anonymous(self):
        return self.filter(visibility__lte=self.model.Visibility.PUBLIC)

    def public(self):
        return self.filter(visibility=self.model.Visibility.PUBLIC)

    def private(self):
        return self.filter(visibility__gte=self.model.Visibility.PUBLIC)


class ContentBlockManager(models.Manager):
    def get_queryset(self):
        return ContentBlockQuerySet(self.model, using=self._db)

    def get_visible(self, user):
        if user.is_anonymous:
            return self.get_queryset().public()
        else:
            return self.get_queryset().private()


class ContentBlock(models.Model):
    class Visibility(models.IntegerChoices):
        ANONYMOUS = 0, _("Anonymous/Guests Only")
        PUBLIC = 1, _("Public")
        PRIVATE = 2, _("Members Only")

    visibility = models.IntegerField(
        _("content visibility"), choices=Visibility.choices, default=Visibility.PRIVATE
    )
    heading = models.CharField(_("heading"), max_length=128, blank=True)
    body = models.TextField(_("body"))
    page = models.ForeignKey(
        Page, on_delete=models.CASCADE, related_name="content_blocks"
    )

    objects = ContentBlockManager()

    class Meta:
        order_with_respect_to = "page"
        verbose_name = _("Content Block")
        verbose_name_plural = _("Content Blocks")

    def __str__(self):
        return self.heading or f"{strip_tags(self.body)[:30]}..."

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import DetailView

from .models import Page


class PageDetailView(DetailView):
    model = Page
    template_name = "pages/page_detail.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.content_blocks.exists():
            return obj
        else:
            raise PermissionDenied

    def get_queryset(self):
        return super().get_queryset().with_content_blocks(user=self.request.user)


class HomePageView(PageDetailView):
    template_name = "pages/home.html"

    def get_object(self, **kwargs):
        if self.request.user.is_authenticated and (
            (
                not self.request.user.family
                or self.request.user.family.members.count() == 1
            )
        ):
            messages.add_message(
                self.request,
                messages.INFO,
                _(
                    "WOW, Such empty! Go visit your <a class='alert-link' href='%(url)s'>My Family</a> "
                    "page to add some family members."
                ) % {"url": reverse("members:my-family")},
            )
        try:
            return self.get_queryset().get(base=Page.Base.HOME)
        except Page.DoesNotExist:
            raise Http404(
                _(
                    "The home page was requested but has not yet been created in the database"
                )
            )


class AboutPageView(PageDetailView):
    template_name = "pages/about.html"

    def get_object(self, **kwargs):
        try:
            return self.get_queryset().get(base=Page.Base.ABOUT)
        except Page.DoesNotExist:
            raise Http404(
                _(
                    "An about us page was requested but has not yet been created in the database"
                )
            )


class ContactPageView(PageDetailView):
    template_name = "pages/contact.html"

    def get_object(self, **kwargs):
        try:
            return self.get_queryset().get(base=Page.Base.CONTACT)
        except Page.DoesNotExist:
            raise Http404(
                _(
                    "A contact page was requested but has not yet been created in the database"
                )
            )


class RegisterPageView(PageDetailView):
    template_name = "pages/register.html"

    def get_object(self, **kwargs):
        try:
            return self.get_queryset().get(base=Page.Base.REGISTER)
        except Page.DoesNotExist:
            raise Http404(
                _(
                    "A registration page was requested but has not yet been created in the database"
                )
            )

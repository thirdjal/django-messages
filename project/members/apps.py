from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MembersConfig(AppConfig):
    name = "project.members"
    verbose_name = _("Members")

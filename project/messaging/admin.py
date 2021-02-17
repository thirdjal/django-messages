from django.contrib import admin
from django.utils.translation import gettext as _

from .models import Attachment, Message, Mailbox


class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 0


class MailboxInline(admin.TabularInline):
    model = Mailbox
    extra = 0
    autocomplete_fields = ["member"]
    readonly_fields = ("date_received", "date_read")
    verbose_name = _("recipient")
    verbose_name_plural = _("recipients")

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    inlines = [AttachmentInline, MailboxInline]

import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Count, Q, Subquery, OuterRef
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext as _

from pathlib import Path

User = get_user_model()


class Thread(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("thread")
        verbose_name_plural = _("threads")

    def __str__(self):
        return str(self.uuid)


class MessageQuerySet(models.QuerySet):
    def with_receipts(self, user):
        receipts = Mailbox.objects.filter(message=OuterRef('uuid'), member=user)
        return self.annotate(date_read=Subquery(receipts.values('date_read')))

    def prefetch_receipts(self, user):
        return self.prefetch_related(
            models.Prefetch("receipts", queryset=Mailbox.objects.filter(member=user))
        )


class Message(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="messages_sent", null=True
    )
    subject = models.CharField(
        _("subject"), max_length=998, help_text=_("The message subject")
    )
    body = models.TextField(_("body"), help_text=_("What do you want to say?"))
    recipients = models.ManyToManyField(
        User, related_name="messages", through="messaging.Mailbox", blank=True
    )

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_sent = models.DateTimeField(blank=True, null=True)
    thread = models.ForeignKey(
        Thread, on_delete=models.CASCADE, related_name="messages", blank=True
    )
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="replies", blank=True, null=True
    )

    objects = MessageQuerySet().as_manager()

    class Meta:
        get_latest_by = "date_modified"
        ordering = ["-date_modified"]
        verbose_name = _("message")
        verbose_name_plural = _("messages")

    def __str__(self):
        return _("On %(date)s at %(time)s, %(author)s wrote: %(subject)s") % {
            "date": self.date_modified.strftime("%B %-d, %Y"),
            "time": self.date_modified.strftime("%-I:%M %p %Z"),
            "author": self.author,
            "subject": self.subject,
        }

    def get_absolute_url(self):
        return reverse_lazy("messaging:detail", kwargs={"pk": self.uuid})

    def clean(self):
        if not self.thread_id:
            self.assign_thread()
        super().clean()

    def assign_thread(self):
        self.thread = self.parent.thread if self.parent else Thread.objects.create()

    def send(self):
        # TODO: implement sending the message
        self.date_sent = timezone.now()
        self.save()

    @property
    def status(self):
        """Should be accessed through a pre_fetched queryset"""
        return self.receipts.first()


def get_attachment_path(instance, filename):
    return f"messages/{instance.message.uuid}/{filename}"


class Attachment(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="attachments")
    file = models.FileField(_("file"), upload_to=get_attachment_path)

    class Meta:
        verbose_name = _("attachment")
        verbose_name_plural = _("attachments")

    def __str__(self):
        return Path(self.file.name).name


class MailboxQuerySet(models.QuerySet):
    def unread(self):
        return self.aggregate(count=Count("message", filter=Q(date_read__isnull=True, folder=Mailbox.Folder.INBOX)))

    def mark_read(self):
        self.update(date_read=timezone.now())

    def mark_unread(self):
        self.update(date_read=None)


class MailboxManager(models.Manager):
    def get_queryset(self):
        return MailboxQuerySet(self.model, using=self._db)

    def mark_read(self):
        return self.get_queryset().mark_read()

    def mark_unread(self):
        return self.get_queryset().mark_unread()

    def unread(self):
        return self.get_queryset().unread()["count"]


class Mailbox(models.Model):

    class Folder(models.IntegerChoices):
        INBOX = 1, _("Inbox")
        ARCHIVE = 2, _("Archive")
        TRASH = 3, _("Trash")

    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="receipts")
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mailbox")
    folder = models.IntegerField(_("folder"), choices=Folder.choices, default=Folder.INBOX)

    date_received = models.DateTimeField(_("received"), auto_now_add=True)
    date_read = models.DateTimeField(_("read"), blank=True, null=True)

    objects = MailboxManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["message", "member"], name="unique_receipt_per_member"
            )
        ]
        verbose_name = _("mailbox")
        verbose_name_plural = _("mailboxes")

    def __str__(self):
        return self.member.__str__()

    @property
    def read(self):
        return bool(self.date_read)

    def mark_read(self):
        if not self.date_read:
            self.date_read = timezone.now()
            self.save()

    def mark_unread(self):
        self.date_read = None
        self.save()

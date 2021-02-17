from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .forms import AttachmentForm, MessageForm
from .mixins import MessageIsForUserTest
from .models import Attachment, Mailbox, Message


class MailboxView(LoginRequiredMixin, ListView):
    model = Mailbox
    context_object_name = "mailbox_items"
    template_name = "messaging/message_list.html"

    def get_queryset(self):
        return super().get_queryset().select_related("message").filter(member=self.request.user)


class InboxView(MailboxView):

    def get_queryset(self):
        return super().get_queryset().filter(folder=Mailbox.Folder.INBOX)


class MailboxArchiveView(MailboxView):

    def get_queryset(self):
        return super().get_queryset().filter(folder=Mailbox.Folder.ARCHIVE)


class MailboxTrashView(MailboxView):

    def get_queryset(self):
        return super().get_queryset().filter(folder=Mailbox.Folder.TRASH)


class MailboxDraftsView(LoginRequiredMixin, ListView):
    model = Message
    context_object_name = "drafts"
    template_name = "messaging/drafts.html"

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user, date_sent__isnull=True)


class MailboxSentView(LoginRequiredMixin, ListView):
    model = Message
    context_object_name = "sent_items"
    template_name = "messaging/sent_items.html"

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user, date_sent__isnull=False)


class MailboxDetailView(MessageIsForUserTest, DetailView):
    model = Message
    context_object_name = "message"
    template_name = "messaging/message_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = MessageForm
        context["status"] = Mailbox.objects.filter(message=self.object, member=self.request.user).first()
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.receipts.filter(member=self.request.user).exists():
            obj.receipts.get(member=self.request.user).mark_read()
        return obj


class MessageCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Message
    template_name = "messaging/message_form.html"
    form_class = MessageForm
    success_message = _("Your message: <strong>%(subject)s</strong>, was %(action)s successfully.")

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        attachment_form = context["attachment_form"]
        files = self.request.FILES.getlist('attachments')
        if attachment_form.is_valid():
            message = form.save(commit=False)
            message.author = self.request.user
            for file in files:
                Attachment.objects.create(message=message, file=file)
            return super().form_valid(form)
        else:
            return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["attachment_form"] = AttachmentForm(self.request.POST, self.request.FILES)
        else:
            context["attachment_form"] = AttachmentForm()
        return context

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            action=_("sent") if self.object.date_sent else _("saved")
        )

    def get_success_url(self):
        if 'draft' in self.request.POST:
            return reverse_lazy("messaging:update", kwargs={"pk": self.object.uuid})

        self.object.send()
        return reverse_lazy("messaging:detail", kwargs={"pk": self.object.uuid})


class MessageDraftView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Message
    template_name = "messaging/message_form.html"
    form_class = MessageForm
    success_message = _("Your message: <strong>%(subject)s</strong>, was %(action)s successfully.")

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        attachment_form = context["attachment_form"]
        files = self.request.FILES.getlist('attachments')
        if attachment_form.is_valid():
            message = form.save(commit=False)
            for file in files:
                Attachment.objects.create(message=message, file=file)
            return super().form_valid(form)
        else:
            return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["attachment_form"] = AttachmentForm(self.request.POST, self.request.FILES)
        else:
            context["attachment_form"] = AttachmentForm()
        return context

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            action=_("sent") if self.object.date_sent else _("saved")
        )

    def get_success_url(self):
        if 'draft' in self.request.POST:
            return reverse_lazy("messaging:update", kwargs={"pk": self.object.uuid})

        self.object.send()
        return reverse_lazy("messaging:detail", kwargs={"pk": self.object.uuid})

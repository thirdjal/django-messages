from django.urls import path
from django.views.generic import RedirectView

from .api import update, delete_attachment
from .views import (
    MessageCreateView,
    MailboxDetailView,
    MailboxDraftsView,
    MailboxArchiveView,
    MailboxTrashView,
    InboxView,
    MailboxSentView,
    MessageDraftView,
)

app_name = "messaging"
urlpatterns = [
    path("", InboxView.as_view(), name="inbox"),
    path("inbox/", RedirectView.as_view(pattern_name="messaging:inbox")),
    path("compose/", MessageCreateView.as_view(), name="create"),
    path("drafts/", MailboxDraftsView.as_view(), name="drafts"),
    path("sent/", MailboxSentView.as_view(), name="sent"),
    path("trash/", MailboxTrashView.as_view(), name="trash"),
    path("archive/", MailboxArchiveView.as_view(), name="archive"),
    path("drafts/<uuid:pk>/", MessageDraftView.as_view(), name="update"),
    path("<uuid:pk>/", MailboxDetailView.as_view(), name="detail"),
    path("api/v1/update/", update, name="api_update"),
    path("api/v1/delete/", delete_attachment, name="api_delete"),
]

import json

from django.core.exceptions import PermissionDenied
from django.http import JsonResponse

from .models import Attachment, Mailbox


def update(request):
    """
    Function to allow a user to toggle the read status of a message via JavaScript.
    Takes input through HTTP POST with the message_id and the desired status either
    read or unread. Does not modify the read status of the message if it is already
    in the desired state.
    """
    if request.method != 'POST':
        return
    body = json.loads(request.body)
    obj = Mailbox.objects.get(message_id=body['message_id'], member=request.user)
    modified = False

    if body['action'] == "read":
        if not obj.read:
            obj.mark_read()
            modified = True

    elif body['action'] == "unread":
        if obj.read:
            obj.mark_unread()
            modified = True

    elif body['action'] == "archive":
        if obj.folder != Mailbox.Folder.ARCHIVE:
            obj.folder = Mailbox.Folder.ARCHIVE
            obj.save()
            modified = True

    elif body['action'] == "unarchive":
        if obj.folder != Mailbox.Folder.INBOX:
            obj.folder = Mailbox.Folder.INBOX
            obj.save()
            modified = True

    elif body['action'] == "delete":
        if obj.folder != Mailbox.Folder.TRASH:
            obj.folder = Mailbox.Folder.TRASH
            obj.save()
            modified = True

    elif body['action'] == "recover":
        if obj.folder != Mailbox.Folder.INBOX:
            obj.folder = Mailbox.Folder.INBOX
            obj.save()
            modified = True

    unread_count = Mailbox.objects.filter(member=request.user).unread()

    return JsonResponse({"was_modified": modified, "is_read": obj.read, "folder": obj.folder, "unread_count": unread_count})


def delete_attachment(request):
    if request.method != 'DELETE':
        return JsonResponse({"Success": False})
    body = json.loads(request.body)
    obj = Attachment.objects.get(id=body['attachment_id'])
    if obj.message.author == request.user:
        obj.file.delete()
        obj.delete()
        return JsonResponse({"Success": True})
    else:
        raise PermissionDenied

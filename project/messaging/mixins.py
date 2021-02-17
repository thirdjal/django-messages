from django.contrib.auth.mixins import UserPassesTestMixin


class MessageIsForUserTest(UserPassesTestMixin):
    """Check to ensure the user requesting a message is either its author or a recipient"""
    def test_func(self):
        obj = self.get_object()
        return self.request.user in obj.recipients.all() or self.request.user == obj.author

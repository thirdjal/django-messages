from django.views.generic import DetailView

from .models import Member


class MemberDetailView(DetailView):
    model = Member
    slug_field = "username"


class MyFamilyView(MemberDetailView):
    def get_object(self, queryset=None):
        return self.get_queryset().get(id=self.request.user.id)

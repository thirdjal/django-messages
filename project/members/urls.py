from django.urls import path

from .views import MemberDetailView, MyFamilyView

app_name = "members"
urlpatterns = [
    path("my-family/", MyFamilyView.as_view(), name="my-family"),
    path("<slug:slug>/", MemberDetailView.as_view(), name="detail"),
]

from django.urls import path
from django.views.generic import RedirectView

from .views import AboutPageView, ContactPageView, HomePageView, RegisterPageView
from .views import PageDetailView

app_name = "pages"
urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("home/", RedirectView.as_view(pattern_name="pages:home")),
    path("about/", AboutPageView.as_view(), name="about"),
    path("contact/", ContactPageView.as_view(), name="contact"),
    path("register/", RegisterPageView.as_view(), name="register"),
    path("<slug:slug>/", PageDetailView.as_view(), name="detail"),
]

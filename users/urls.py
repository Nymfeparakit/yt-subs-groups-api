from django.urls import re_path

from .views import GoogleLoginView


urlpatterns = [
    re_path(r'^rest-auth/google/$', GoogleLoginView.as_view(), name='google_login'),
]
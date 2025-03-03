from django.urls import path

from .views import *

urlpatterns = [
    path("login", login),
    path("register", register),
    path("delete", delete_user),
    path("get", get_user),
]

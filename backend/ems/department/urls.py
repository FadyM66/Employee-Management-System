from django.urls import path
from .views import *


urlpatterns = [
    path('create', create),
    path('get', get),
    path('delete', delete),
    path('update', update),
]
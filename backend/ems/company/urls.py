from django.urls import path

from .views import test, x

urlpatterns = [
    path('test', test),
    path('*', x)
]
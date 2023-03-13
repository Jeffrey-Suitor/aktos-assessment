from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path("consumers", views.get_consumers, name="get_consumers"),
]

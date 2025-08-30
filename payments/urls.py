# payments/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_payment, name="create_payment"),
]

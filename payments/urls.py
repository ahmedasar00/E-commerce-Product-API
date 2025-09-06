# payments/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # The URL now accepts an integer called 'order_id'
    path("create/<int:order_id>/", views.create_payment, name="create_payment"),
]

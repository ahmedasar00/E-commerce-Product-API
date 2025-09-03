# orders/urls.py

from django.urls import path
from .views import (
    OrderListView,
    OrderDetailView,
    OrderCreateView,
    OrderCancelView,
    OrderDeleteView,
)

urlpatterns = [
    path("", OrderListView.as_view(), name="order_list"),
    path("create/", OrderCreateView.as_view(), name="order_create"),
    path(
        "<int:pk>/", OrderDetailView.as_view(), name="order_detail"
    ),  # The fix is here
    path("<int:pk>/cancel/", OrderCancelView.as_view(), name="order_cancel"),
    path("<int:pk>/delete/", OrderDeleteView.as_view(), name="order_delete"),
]

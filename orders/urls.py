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
    path("my-orders/", OrderListView.as_view(), name="order_list"),
    path("my-orders/create/", OrderCreateView.as_view(), name="order_create"),
    path(
        "my-orders/<int:pk>/", OrderDetailView.as_view(), name="order_detail"
    ),  # 👈 The fix is here
    path("my-orders/<int:pk>/cancel/", OrderCancelView.as_view(), name="order_cancel"),
    path("my-orders/<int:pk>/delete/", OrderDeleteView.as_view(), name="order_delete"),
]

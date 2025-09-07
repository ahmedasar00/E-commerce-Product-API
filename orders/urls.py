# orders/urls.py

from django.urls import path, include
from .views import (
    OrderListView,
    OrderDetailView,
    OrderCreateView,
    OrderCancelView,
    OrderDeleteView,
)
from . import views

from rest_framework.routers import DefaultRouter

api_router = DefaultRouter()
api_router.register(r"", views.OrderViewSet, basename="order-api")

urlpatterns = [
    path("", OrderListView.as_view(), name="order_list"),
    path("create/", OrderCreateView.as_view(), name="order_create"),
    path("api/", include(api_router.urls)),
    path(
        "<int:pk>/", OrderDetailView.as_view(), name="order_detail"
    ),  # The fix is here
    path("<int:pk>/cancel/", OrderCancelView.as_view(), name="order_cancel"),
    path("<int:pk>/delete/", OrderDeleteView.as_view(), name="order_delete"),
]

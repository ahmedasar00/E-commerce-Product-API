# categories/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

api_router = DefaultRouter()
api_router.register(r"", views.CategoryViewSet, basename="category-api")

urlpatterns = [
    path("", views.CategoryListView.as_view(), name="category-list"),
    path("new/", views.CategoryCreateView.as_view(), name="category-create"),
    path("api/", include(api_router.urls)),
    path("<slug:slug>/", views.CategoryDetailView.as_view(), name="category-detail"),
    path(
        "<slug:slug>/edit/", views.CategoryUpdateView.as_view(), name="category-update"
    ),
    path(
        "<slug:slug>/delete/",
        views.CategoryDeleteView.as_view(),
        name="category-delete",
    ),
]

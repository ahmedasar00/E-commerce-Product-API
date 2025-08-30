# ecommerce_api/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from categories import views as category_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("users.urls")),
    path("api/v1/categories/", include("categories.urls")),
    path(
        "categories/", category_views.CategoryListView.as_view(), name="category-list"
    ),
    path(
        "categories/new/",
        category_views.CategoryCreateView.as_view(),
        name="category-create",
    ),
    path(
        "categories/<slug:slug>/",
        category_views.CategoryDetailView.as_view(),
        name="category-detail",
    ),
    path(
        "categories/<slug:slug>/edit/",
        category_views.CategoryUpdateView.as_view(),
        name="category-update",
    ),
    path(
        "categories/<slug:slug>/delete/",
        category_views.CategoryDeleteView.as_view(),
        name="category-delete",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

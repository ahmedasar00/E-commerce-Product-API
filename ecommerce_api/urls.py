from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from categories import views as category_views

urlpatterns = [
    path("admin/", admin.site.urls),
    # Route all API requests starting with 'api/' to the api_urls.py file
    path("api/", include("orders.api_urls")),
    # Route all other requests to the standard urls.py file
    path("", include("orders.urls")),
    path("", include("users.urls")),
    path("payments/", include("payments.urls")),
    # Include the API urls. All URLs here will be prefixed with 'api/'.
    # Example: /api/reviews/
    path("api/", include("reviews.api_urls")),
    # Include the web page urls. All URLs here will be prefixed with 'reviews/'.
    # Example: /reviews/
    path("reviews/", include("reviews.web_urls")),
    # You might want to include DRF's built-in login views for browsable API
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
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
    path("products/", include("products.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

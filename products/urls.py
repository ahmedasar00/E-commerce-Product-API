from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# ==================================================
# API URLs (using DRF Router)
# ==================================================
# The router automatically generates RESTful API routes (GET, POST, PUT, DELETE)
# for the ProductViewSet.
api_router = DefaultRouter()
api_router.register(r"", views.ProductViewSet, basename="product-api")

# ==================================================
# Template (Web Page) URLs
# ==================================================
# These URLs are for the user-facing web pages (using Django class-based views).
# They render HTML templates for CRUD operations.
template_urls = [
    path("", views.ProductListView.as_view(), name="product-list"),  # Show all products
    path(
        "new/", views.ProductCreateView.as_view(), name="product-create"
    ),  # Create a new product
    path(
        "<int:pk>/", views.ProductDetailView.as_view(), name="product-detail"
    ),  # Show product details
    path(
        "<int:pk>/edit/", views.ProductUpdateView.as_view(), name="product-update"
    ),  # Edit a product
    path(
        "<int:pk>/delete/", views.ProductDeleteView.as_view(), name="product-delete"
    ),  # Delete a product
]

# ==================================================
# Main URL Patterns for the App
# ==================================================
# Here we combine both API and Template URLs.
# This file will be included in the project's main urls.py (e.g., under /products/).
urlpatterns = [
    # Web Pages (HTML templates)
    # Examples: /products/, /products/new/, /products/1/
    path("", include(template_urls)),
    # API Endpoints (JSON responses)
    # Examples: /products/api/, /products/api/1/
    path("api/", include(api_router.urls)),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

"""
API Router setup:
This will automatically create API routes for ProductViewSet.
"""
api_router = DefaultRouter()
api_router.register(r"", views.ProductViewSet, basename="product-api")


"""
Template-based routes:
These routes return HTML pages for product management.
"""
template_urls = [
    path(
        "", views.ProductListView.as_view(), name="product_list"
    ),  # Show a list of all products
    path(
        "new/", views.ProductCreateView.as_view(), name="product-create"
    ),  # Create a new product
    path(
        "<int:pk>/", views.ProductDetailView.as_view(), name="product-detail"
    ),  # Show details of a single product
    path(
        "<int:pk>/edit/", views.ProductUpdateView.as_view(), name="product-update"
    ),  # Edit a product
    path(
        "<int:pk>/delete/", views.ProductDeleteView.as_view(), name="product-delete"
    ),  # Delete a product
]


"""
Main URL configuration:
- Template URLs for web pages
- API URLs for JSON responses
"""
urlpatterns = [
    path("", include(template_urls)),  # Web pages (HTML templates)
    path("api/", include(api_router.urls)),  # API endpoints (REST API)
]

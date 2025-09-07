from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# --- Django REST Framework API URLs ---

# Create a router and register our viewset with it.
router = DefaultRouter()
router.register(r"reviews", views.ReviewViewSet, basename="review")

# The API URLs are now determined automatically by the router.
# - /api/reviews/ -> list all reviews (GET) or create a new one (POST)
# - /api/reviews/{pk}/ -> retrieve (GET), update (PUT/PATCH), or delete (DELETE) a specific review

# --- Django Template-Based URLs ---

urlpatterns = [
    # API URLs
    path("", views.ReviewListView.as_view(), name="review-list"),
    path("api/", include(router.urls)),
    # Template-based URLs
    path("new/", views.ReviewCreateView.as_view(), name="review-create"),
    path("<int:pk>/edit/", views.ReviewUpdateView.as_view(), name="review-update"),
    path("<int:pk>/delete/", views.ReviewDeleteView.as_view(), name="review-delete"),
]

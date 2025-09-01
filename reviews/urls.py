from django.urls import path
from .views import ReviewListView, ReviewDetailView

# This file is for the user-facing web pages, not the API.
app_name = "reviews"

urlpatterns = [
    # Example: /reviews/
    path("", ReviewListView.as_view(), name="review-list"),
    # Example: /reviews/5/
    path("<int:pk>/", ReviewDetailView.as_view(), name="review-detail"),
]

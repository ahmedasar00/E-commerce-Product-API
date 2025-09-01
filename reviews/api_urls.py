from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet

# Create a router and register our viewsets with it.
# The router automatically generates the URL patterns for the ViewSet.
router = DefaultRouter()
router.register(r"reviews", ReviewViewSet, basename="review")

# The API URLs are now determined automatically by the router.
# - /api/reviews/ -> GET (list), POST (create)
# - /api/reviews/{pk}/ -> GET (retrieve), PUT (update), PATCH (partial_update), DELETE (destroy)
urlpatterns = [
    path("", include(router.urls)),
]

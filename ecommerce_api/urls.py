from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home_view, name="home"),
    path("products/", include("products.urls")),
    path("users/", include("users.urls")),
    path("orders/", include("orders.urls")),
    path("reviews/", include("reviews.urls")),
    path("payments/", include("payments.urls")),
    path("categories/", include("categories.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # path("api/e1/categories/", include("categories.urls")),
    # path("api/11/reviews/", include("reviews.api_urls")),  # للـ API
    # Route all API requests starting with 'api/' to the api_urls.py file
    # path("api/", include("orders.api_urls")),
    # Route all other requests to the standard urls.py file

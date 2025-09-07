from django.urls import path
from .views import (
    register_view,
    login_view,
    logout_view,
    profile_view,
    AddressListView,
    AddressCreateView,
    AddressUpdateView,
    AddressDeleteView,
)

urlpatterns = [
    # --- Auth URLs ---
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile_view, name="profile"),
    # === URLs for Address Management ===
    path("profile/addresses/", AddressListView.as_view(), name="address_list"),
    path("profile/addresses/add/", AddressCreateView.as_view(), name="address_add"),
    path(
        "profile/addresses/<int:pk>/edit/",
        AddressUpdateView.as_view(),
        name="address_edit",
    ),
    path(
        "profile/addresses/<int:pk>/delete/",
        AddressDeleteView.as_view(),
        name="address_delete",
    ),
]
